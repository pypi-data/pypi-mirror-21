default: test

test: test_only pylint

test_only: env
	.env/bin/py.test -x tests

env: .env/.up-to-date


.env/.up-to-date: setup.py Makefile test_requirements.txt
	python3 -m venv .env
	.env/bin/pip install -e .
	.env/bin/pip install pylint
	.env/bin/pip install -r ./*.egg-info/requires.txt || true
	.env/bin/pip install -r test_requirements.txt
	.env/bin/pip install -r ./doc/pip_requirements.txt
	touch $@

pylint: env
	.env/bin/pylint --rcfile=.pylintrc cob

doc: env
	.env/bin/python setup.py build_sphinx -a -E
