import collections
import copy
from dataclasses import dataclass
import json
import os
import subprocess
import tempfile
from typing import Any, Iterable, Iterator, Optional, Set, Union
from hodgepodge import files, strings
import networkx as nx
import genson
import logging

DEFAULT_DOT_INDENT = 4

logger = logging.getLogger(__name__)


def get_keys_from_files(paths: Union[str, Iterable[str]]) -> Set[str]:
    """
    Extract all keys from the JSON schemas generated from the documents in the specified files.

    Supported input file types:

    """
    if isinstance(paths, str):
        paths = [paths]
    
    docs = files.read_documents_from_files(paths)
    schema = get_json_schema_from_dicts(docs)
    return set(get_keys_from_json_schema(schema))


def get_json_schema_from_dict(doc: dict, ignored_properties: Optional[Iterable[str]] = None) -> dict:
    """
    Generate a JSON schema from the provided dictionary.
    """
    return get_json_schema_from_dicts([doc], ignored_properties=ignored_properties)


def get_json_schema_from_dicts(docs: Iterable[dict], ignored_properties: Optional[Iterable[str]] = None) -> dict:
    """
    Generate a JSON schema from the provided iterable of dictionaries.
    """
    builder = genson.SchemaBuilder()
    for doc in docs:
        builder.add_object(doc)
    
    schema = builder.to_schema()

    if ignored_properties:
        schema = _drop_ignored_properties_from_json_schema(schema, ignored_properties)
    
    return schema


def _drop_ignored_properties_from_json_schema(schema: dict, ignored_properties: Iterable[str]) -> dict:
    """
    Drop the specified ignored properties from the provided JSON schema.
    """
    ignored_properties = set(ignored_properties)
    keys = get_keys_from_json_schema(schema)

    for key in keys:
        if key in ignored_properties:
            parts = key.split('.')
            parent = schema
            for part in parts[:-1]:
                if part.endswith('[]'):
                    part = part[:-2]
                    parent = parent['properties'][part]['items']
                else:
                    parent = parent['properties'][part]
            del parent['properties'][parts[-1].rstrip('[]')]

    return schema


def get_json_schema_from_files(paths: Union[str, Iterable[str]], ignored_properties: Optional[Iterable[str]] = None) -> dict:
    """
    Generate a JSON schema from the documents in the specified input files.

    The input files can be in any of the following formats:

    - JSON
    - JSON Lines (JSONL)
    - YAML
    - Parquet
    - CSV

    If a list of ignored properties is provided, they will not be included in the generated JSON schema.
    """
    if isinstance(paths, str):
        paths = [paths]

    docs = files.read_documents_from_files(paths)
    schema = get_json_schema_from_dicts(docs, ignored_properties=ignored_properties)
    return schema


def get_json_schema_from_file(path: str, ignored_properties: Optional[Iterable[str]] = None) -> dict:
    """
    Generate a JSON schema from the documents in the specified file.

    The file can be in any of the following formats:

    - JSON
    - JSON Lines (JSONL)
    - YAML
    - Parquet
    - CSV
    """
    return get_json_schema_from_files([path], ignored_properties=ignored_properties)


def merge_json_schemas(schemas: Iterable[dict]) -> dict:
    """
    Merge the provided JSON schemas into a single unified schema.
    """
    schemas = tuple(schemas)
    n = len(schemas)
    if n == 0:
        raise ValueError("No JSON schemas provided")
    elif n == 1:
        return next(iter(schemas))

    builder = genson.SchemaBuilder()
    for schema in schemas:
        builder.add_schema(schema)
    return builder.to_schema()


# TODO
def json_schema_to_nx_digraph(schema: dict) -> nx.DiGraph:
    """
    Convert a JSON schema into a NetworkX directed graph (DiGraph).
    """
    keys = sorted(get_keys_from_json_schema(schema))
    
    g = nx.DiGraph()
    for key in keys:
        parts = key.split('.')
        for i in range(len(parts)):
            node = '.'.join(parts[:i + 1])
            if node not in g:
                g.add_node(node, label=parts[i])

            if i > 0:
                parent_node = '.'.join(parts[:i])
                g.add_edge(parent_node, node)

    return g


def get_keys_from_json_schema(schema: dict[str, Any]) -> Iterator[str]:
    """
    Extract property paths from a JSON Schema, including nested objects, arrays,
    and `anyOf` branches.

    Array properties use `[]` notation, e.g. `users[].profile.name`.
    """
    keys: set[str] = set()

    def walk(node: dict[str, Any], parent_keys: Optional[list[str]] = None) -> None:
        parent_keys = parent_keys or []

        # Keys where the value can be one of several types
        for branch in node.get("anyOf", []):
            if isinstance(branch, dict):
                walk(branch, parent_keys)

        for key, value in node.get("properties", {}).items():
            value_type = value.get("type")

            # Keys with object values (e.g. objects representing files, processes, users, etc.)
            if value_type == 'object':
                path = parent_keys + [key]
                keys.add(".".join(path))

            # Keys with array values (e.g. arrays of integers, arrays of objects)
            elif value_type == 'array':
                path = parent_keys + [f"{key}[]"]
                keys.add(".".join(path))

                items = value.get("items", {})
                if isinstance(items, dict):
                    walk(items, path)

            # Keys with scalar values (i.e. strings, booleans, integers, etc.)
            else:
                path = parent_keys + [key]
                keys.add(".".join(path))

    walk(schema)
    return iter(sorted(keys))


@dataclass(frozen=True)
class JSONSchemaGraphConfig:
    """
    Configuration options for visualizing JSON schemas as graphs
    """
    graph_font_name: str = 'Helvetica'
    graph_font_size: int = 12
    graph_layout: str = 'dot'
    graph_rankdir: str = 'LR'
    graph_splines: str = 'spline'
    graph_background_color: str = 'white'
    node_shape: str = 'box'
    node_style: str = 'rounded,filled'
    node_fillcolor: str = 'gray96'
    node_fontname: str = 'Helvetica'
    node_fontsize: int = 11
    node_margin: str = '0.18,0.10'
    edge_color: str = 'blue'
    edge_arrowsize: float = 0.7
    edge_arrowhead: str = 'vee'
    edge_tailport: str = 'e'
    subgraph_color: str = 'gray70'
    concentrate_edges: bool = True
    vertical_spacing: float = 1
    horizontal_spacing: float = 0.25


# TODO: make node colour customizable
# TODO: make edge colour customizable
# TODO: add edge weight colouring (e.g. to show how often a key was present)
def json_schema_to_dot(
        schema: dict, 
        config: Optional[JSONSchemaGraphConfig] = None, 
        indent: int = DEFAULT_DOT_INDENT) -> str:
    """
    Convert a JSON schema into a Graphviz DOT string.
    """
    g = json_schema_to_nx_digraph(schema)

    config = config or JSONSchemaGraphConfig()
    sep = ' ' * indent
    lines = [
        'digraph G {',
        f'{sep}layout={config.graph_layout}',
        f'{sep}rankdir={config.graph_rankdir}',
        f'{sep}splines={config.graph_splines}',
        f'{sep}concentrate={str(config.concentrate_edges).lower()}',
        f'{sep}ranksep={config.vertical_spacing}',
        f'{sep}nodesep={config.horizontal_spacing}',
        '',
        f'{sep}bgcolor={config.graph_background_color}',
        '',
        f'{sep}graph [',
        f'{sep * 2}fontname="{config.graph_font_name}"',
        f'{sep * 2}fontsize={config.graph_font_size}',
        f'{sep}]'
        '',        '',
        f'{sep}node [',
        f'{sep * 2}shape={config.node_shape}',
        f'{sep * 2}style="{config.node_style}"',
        f'{sep * 2}fillcolor={config.node_fillcolor}',
        f'{sep * 2}fontname="{config.node_fontname}"',
        f'{sep * 2}fontsize={config.node_fontsize}',
        f'{sep * 2}margin="{config.node_margin}"',
        f'{sep}]',
        '',
        f'{sep}edge [',
        f'{sep * 2}color={config.edge_color}',
        f'{sep * 2}arrowsize={config.edge_arrowsize}',
        f'{sep * 2}arrowhead={config.edge_arrowhead}',
        f'{sep * 2}tailport={config.edge_tailport}',
        f'{sep}]',
        '',
    ]

    # Place nodes into the subgraph corresponding to their parent node (i.e. subgraphs contain nodes and their siblings)
    nodes_by_parent = collections.defaultdict(list)
    for node, data in g.nodes(data=True):
        parent = data.get('parent')
        if parent:
            nodes_by_parent[parent].append((node, data))

    # Add nodes
    # - Nodes without a parent are placed at the top level of the graph
    # - Nodes with a parent are placed in the subgraph associated with their siblings
    for node, data in sorted(g.nodes(data=True)):
        if node == '.':
            continue

        parent = data.get('parent')
        if not parent:
            label = data.get('label')
            if label:
                lines.append(f'{sep}"{node}" [label="{label}"]')
            else:
                lines.append(f'{sep}"{node}"')

    for parent, nodes in sorted(nodes_by_parent.items()):
        subgraph_label = copy.copy(parent)
        subgraph_cluster = copy.copy(parent)
        subgraph_cluster = strings.multi_replace(subgraph_cluster, ['.', '-'], '_')
        subgraph_cluster = strings.multi_replace(subgraph_cluster, ['[', ']'], '')

        lines.append('')
        lines.append(f'{sep}subgraph cluster_{subgraph_cluster} {{')
        lines.append(f'{sep * 2}label="{subgraph_label}"')
        lines.append(f'{sep * 2}color={config.subgraph_color}')
        lines.append('')

        for node, data in sorted(nodes):
            label = data.get('label')
            if label:
                lines.append(f'{sep * 2}"{node}" [label="{label}"]')
            else:
                lines.append(f'{sep * 2}"{node}"')
        
        lines.append(f'{sep}}}')
    lines.append('')

    # Add edges
    if g.number_of_edges() > 0:
        lines.append('')
        for a, b in g.edges:
            if a == '.' or b == '.':
                continue

            lines.append(f'{sep}"{a}" -> "{b}"')

    lines.append('}')

    return '\n'.join(lines)


def to_json_file(o: dict, output_file: str):
    """
    Save the provided JSON schema as a JSON file.
    """
    with open(output_file, 'w') as f:
        json.dump(o, f, indent=2)


def json_schema_to_dot_file(schema: dict, output_file: str, indent: int = DEFAULT_DOT_INDENT):
    """
    Save the provided JSON schema as a Graphviz DOT file.
    """
    dot = json_schema_to_dot(schema, indent=indent)
    with open(output_file, 'w') as f:
        f.write(dot)


def json_schema_to_image_file(schema: dict, output_file: str, indent: int = DEFAULT_DOT_INDENT):
    """
    Save the provided JSON schema as an image file (PNG or SVG).

    Supported output formats:

    - PNG
    - SVG
    """
    output_filename = os.path.basename(output_file)
    output_format = output_filename.split('.')[-1]
    if output_format not in ['png', 'svg']:
        raise ValueError(f"Unsupported output format: {output_format}")

    dot = json_schema_to_dot(schema, indent=indent)
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(dot.encode())
        fp.flush()
        subprocess.run(['dot', f'-T{output_format}', '-Gdpi=300', fp.name, '-o', output_file])


def json_schema_to_image(schema: dict, output_format: str, indent: int = DEFAULT_DOT_INDENT) -> bytes:
    """
    Convert the provided JSON schema into an image in the specified format and return it as bytes.
    
    Supported output formats:
    """
    if output_format not in ['png', 'svg']:
        raise ValueError(f"Unsupported output format: {output_format}")

    dot = json_schema_to_dot(schema, indent=indent)
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(dot.encode())
        fp.flush()
        p = subprocess.run(['dot', f'-T{output_format}', '-Gdpi=300', fp.name], capture_output=True)
        return p.stdout
