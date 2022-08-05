#
# This Makefile serves as convenient command-line auto-completion
#
PROJECT_NAME=joe-pkg-qemu
CONFIGS=src/joe/qemu/configs/qemu.config

define default-help
# invoke: 'make uninstall', 'make install'
endef
.PHONY: default
default: build
	@echo "## py: make default"
	@echo "## py: make default [DONE]"

define  all-help
# Do all: clean uninstall build install
endef
.PHONY: all
all: uninstall clean build install test

define build-help
# Build the package (source distribution package)
endef
.PHONY: build
build:
	@echo "## py: make build-sdist"
	@python3 setup.py sdist
	@echo "## py: make build-sdist [DONE]"

define install-help
# install for current user
endef
.PHONY: install
install:
	@echo "## py: make install"
	@python3 -m pip install dist/*.tar.gz --user
	@echo "## py: make install [DONE]"

define uninstall-help
# uninstall
#
# Prefix with 'sudo' when uninstalling a system-wide installation
endef
.PHONY: uninstall
uninstall:
	@echo "## py: make uninstall"
	@python3 -m pip uninstall ${PROJECT_NAME} --yes || echo "Cannot uninstall => That is OK"
	@echo "## py: make uninstall [DONE]"

define install-system-help
# install system-wide
#
# install system-wide
endef
.PHONY: install-system
install-system:
	@echo "## py: make install-system"
	@python3 -m pip install dist/*.tar.gz
	@echo "## py: make install-system [DONE]"

define examples-help
# Run pytest on the testcase-test
endef
.PHONY: test
test:
	@echo "## py: make test"
	@for config in $(CONFIGS); do python3 -m pytest --pyargs joe.qemu.selftest --config $$config; sleep 1; done
	@echo "## py: make test [DONE]"

define clean-help
# clean the Python build dirs (build, dist)
endef
.PHONY: clean
clean:
	@echo "## py: clean"
	@rm -r cijoe-output-* || echo "Cannot remove => That is OK"
	@rm -r build || echo "Cannot remove => That is OK"
	@rm -r dist || echo "Cannot remove => That is OK"
	@rm -r *.egg-info || echo "Cannot remove => That is OK"
	@echo "## py: clean [DONE]"
