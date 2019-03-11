clean-pyc:
	find . -name '*.pyc' -delete

clean-build:
	rm -rf build
	rm -rf *.egg-info

clean-virtual-environment:
	rm -rf venv

lint:
	/usr/bin/env flake8 --exclude=.tox

build-sdist: clean-build
	/usr/bin/env python3 setup.py sdist

build-wheel: clean-build
	/usr/bin/env python3 -m pip install -U wheel
	/usr/bin/env python3 setup.py bdist_wheel --universal

build-rpm: clean-build
	/usr/bin/env python3 -m pip install -U wheel
	/usr/bin/env python3 setup.py bdist --format=rpm

release: build-wheel

wheel: build-wheel

virtual-environment:
	/usr/bin/env python3 -m virtualenv venv

development-mode: virtual-environment
	venv/bin/python3 -m pip install -e .

clean: clean-pyc clean-build clean-virtual-environment
