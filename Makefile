clean-pyc:
	find . -name '*.pyc' -delete

clean-build:
	rm -rf build
	rm -rf *.egg-info

clean-virtual-environment:
	rm -rf venv

lint:
	flake8 --exclude=.tox

build-sdist: clean-build
	/usr/bin/env python setup.py sdist

build-wheel: clean-build
	pip install -U wheel
	/usr/bin/env python setup.py bdist_wheel --universal

wheel: build-wheel build-readme

build-rpm: clean-build
	pip install -U wheel
	/usr/bin/env python setup.py bdist --format=rpm

build-readme:
	/usr/bin/env pandoc -s -r markdown -w rst README.md -o README.rst

release: build-wheel build-readme

wheel: build-wheel build-readme

virtual-environment:
	/usr/bin/env python -m virtualenv venv

development-mode: virtual-environment
	venv/bin/pip install -e .

clean: clean-pyc clean-build clean-virtual-environment
