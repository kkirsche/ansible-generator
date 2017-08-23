clean-pyc:
	find . -name '*.pyc' -delete

clean-build:
	rm -rf build
	rm -rf *.egg-info

clean-virtual-environment:
	rm -rf venv

lint:
	flake8 --exclude=.tox

build-readme:
	/usr/bin/env pandoc -s -r markdown -w rst README.md -o README.rst

build-sdist: clean-build build-readme
	/usr/bin/env python setup.py sdist

build-wheel: clean-build build-readme
	pip install -U wheel
	/usr/bin/env python setup.py bdist_wheel --universal

build-rpm: clean-build build-readme
	pip install -U wheel
	/usr/bin/env python setup.py bdist --format=rpm

release: build-wheel

wheel: build-wheel

virtual-environment:
	/usr/bin/env python -m virtualenv venv

development-mode: virtual-environment
	venv/bin/pip install -e .

clean: clean-pyc clean-build clean-virtual-environment
