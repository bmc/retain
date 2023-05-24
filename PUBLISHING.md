# Publishing to PyPI

(Notes to self...)

Adapted from <https://realpython.com/pypi-publish-python-package/>

Python 3 only (from version 2.0.0 forward):

```
$ pip install twine
$ pip install 'readme_renderer[md]'
$ python setup.py sdist bdist_wheel
$ twine check dist/*
$ twine upload dist/*
```
