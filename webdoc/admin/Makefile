# $Id$

include ../../config.mk
-include ../../config-local.mk

ADMINDIR = $(DOCDIR)/admin
DOCFILES = *.webdoc 

all:
	@echo "Done."

test:
	@echo "Nothing to test."

install:
	$(INSTALL) -m 664 $(DOCFILES) $(ADMINDIR)

clean:
	@rm -f *.orig *~

# end of file
