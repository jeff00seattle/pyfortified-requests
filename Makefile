#   Makefile
#
# license   http://opensource.org/licenses/MIT The MIT License (MIT)
#

.PHONY: clean version build dist local-dev yapf pyflakes pylint

PACKAGE := requests-fortified
PACKAGE_PREFIX := requests_fortified

PYTHON3 := $(shell which python3)

PY_MODULES := pip setuptools pylint flake8 pprintpp pep8 requests six sphinx wheel python-dateutil

PACKAGE_SUFFIX := py3-none-any.whl
PACKAGE_WILDCARD := $(PACKAGE)-*
PACKAGE_PREFIX_WILDCARD := $(PACKAGE_PREFIX)-*
PACKAGE_PATTERN := $(PACKAGE_PREFIX)-*-$(PACKAGE_SUFFIX)

VERSION := $(shell $(PYTHON3) setup.py version)
WHEEL_ARCHIVE := dist/$(PACKAGE_PREFIX)-$(VERSION)-$(PACKAGE_SUFFIX)

PACKAGE_FILES := $(shell find $(PACKAGE_PREFIX) examples ! -name '__init__.py' -type f -name "*.py")
PACKAGE_ALL_FILES := $(shell find $(PACKAGE_PREFIX) tests examples -type f -name "*.py")
PACKAGE_EXAMPLE_FILES := $(shell find examples ! -name '__init__.py' -type f -name "*.py")
PYFLAKES_ALL_FILES := $(shell find $(PACKAGE_PREFIX) tests examples -type f  -name '*.py' ! '(' -name '__init__.py' ')')

REQ_FILE := requirements.txt
TOOLS_REQ_FILE := requirements-tools.txt
SETUP_FILE := setup.py
ALL_FILES := $(PACKAGE_FILES) $(REQ_FILE) $(SETUP_FILE)

# Report the current package version.
version:
	@echo "======================================================"
	@echo version $(PACKAGE)
	@echo "======================================================"
	@echo $(REQUESTS_MV_INTGS_PKG) $(VERSION)

clean:
	@echo "======================================================"
	@echo clean $(PACKAGE)
	@echo "======================================================"
	rm -fR htmlcov
	rm -fR __pycache__ venv "*.pyc" build/*    \
		$(PACKAGE_PREFIX)/__pycache__/         \
		$(PACKAGE_PREFIX)/helpers/__pycache__/ \
		$(PACKAGE_PREFIX).egg-info/*
	find ./* -maxdepth 0 -name "*.pyc" -type f -delete
	find $(PACKAGE_PREFIX) -name "*.pyc" -type f -delete
	@echo "======================================================"
	@echo delete distributions: $(PACKAGE)
	@echo "======================================================"
	mkdir -p ./dist/
	find ./dist/ -name $(PACKAGE_WILDCARD) -exec rm -vf {} \;
	find ./dist/ -name $(PACKAGE_PREFIX_WILDCARD) -exec rm -vf {} \;

uninstall-package: clean
	@echo "======================================================"
	@echo uninstall-package $(PACKAGE)
	@echo "======================================================"
	$(PYTHON3) -m pip install --upgrade list
	@if $(PYTHON3) -m pip list | grep -F $(PACKAGE) > /dev/null; then \
		echo "python package $(PACKAGE) Found"; \
		$(PYTHON3) -m pip uninstall --yes $(PACKAGE); \
		echo "uninstall package $(PACKAGE)"; \
	else \
		echo "python package $(PACKAGE) Not Found"; \
	fi

site-packages:
	@echo "======================================================"
	@echo site-packages
	@echo "======================================================"
	$(eval PYTHON3_SITE_PACKAGES := $(shell python3 -c "import site; print(site.getsitepackages()[0])"))
	@echo $(PYTHON3_SITE_PACKAGES)

remove-package: uninstall-package site-packages
	@echo "======================================================"
	@echo remove-package $(PACKAGE_PREFIX)
	@echo "======================================================"
	rm -fR $(PYTHON3_SITE_PACKAGES)/$(PACKAGE_PREFIX)*

install: remove-package
	@echo "======================================================"
	@echo install $(PACKAGE)
	@echo "======================================================"
	$(PYTHON3) -m pip install --upgrade pip
	$(PYTHON3) -m pip install --upgrade $(WHEEL_ARCHIVE)
	$(PYTHON3) -m pip freeze | grep $(PACKAGE)

install-dist:
	@echo "======================================================"
	@echo install-dist $(PACKAGE)
	@echo "======================================================"
	$(PYTHON3) -m pip install --upgrade $(WHEEL_ARCHIVE)
	$(PYTHON3) -m pip freeze | grep $(PACKAGE)

freeze:
	@echo "======================================================"
	@echo freeze $(PACKAGE)
	@echo "======================================================"
	$(PYTHON3) -m pip install --upgrade freeze
	$(PYTHON3) -m pip freeze | grep $(PACKAGE)

fresh: dist dist-update install
	@echo "======================================================"
	@echo fresh completed $(PACKAGE)
	@echo "======================================================"

# Register the module with PyPi.
register:
	$(PYTHON3) $(SETUP_FILE) register

local-dev: requirements remove-package
	@echo "======================================================"
	@echo local-dev $(PACKAGE)
	@echo "======================================================"
	$(PYTHON3) -m pip install --upgrade freeze
	$(PYTHON3) -m pip install --upgrade .
	@echo "======================================================"
	$(PYTHON3) -m pip freeze | grep $(PACKAGE)
	@echo "======================================================"

local-dev-no-install:
	@echo "======================================================"
	@echo local-dev-no-install $(PACKAGE)
	@echo "======================================================"
	$(PYTHON3) -m pip install --upgrade freeze
	$(PYTHON3) -m pip install --upgrade .
	@echo "======================================================"
	$(PYTHON3) -m pip freeze | grep $(PACKAGE)
	@echo "======================================================"

dist: clean
	@echo "======================================================"
	@echo dist $(PACKAGE)
	@echo "======================================================"
	$(PYTHON3) -m pip install --upgrade -r requirements.txt
	$(PYTHON3) $(SETUP_FILE) sdist bdist_wheel install upload
	@echo "======================================================"
	ls -al ./dist/$(PACKAGE_PREFIX_WILDCARD)
	@echo "======================================================"

build: clean
	@echo "======================================================"
	@echo remove $(PACKAGE_PREFIX_WILDCARD) and $(PACKAGE_WILDCARD)
	@echo "======================================================"
	mkdir -p ./dist/
	find ./dist/ -name $(PACKAGE_WILDCARD) -exec rm -vf {} \;
	find ./dist/ -name $(PACKAGE_PREFIX_WILDCARD) -exec rm -vf {} \;
	@echo "======================================================"
	@echo build $(PACKAGE)
	@echo "======================================================"
	$(PYTHON3) -m pip install --upgrade -r requirements.txt
	$(PYTHON3) $(SETUP_FILE) clean
	$(PYTHON3) $(SETUP_FILE) bdist_wheel
	$(PYTHON3) $(SETUP_FILE) sdist
	$(PYTHON3) $(SETUP_FILE) build
	$(PYTHON3) $(SETUP_FILE) install
	@echo "======================================================"
	ls -al ./dist/$(PACKAGE_PREFIX_WILDCARD)
	@echo "======================================================"

requirements: $(REQ_FILE)
	@echo "======================================================"
	@echo requirements
	@echo "======================================================"
	$(PYTHON3) -m pip install --upgrade -r $(REQ_FILE)

tools-requirements: $(TOOLS_REQ_FILE)
	@echo "======================================================"
	@echo tools-requirements
	@echo "======================================================"
	$(PYTHON3) -m pip install --upgrade -r $(TOOLS_REQ_FILE)

pep8: tools-requirements
	@echo "======================================================"
	@echo pep8 $(PACKAGE)
	@echo "======================================================"
	$(PYTHON3) -m pep8 --config .pep8 $(PACKAGE_ALL_FILES)

pyflakes: tools-requirements
	@echo "======================================================"
	@echo pyflakes $(PACKAGE)
	@echo "======================================================"
	$(PYTHON3) -m pip install --upgrade pyflakes
	$(PYTHON3) -m pyflakes $(PYFLAKES_ALL_FILES)

pylint: tools-requirements
	@echo "======================================================"
	@echo pylint $(PACKAGE)
	@echo "======================================================"
	$(PYTHON3) -m pip install --upgrade pylint
	$(PYTHON3) -m pylint --rcfile .pylintrc $(PACKAGE_ALL_FILES) --disable=C0330,F0401,E0611,E0602,R0903,C0103,E1121,R0913,R0902,R0914,R0912,W1202,R0915,C0302 | more -30

yapf: tools-requirements
	@echo "======================================================"
	@echo yapf $(PACKAGE)
	@echo "======================================================"
	$(PYTHON3) -m yapf --style .style.yapf --in-place $(PACKAGE_ALL_FILES)

lint: tools-requirements
	@echo "======================================================"
	@echo lint $(PACKAGE)
	@echo "======================================================"
	pylint --rcfile .pylintrc $(REQUESTS_MV_INTGS_FILES) | more

flake8:
	@echo "======================================================"
	@echo flake8 $(PACKAGE)
	@echo "======================================================"
	flake8 --ignore=F401,E265,E129 $(PACKAGE_PREFIX)

list-package: site-packages
	@echo "======================================================"
	@echo list-packages $(PACKAGE)
	@echo "======================================================"
	ls -al $(PYTHON3_SITE_PACKAGES)/$(PACKAGE_PREFIX)*

run-examples: requirements
	@echo "======================================================"
	@echo run-examples $(PACKAGE)
	@echo "======================================================"
	rm -fR _tmp/*.json
	@echo "======================================================"
	@$(PYTHON3) examples/example_requests_countries.py
	@echo "======================================================"
	@$(PYTHON3) examples/example_requests_countries_stdout_color.py
	@echo "======================================================"

coverage-percent:
	py.test --verbose --cov=requests_fortified tests

list:
	cat Makefile | grep "^[a-z]" | awk '{print $$1}' | sed "s/://g" | sort