include ../config.mk
-include ../config-local.mk


FTP_LOC = ftp://ftp.slac.stanford.edu/groups/library/spires/inspire/

TEST_BASE = hep_test_recs
TEST_URL = ${FTP_LOC}testset/${TEST_BASE}.xml
MARC_URL = ${FTP_LOC}testset/${TEST_BASE}.marcxml

TEST_INST_BASE = inst_test_recs
TEST_INST_URL = ${FTP_LOC}testset/${TEST_INST_BASE}.xml
TEST_INST_MARC_URL = ${FTP_LOC}testset/${TEST_INST_BASE}.marcxml

FULL_INST_BASE = inst_recs
FULL_INST_URL = ${FTP_LOC}inst/${FULL_INST_BASE}.xml
FULL_INST_MARC_URL = ${FTP_LOC}inst/${FULL_INST_BASE}.marcxml

TEST_CONF_BASE = conf_test_recs
TEST_CONF_URL = ${FTP_LOC}testset/${TEST_CONF_BASE}.xml
TEST_CONF_MARC_URL = ${FTP_LOC}testset/${TEST_CONF_BASE}.marcxml

FULL_CONF_BASE = conf_recs
FULL_CONF_URL = ${FTP_LOC}inst/${FULL_CONF_BASE}.xml
FULL_CONF_MARC_URL = ${FTP_LOC}inst/${FULL_CONF_BASE}.marcxml


XSLFILES = SPIRES2MARC.xsl oaiarXiv2inspire.xsl oaiarXiv2inspire_categories.xml inst2marc.xsl conf2marc.xsl
TEST_TARGETS = load-small-sample-of-records

# main targets:

all:
	@echo "Done."

test: ${TEST_TARGETS}
	@echo "Done."

clean:
	@rm -f ${TEST_BASE}.*xml ${TEST_INST_BASE}.*xml ${FULL_INST_BASE}.*xml ${TEST_CONF_BASE}.*xml ${FULL_CONF_BASE}.*xml

install:
	$(INSTALL) -m 664 $(XSLFILES) $(ETCDIR)/bibconvert/config

convert-test-sample-of-records: get-test convert-test
load-test-sample-of-records: get-test convert-test upload-test

convert-test-sample-of-inst: get-test-inst convert-test-inst
load-test-sample-of-inst: get-test-inst convert-test-inst upload-test-inst

convert-test-sample-of-conf: get-test-conf convert-test-conf
load-test-sample-of-conf: get-test-conf convert-test-conf upload-test-conf



# helper targets:

get-test:
	@echo "* Downloading the file please be patient..."
	rm -f $(TEST_BASE).xml
	wget $(TEST_URL)
	@echo "* Done.  Please run 'make convert-test' now."

get-test-marc:
	@echo "* Downloading the file please be patient..."
	rm -f $(TEST_BASE).marcxml
	wget $(MARC_URL)
	@echo "* Done.  Please run 'make upload-test' now."

clean-test:
	@echo "* Removing non-ascii chars in large file, please be patient..."
	@for file in `/bin/ls ${TEST_BASE}.xml`; do \
		perl -i.bk -pe 's/[^[:ascii:]]//g;' $${file} ;\
		cat $${file} | tr -d "\000-\011" | tr -d "\013-\014"| tr -d "\016-\037" > $${file}.x ;\
		mv  $${file}.x $${file} ;\
		done
	@echo "Please see clean-spires-data.sh if your input contains broken tags"
	@echo "* Done.  Please run 'make convert-test' now."

convert-test:
	@echo -n "* Converting small SPIRES record sample..."
	$(BINDIR)/bibconvert -c `pwd`/SPIRES2MARC.xsl < ${TEST_BASE}.xml > ${TEST_BASE}.marcxml
	@echo -n " done."
	@echo "Please run 'make upload-test' now."

upload-test:
	@echo "* Uploading converted files..."
	cp ${TEST_BASE}.marcxml /tmp
	chmod a+r /tmp/${TEST_BASE}.marcxml
	$(BINDIR)/bibupload -ir /tmp/${TEST_BASE}.marcxml
	@echo "* Done.  Please see via 'bibsched' the task progress."

### Institutions targets

get-test-inst:
	@echo "* Downloading the file please be patient..."
	rm -f $(TEST_INST_BASE).xml
	wget $(TEST_INST_URL)
	@echo "* Done.  Please run 'make convert-test-inst' now."

get-test-inst-marc:
	@echo "* Downloading the file please be patient..."
	rm -f $(TEST_INST_BASE).marcxml
	wget $(TEST_INST_MARC_URL)
	@echo "* Done.  Please run 'make upload-test-inst' now."

convert-test-inst:
	@echo -n "* Converting small INST record sample..."
	$(BINDIR)/bibconvert -c `pwd`/inst2marc.xsl < ${TEST_INST_BASE}.xml > ${TEST_INST_BASE}.marcxml
	@echo -n " done."
	@echo "Please run 'make upload-test-inst' now."

upload-test-inst:
	@echo "* Uploading converted files..."
	cp ${TEST_INST_BASE}.marcxml /tmp
	chmod a+r /tmp/${TEST_INST_BASE}.marcxml
	$(BINDIR)/bibupload -ir /tmp/${TEST_INST_BASE}.marcxml
	@echo "* Done.  Please see via 'bibsched' the task progress."


### Conferences test targets

get-test-conf:
	@echo "* Downloading the file please be patient..."
	rm -f $(TEST_CONF_BASE).xml
	wget $(TEST_CONF_URL)
	@echo "* Done.  Please run 'make convert-test-conf' now."

get-test-conf-marc:
	@echo "* Downloading the file please be patient..."
	rm -f $(TEST_CONF_BASE).marcxml
	wget $(TEST_CONF_MARC_URL)
	@echo "* Done.  Please run 'make upload-test-conf' now."

convert-test-conf:
	@echo -n "* Converting small CONF record sample..."
	$(BINDIR)/bibconvert -c `pwd`/conf2marc.xsl < ${TEST_CONF_BASE}.xml > ${TEST_CONF_BASE}.marcxml
	@echo -n " done."
	@echo "Please run 'make upload-test-conf' now."

upload-test-conf:
	@echo "* Uploading converted files..."
	cp ${TEST_CONF_BASE}.marcxml /tmp
	chmod a+r /tmp/${TEST_CONF_BASE}.marcxml
	$(BINDIR)/bibupload -ir /tmp/${TEST_CONF_BASE}.marcxml
	@echo "* Done.  Please see via 'bibsched' the task progress."

####
## Get the full 9000 record institution set.  Should rarely if ever be used.

get-inst-full:
	@echo "* Downloading the file please be patient..."
	rm -f $(FULL_INST_BASE).xml
	wget $(FULL_INST_URL)
	@echo "* Done.  Please run 'make convert-inst-full' now."

get-inst-marc-full:
	@echo "* Downloading the file please be patient..."
	rm -f $(FULL_INST_BASE).marcxml
	wget $(FULL_INST_MARC_URL)
	@echo "* Done.  Please run 'make upload-inst-full' now."

convert-inst-full:
	@echo -n "* Converting full inst record set..."
	$(BINDIR)/bibconvert -c `pwd`/inst2marc.xsl < ${FULL_INST_BASE}.xml > ${FULL_INST_BASE}.marcxml
	@echo -n " done."
	@echo "Please run 'make upload-inst-full' now."

upload-inst-full:
	@echo "* Uploading converted files..."
	cp ${FULL_INST_BASE}.marcxml /tmp
	chmod a+r /tmp/${FULL_INST_BASE}.marcxml
	$(BINDIR)/bibupload -ir /tmp/${FULL_INST_BASE}.marcxml
	@echo "* Done.  Please see via 'bibsched' the task progress."



####
## Get the full conference set.  Should rarely if ever be used.

get-conf-full:
	@echo "* Downloading the file please be patient..."
	rm -f $(FULL_CONF_BASE).xml
	wget $(FULL_CONF_URL)
	@echo "* Done.  Please run 'make convert-conf-full' now."

get-conf-marc-full:
	@echo "* Downloading the file please be patient..."
	rm -f $(FULL_CONF_BASE).marcxml
	wget $(FULL_CONF_MARC_URL)
	@echo "* Done.  Please run 'make upload-conf-full' now."

convert-conf-full:
	@echo -n "* Converting full conf record set..."
	$(BINDIR)/bibconvert -c `pwd`/conf2marc.xsl < ${FULL_CONF_BASE}.xml > ${FULL_CONF_BASE}.marcxml
	@echo -n " done."
	@echo "Please run 'make upload-conf-full' now."

upload-conf-full:
	@echo "* Uploading converted files..."
	cp ${FULL_CONF_BASE}.marcxml /tmp
	chmod a+r /tmp/${FULL_CONF_BASE}.marcxml
	$(BINDIR)/bibupload -ir /tmp/${FULL_CONF_BASE}.marcxml
	@echo "* Done.  Please see via 'bibsched' the task progress."

# to support historical scripts

get-small: get-test
get-inst: get-test-inst
convert-small: convert-test
convert-inst: convert-test-inst
upload-small: upload-test
upload-inst: upload-test-inst

