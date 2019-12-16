import json

from typing import List, Tuple
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


def simple_setup(info, data_files: List[Tuple[str, List[str]]] = [], python_version: str = '>=3.6', excludes: list = []):
    with open('resources/requirements.txt') as fr:
        requirements = [x for x in fr.readlines() if not x.startswith('--extra-index-url')]
        links = [x[18:] for x in fr.readlines() if x.startswith('--extra-index-url')]

    data_files.append(('resources', ['resources/setup.json', 'resources/requirements.txt']))
    setup(
        **info,

        long_description=long_description,
        long_description_content_type="text/markdown",

        install_requires=requirements,
        python_requires=python_version,
        dependency_links=links,

        packages=find_packages(exclude=excludes),
        data_files=data_files,
        include_package_data=True
    )


simple_setup(json.load(open('resources/setup.json')))
