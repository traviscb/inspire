# $Id$

include ../config.mk

XSLFILES = conf2marc.xsl
SPIRESXML = ftp://ftp.slac.stanford.edu/groups/library/spires/conf.xml.gz

all:
	@echo "Done."
test:
	$(BINDIR)/bibconvert -c $(XSLFILES) < test_conf.xml > test_conf.marcxml
	xmllint --format test_conf.marcxml

install:
	$(INSTALL) -m 664 $(XSLFILES) $(ETCDIR)/bibconvert/config

# targets working with big SPIRES dump files follow:

get:
	@echo "* Downloading large file from SLAC FTP server, please be patient..."
	wget $(SPIRESXML)
	rm -f ./conf.xml
	gunzip ./conf.xml.gz
	#  Please note, bibconvert and xmllint appear to fail on this large file.  
	#  It may be neccessary to use a different xslt engine or break up the 
	#  file.
	@echo "* Done.  Please run 'make utf8' now."


utf8:
	@echo "* Changing non-standard characters to UTF8 .."
	mv conf.xml confn.xml
	iconv -fLatin1 -tUTF8 confn.xml > conf.xml
	rm -f confn.xml
	@echo "* Done.  Please run 'make convert' now."

convert:
	@echo "* Converting  files, please be patient..."
	$(BINDIR)/bibconvert -c $(XSLFILES) < conf.xml > conf.marcxml 
	@echo "* Done.  Please run 'make test-with-xmllint' or 'make test-with-xmlmarclint' now."

test-with-xmllint:
	@echo "* Testing XML correctness of converted files, please be patient..."
	xmllint --noout conf.marcxml
	@echo "* Done.  Please run 'make upload' now."

test-with-xmlmarclint:
	@echo "* Testing MARCXML correctness of converted files, please be patient..."
	$(BINDIR)/xmlmarclint conf.marcxml
	@echo "* Done.  Please run 'make upload' now."

upload:
	@echo "* Uploading converted files..."
	$(BINDIR)/bibupload -ir conf.marcxml
	@echo "* Done.  Please see via 'bibsched' the task progress."

# end of file
