TMPDIR := $(shell mktemp -d)
OUTDIR := $(shell pwd)

BASEDIR := $(TMPDIR)/usr/share/anaconda/
ADDONDIR := $(BASEDIR)/addons/
SERVICESDIR := $(BASEDIR)/dbus/services/
CONFDIR := $(BASEDIR)/dbus/confs/

PYTHON?=python3

build:
	@echo "*** Building updates image ***"
	@echo -n "Working..."
	@mkdir -p $(ADDONDIR)
	@cp -par org_rosa_package_remove $(ADDONDIR)
	@mkdir -p $(SERVICESDIR)
	@cp -pa data/org.rosa.Anaconda.Addons.*.service $(SERVICESDIR)
	@mkdir -p $(CONFDIR)
	@cp -pa data/org.rosa.Anaconda.Addons.*.conf $(CONFDIR)
	@cd $(TMPDIR) ; find . | cpio -c -o --quiet | gzip -9 > $(OUTDIR)/updates.img
	@rm -rf $(TMPDIR)
	@echo "building done."

_default: build
	@cp -u $(OUTDIR)/updates.img ~/addon
	@echo "Success!"

.PHONY: debug
debug: build
	scp updates.img gel0@35.228.159.44:/home/gel0/addon

.PHONY: check
check:
	@echo "*** Running pylint ***"
	$(PYTHON) -m pylint org_rosa_package_remove/
# Using git clone of Anaconda will give you import errors. In such case, run the check this way:
# PYTHONPATH=/my/anaconda/git/clone make check
