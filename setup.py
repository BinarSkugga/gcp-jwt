import json
import sys

from typing import List, Tuple
from setuptools import setup, find_packages


class VersionInfo:
    def __init__(self, name: str, version: str, author: str, email: str, description: str, license: str):
        self._name = name
        self._version = version
        self._author = author
        self._email = email
        self._description = description
        self._license = license

    @staticmethod
    def from_json(file: str):
        data = json.load(open(file))
        if 'name' not in data or 'version' not in data or 'author' not in data or 'email' not in data \
                or 'description' not in data or 'license' not in data:
            print('Invalid json data for version info.', file=sys.stderr, flush=True)
            return None

        return VersionInfo(data['name'], data['version'], data['author'], data['email'], data['description'], data['license'])

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, new_author: str):
        self._author = new_author

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email: str):
        self._version = new_email

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description: str):
        self._description = new_description

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, new_version: str):
        self._version = new_version

    @property
    def license(self):
        return self._license

    @license.setter
    def license(self, new_license: str):
        self._license = new_license


def simple_setup(info: VersionInfo, data_files: List[Tuple[str, List[str]]] = [], python_version: str = '>=3.6', excludes: list = []):
    with open('resources/requirements.txt') as fr:
        requirements = [x for x in fr.readlines() if not x.startswith('--extra-index-url')]
        links = [x[18:] for x in fr.readlines() if x.startswith('--extra-index-url')]

    data_files.append(('resources', ['resources/setup.json', 'resources/requirements.txt']))
    setup(
        name=info.name,
        version=info.version,
        author=info.author,
        author_email=info.email,
        description=info.description,
        license=info.license,

        install_requires=requirements,
        python_requires=python_version,
        dependency_links=links,

        packages=find_packages(exclude=excludes),
        data_files=data_files,
        include_package_data=True
    )


simple_setup(VersionInfo.from_json('resources/setup.json'))
