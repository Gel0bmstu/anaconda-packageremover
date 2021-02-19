INSTALL		 = /usr/bin/install
INSTALL_DATA = $(INSTALL) -m 644
INSTALL_DIR	 = $(INSTALL) -d

# destination directory
NLSPACKAGE		= anaconda-packageremover
INSTALL_NLS_DIR = $(DESTDIR)/usr/share/locale
MSGFMT			= msgfmt --statistics --verbose

# What do we need to do
POFILES	= $(wildcard ./*.po)
MOFILES	= $(patsubst %.po,%.mo,$(POFILES))

all: $(MOFILES)

install: $(MOFILES)
	@for n in $(MOFILES); do \
	    l=`basename $$n .mo`; \
	    $(INSTALL_DIR) $(INSTALL_NLS_DIR)/$$l/LC_MESSAGES; \
	    $(INSTALL_DATA) --verbose $$n $(INSTALL_NLS_DIR)/$$l/LC_MESSAGES/$(NLSPACKAGE).mo; \
	done

%.mo: %.po
	$(MSGFMT) -o $@ $<
