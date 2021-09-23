from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='hodgepodge',
    version='0.3.2',
    author='Tyler Fisher',
    author_email='tylerfisher@tylerfisher.ca',
    description="A hodgepodge of helpful code that's hopefully helpful to you.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    install_requires=[],
)
