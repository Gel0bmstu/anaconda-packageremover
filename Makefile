TMPDIR := $(shell mktemp -d)
OUTDIR := $(shell pwd)

LOCALEDIR := usr/share/locale
ANACONDADIR := usr/share/anaconda/
ANACONDAADDONSDIR := usr/share/anaconda/addons/
ADDONDIR := org_fedoraproject_package_remove/
SERVICESDIR = $(ANACONDADIR)/dbus/services/
CONFDIR = $(ANACONDADIR)/dbus/confs/

PYTHON?=python3

build:
	@echo "*** Building updates image ***"
	@echo -n "Working..."
	@mkdir -p $(TMPDIR)/$(ANACONDAADDONSDIR)
	@cp -par org_fedoraproject_package_remove $(TMPDIR)/$(ANACONDAADDONSDIR)
	@mkdir -p $(TMPDIR)/$(SERVICESDIR)
	@cp -pa data/org.fedoraproject.Anaconda.Addons.*.service $(TMPDIR)/$(SERVICESDIR)
	@mkdir -p $(TMPDIR)/$(CONFDIR)
	@cp -pa data/org.fedoraproject.Anaconda.Addons.*.conf $(TMPDIR)/$(CONFDIR)
	@mkdir -p $(TMPDIR)/$(LOCALEDIR)
	make -C ./po install DESTDIR=$(TMPDIR)
	@cd $(TMPDIR) ; find . | cpio -c -o --quiet | gzip -9 > $(OUTDIR)/updates.img
	@rm -rf $(TMPDIR)
	@echo "building done."

_default: build
	@cp -u $(OUTDIR)/updates.img ~/addon
	@echo "Success!"

.PHONY: debug
debug: build
	scp updates.img gel0@35.228.159.44:/home/gel0/addon

.PHONY: install
install:
	mkdir -p $(DESTDIR)$(ANACONDAADDONSDIR)
	mkdir -p $(DESTDIR)$(SERVICESDIR)
	mkdir -p $(DESTDIR)$(CONFDIR)
	cp -rv $(ADDONDIR) $(DESTDIR)$(ANACONDAADDONSDIR)
	install -c -m 644 data/*.service $(DESTDIR)$(SERVICESDIR)
	install -c -m 644 data/*.conf $(DESTDIR)$(CONFDIR)

.PHONY: check
check:
	@echo "*** Running pylint ***"
	$(PYTHON) -m pylint org_fedoraproject_package_remove/
# Using git clone of Anaconda will give you import errors. In such case, run the check this way:
# PYTHONPATH=/my/anaconda/git/clone make check
