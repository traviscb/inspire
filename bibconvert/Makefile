include ../config.mk

LARGE_PATH = /afs/slac/public/groups/library/spires/inspire/test
LARGE_PATTERN = ????_test_set.xml
XSLFILES = SPIRES2MARC.xsl
TEST_TARGETS = test-large-with-xmllint test-large-with-xmlmarclint

# main targets:

all:
	@echo "Done."

test: ${TEST_TARGETS}
	@echo "Done."

clean:
	@rm -f ${LARGE_PATTERN} ${LARGE_PATTERN}.x ${LARGE_PATTERN}.bk ${LARGE_PATTERN}.marcxml

install:
	$(INSTALL) -m 664 $(XSLFILES) $(ETCDIR)/bibconvert/config


load-large-sample-of-records: get-large clean-large split-large convert-large upload-large

# helper targets:

get-large:
	@echo -n "* Copying XML files from AFS space, please be patient..."
	@cp ${LARGE_PATH}/${LARGE_PATTERN} .
	@echo " done."

clean-large: get-large
	@echo "* Removing non-ascii chars in large file, please be patient..."
	@for file in `/bin/ls ${LARGE_PATTERN}`; do \
		perl -i.bk -pe 's/[^[:ascii:]]//g;' $${file} ;\
		cat $${file} | tr -d "\000-\011" | tr -d "\013-\014"| tr -d "\016-\037" > $${file}.x ;\
		mv  $${file}.x $${file} ;\
		done
	@echo "Please see clean-spires-data.sh if your input contains broken tags"
	@echo "* Done.  Please run 'make split-large' now."

convert-large: clean-large
	@echo "* Converting split files, please be patient..."
	@for file in `/bin/ls ${LARGE_PATTERN}`; do \
	   echo " ... converting file $${file}..." ;\
	   $(BINDIR)/bibconvert -c `pwd`/SPIRES2MARC.xsl < $${file} > $${file}.marcxml ;\
	   if [ `md5sum $${file} | cut -f1 -d' '` = `md5sum $${file}.bk | cut -f1 -d' '` ]; \
	     then rm -f $${file}.bk ;\
		 else echo "WARNING: Input and backup files differ; something strange is going on." ;\
	   fi ;\
     done
	@echo "* Done.  Please run 'make test-large-with-xmllint' or 'make test-large-with-xmlmarclint' now."

test-large-with-xmllint: convert-large
	@echo "* Testing XML correctness of converted files, please be patient..."
	@for file in `/bin/ls ${LARGE_PATTERN}`; do \
	    xmllint --noout $${file}; \
     done
	@echo "* Done.  Please run 'make upload-large' now."

############# XXX: HACK: The following output parsing (if clause) would be unnecessary 
#############            if xmlmarclint used shell return codes correctly.
############# was: $(BINDIR)/xmlmarclint $${file}; \

test-large-with-xmlmarclint: convert-large
	@echo "* Testing MARCXML correctness of converted files, please be patient..."
	@for file in `/bin/ls ${LARGE_PATTERN}.marcxml`; do \
	    echo -n $(BINDIR)/xmlmarclint $${file}; \
		if [ -n "`$(BINDIR)/xmlmarclint $${file}`" ] ;\
		  then echo "Removing $${file} because of bad/missing records..."; rm -f $${file} ;\
		  else echo " ...ok." ;\
		fi ;\
     done
	@echo "* Done.  Please run 'make upload-large' now."

upload-large: test-large-with-xmlmarclint
	@echo "* Uploading converted files..."
	@for file in `/bin/ls ${LARGE_PATTERN}.marcxml`; do \
		echo "Uploading from " $${file} "..." ;\
	    $(BINDIR)/bibupload -ir $${file}; \
     done
	@echo "* Done.  Please see via 'bibsched' the task progress."


#################
# Targets below this point have not been verified as correct
SMALL = http://cdsware.cern.ch/download/invenio-demo-site-files/SPIRES_small_sample.xml.gz
SPIRESDIR = ftp://ftp.slac.stanford.edu/groups/library/spires
SPIRESFILES = SPIRES_pre_1975.xml.gz SPIRES_1975_1984.xml.gz SPIRES_1985_1994.xml.gz SPIRES_1995_1999.xml.gz SPIRES_2000_2002.xml.gz SPIRES_2003_2005.xml.gz SPIRES_post_2005.xml.gz

load-small-sample-of-records: get-small convert-small upload-small
load-full-sample-of-records: get-full clean-large split-large convert-large upload

get-small:
	@echo "* Downloading the file please be patient..."
	wget $(SMALL)
	rm -f ./SPIRES_small_sample.xml
	gunzip SPIRES_small_sample.xml.gz

get-full:
	@echo "* Downloading files from SLAC FTP server, please be patient..."
	rm -rf ${SPIRESFILES} large_test.xml
	for i in ${SPIRESFILES}; do wget -nc ${SPIRESDIR}/$${i}; done
	for i in ${SPIRESFILES}; do gunzip -c $${i} >> large_test.xml; done
	#  Please note, bibconvert and xmllint appear to fail on this large file.  
	#  It may be neccessary to use a different xslt engine or break up the 
	#  file.
	@echo "* Done.  Please run 'make split-large' or 'make clean-large' now."

convert-small:
	$(BINDIR)/bibconvert -c `pwd`/SPIRES2MARC.xsl < SPIRES_small_sample.xml > SPIRES_small_sample.marcxml

upload-small:
	@echo "* Uploading converted files..."
	cp SPIRES_small_sample.marcxml /tmp
	chmod a+r /tmp/SPIRES_small_sample.marcxml
	$(BINDIR)/bibupload -ir /tmp/SPIRES_small_sample.marcxml
	@echo "* Done.  Please see via 'bibsched' the task progress."

convert-SPIRES:
	@echo "* Converting split files, please be patient..."
	for file in SPIRES_*.xml_*[0-9]; do \
	   echo " ... converting file $${file}..." ;\
	   $(BINDIR)/bibconvert -c `pwd`/SPIRES2MARC.xsl < $${file} > $${file}.marcxml ;\
        done
	@echo "* Done.  Please run 'make test-large-with-xmllint' or 'make test-large-with-xmlmarclint' now."

test-SPIRES-with-xmllint:
	@echo "* Testing XML correctness of converted files, please be patient..."
	for file in SPIRES_*.xml_*[0-9].marcxml; do \
	    xmllint --noout $${file}; \
        done
	@echo "* Done.  Please run 'make upload-large' now."

test-SPIRES-with-xmlmarclint:
	@echo "* Testing MARCXML correctness of converted files, please be patient..."
	for file in SPIRES_*.xml_*[0-9].marcxml; do \
	    $(BINDIR)/xmlmarclint --noout $${file}; \
        done
	@echo "* Done.  Please run 'make upload-large' now."

upload:
	@echo "* Uploading converted files..."
	for file in SPIRES_*.xml_*[0-9].marcxml; do \
	    $(BINDIR)/bibupload -ir $${file}; \
        done
	@echo "* Done.  Please see via 'bibsched' the task progress."

# end of file
