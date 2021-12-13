from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='hodgepodge',
    version='3.1.1',
    author='Tyler Fisher',
    author_email='tylerfisher@tylerfisher.ca',
    description="A hodgepodge of helpful code that's hopefully helpful to you.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/whitfieldsdad/hodgepodge',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Topic :: Security',
    ],
    packages=find_packages(),
    install_requires=[],
)
