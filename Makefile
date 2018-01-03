PROJECT := stsAval
CUR_DIR = $(shell pwd)
PYTHON_VERSION := python3
PYTHON3_PATH := $(shell which $(PYTHON_VERSION))
GIT := $(shell which git)
VENV_DIR := $(CUR_DIR)/p3_venv
PIP_CALL := $(VENV_DIR)/bin/pip
MAKE = $(shell which make)
MODULE_PATH := $(CUR_DIR)/$(PROJECT)
SCRIPTS := $(CUR_DIR)/scripts
DOC_PATH := $(CUR_DIR)/docs
REQUIREMENT = $(CUR_DIR)/requirements.txt
VERSION_FILE = $(CUR_DIR)/$(PROJECT)/_version.py


fresh-install: clean setup-venv install
fresh-test-install: clean setup-venv test-install
deploy-test: clean testpypi
deploy-prod: clean pypi


.PHONY: pre-build setup-venv build testpypi pypi test-install install


pre-build:
	rm -rf $(CUR_DIR)/dist
	mkdir $(CUR_DIR)/dist

setup-venv:
	$(PYTHON3_PATH) -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && $(PIP_CALL) install -U setuptools pip && \
	$(PIP_CALL) install -r $(REQUIREMENT)

test: setup_venv
	@$(VENV_DIR)/bin/pip install pytest pytest-pylint coverage
	@$(VENV_DIR)/bin/py.test $(MODULE_PATH)

docs:  setup-venv
	. $(VENV_DIR)/bin/activate && \
	$(PIP_CALL) install sphinx sphinx_rtd_theme autodoc
	#cd $(CUR_DIR) && $(MAKE) clean-docs
	cd $(DOC_PATH) && . $(VENV_DIR)/bin/activate && $(MAKE) html

build: pre-build setup-venv
	sh $(SCRIPTS)/version_update.sh && . $(VENV_DIR)/bin/activate && \
	cd $(CUR_DIR) && $(PYTHON3_PATH) setup.py sdist

testpypi: build
	@echo "Deploy $(PROJECT) to test.pypi.org"
	. $(VENV_DIR)/bin/activate && twine upload --repository testpypi dist/*

pypi: clean build
	@echo "Deploy $(PROJECT) to pypi.org"
	. $(VENV_DIR)/bin/activate && twine upload --repository pypi dist/*

test-install:
	cd $(CUR_DIR) && . $(VENV_DIR)/bin/activate && \
	$(PIP_CALL) install -U $(PROJECT) --extra-index-url https://test.pypi.org/simple/

install:
	cd $(CUR_DIR) && . $(VENV_DIR)/bin/activate && \
	$(PIP_CALL) install -U $(PROJECT)

.PHONY: clean clean-docs

clean-docs:
	@echo "Clean docs build"
	. $(VENV_DIR)/bin/activate && \
	cd $(DOC_PATH) && $(MAKE) clean

clean:
	@echo "Cleanup"
	rm -rf $(VENV_DIR)
	rm -rf $(CUR_DIR)/dist
	rm -rf $(CUR_DIR)/*.egg-info
	rm -f $(CUR_DIR)/README.rst || true
	rm -rf $(CUR_DIR)/$(PROJECT)/__pycache__ || true
