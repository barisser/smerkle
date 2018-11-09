build:
	virtualenv --python python3.6 venv && pip install -e . && . venv/bin/activate && python setup.py install

clean:
	rm -rf venv && rm -rf build && rm -rf dist && rm -rf *.egg-info

test:
	export PYTHONPATH=.; py.test tests -vvv --cov smerkle --cov-report=term-missing

lint:
	pylint --rcfile=.pylintrc smerkle

errors_only_lint:
	pylint --rcfile=.pylintrc --disable=c,w,r src
