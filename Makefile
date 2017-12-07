CUR_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
REQUIREMENTS := $(CUR_DIR)/requirements.txt
MODULE_PATH := $(CUR_DIR)/stsAval
DOC_PATH := $(CUR_DIR)/doc

PYTHON3_PATH := $(shell which python3)
PYTHON3_DIR := $(shell dirname $(PYTHON3_PATH))
VENV_DIR := $(CUR_DIR)/p3_venv

all: test doc

setup_venv:
	@echo "Setting up virtualenv"
	$(PYTHON3_PATH) -m venv $(VENV_DIR)
	sh $(VENV_DIR)/bin/activate
	$(VENV_DIR)/bin/pip install -r $(REQUIREMENTS)

test: setup_venv
	@$(VENV_DIR)/bin/pip install pytest pytest-pylint coverage
	@$(VENV_DIR)/bin/py.test $(MODULE_PATH)
	# @$(VENV_DIR)/bin/coverage $(MODULE_PATH)

doc: setup_venv
	@$(VENV_DIR)/bin/pip install sphinx sphinx_rtd_theme
	@$(VENV_DIR)/bin/sphinx-apidoc -o $(DOC_PATH) $(MODULE_PATH) -e -f
	cd $(DOC_PATH) && $(MAKE) html

clean:
	@echo "Cleanup"
	rm -rf $(VENV_DIR)
	rm -rf $(CUR_DIR)/dist
