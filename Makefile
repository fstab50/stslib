PROJECT := stsAval
PYTHON_VERSION := python3
PYTHON3_PATH := $(shell which $(PYTHON_VERSION))
CUR_DIR = $(shell pwd)
VENV_DIR := $(CUR_DIR)/p3_venv
PIP_CALL := $(VENV_DIR)/bin/pip
MODULE_PATH := $(CUR_DIR)/$(PROJECT)
SCRIPTS := $(CUR_DIR)/scripts
DOC_PATH := $(CUR_DIR)/doc
REQUIREMENT = $(PROJECT)/requirements.txt


pre-build:
	rm -rf $(CUR_DIR)/dist
	mkdir $(CUR_DIR)/dist

setup-venv:
	$(PYTHON3_PATH) -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && $(PIP_CALL) install -U setuptools pip && \
	$(PIP_CALL) install -r $(CUR_DIR)/requirements.txt || true

test: setup_venv
	@$(VENV_DIR)/bin/pip install pytest pytest-pylint coverage
	@$(VENV_DIR)/bin/py.test $(MODULE_PATH)

docs:  setup-venv
	@$(VENV_DIR)/bin/pip install sphinx sphinx_rtd_theme
	sphinx-apidoc -o $(DOC_PATH) $(MODULE_PATH) -e -f
	cd $(DOC_PATH) && $(MAKE) html SPHINXBUILD="$(PYTHON3_PATH) -msphinx"

build: pre-build setup-venv
	cd $(CUR_DIR) && \
	pandoc --from=markdown --to=rst --output=README.rst README.md
	$(PYTHON3_PATH) setup.py sdist

testpypi: build
	sh $(SCRIPTS)/version_update.sh && \
	. $(VENV_DIR)/bin/activate && twine upload --repository testpypi dist/*

pypi: build
	sh $(SCRIPTS)/version_update.sh && \
	. $(VENV_DIR)/bin/activate && twine upload --repository pypi dist/*

install: clean setup-venv
	cd $(CUR_DIR) && . $(VENV_DIR)/bin/activate && \
	$(PIP_CALL) install -U $(PROJECT) --extra-index-url https://test.pypi.org/simple/

.PHONY: clean

clean:
	@echo "Cleanup"
	rm -rf $(VENV_DIR)
	rm -rf $(CUR_DIR)/dist
	rm -rf $(CUR_DIR)/*.egg-info
	rm -rf $(CUR_DIR)/README.rst || true
