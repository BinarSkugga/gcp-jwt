python -m clean

python -m pip install setuptools twine wheel
python setup.py sdist bdist_wheel
twine upload --verbose dist/*