python -m clean

python -m pip install setuptools twine wheel
python setup.py sdist bdist_wheel
twine upload --repository-url https://pypi.org --verbose dist/*