# $Id$

include ../../config.mk
-include ../../config-local.mk

BFTFILES = *.bft
XSLFILES = *.xsl
BFTDIR = $(ETCDIR)/bibformat/format_templates

all:
	@echo "Done."

test:
	@echo "Nothing to test."

install:
	$(INSTALL) -m 664 $(BFTFILES) $(BFTDIR)
	$(INSTALL) -m 664 $(XSLFILES) $(BFTDIR)

clean:
	@rm -f *.orig *~
