include config.mk

SUBDIRS = bibconvert bibformat webstyle kbs bibrank conf editor

all:
	$(foreach SUBDIR, $(SUBDIRS), cd $(SUBDIR) && make all && cd .. ;)
	@echo "Done.  Please run make test now."

test:
	$(foreach SUBDIR, $(SUBDIRS), cd $(SUBDIR) && make test && cd .. ;)
	@echo "Done.  Please run make install now."

reset-inspire-test-site-field-configuration:
	echo "UPDATE tag SET value='773__%' WHERE name='journal'" | $(BINDIR)/dbexec
	echo "UPDATE tag SET value='260__c' WHERE name='year'" | $(BINDIR)/dbexec
	echo "UPDATE tag SET value='693__e' WHERE name='experiment'" | $(BINDIR)/dbexec
	echo "REPLACE INTO field VALUES (50, 'collaboration', 'collaboration')" | $(BINDIR)/dbexec
	echo "REPLACE INTO tag VALUES (200, 'collaboration', '710__g')" | $(BINDIR)/dbexec
	echo "REPLACE INTO field_tag VALUES (50, 200, 100)" | $(BINDIR)/dbexec

install: reset-inspire-test-site-field-configuration reset-inspire-test-site-collection-configuration
	$(foreach SUBDIR, $(SUBDIRS), cd $(SUBDIR) && make install && cd .. ;)
	@echo "Done.  You may want to copy $(ETCDIR)/invenio-local.conf-example to $(ETCDIR)/invenio-local.conf, edit commented parts, run inveniocfg --update-all --reset-all and restart Apache now."

reset-inspire-test-site-collection-configuration:
	echo "TRUNCATE collection" | $(BINDIR)/dbexec
	echo "TRUNCATE collectionname" | $(BINDIR)/dbexec
	echo "TRUNCATE collection_collection" | $(BINDIR)/dbexec
	echo "TRUNCATE collection_portalbox" | $(BINDIR)/dbexec
	echo "TRUNCATE collection_rnkMETHOD" | $(BINDIR)/dbexec
	echo "INSERT INTO collection VALUES (1, 'INSPIRE', NULL, 0, NULL, NULL)" | $(BINDIR)/dbexec
	echo "INSERT INTO collection VALUES (2, 'HEP','970__a:\'SPIRES\'', 0, NULL, NULL)" | $(BINDIR)/dbexec
	echo "INSERT INTO collection VALUES (3,'Institutions','980__a:"INSTITUTIONS"', 0, NULL, NULL)" | $(BINDIR)/dbexec
	echo "INSERT INTO collection VALUES (4, 'Conferences','980__a:"CONFERENCES"', 0, NULL, NULL)" | $(BINDIR)/dbexec
#	echo "INSERT INTO collection VALUES (5,'HEPNames','980__a:"AUTHORS"', 0, NULL, NULL)" | $(BINDIR)/dbexec

	echo "INSERT INTO collection_collection VALUES (1 , 2, 'r', 4)"|$(BINDIR)/dbexec
	echo "INSERT INTO collection_collection VALUES (1 , 3, 'r', 2)"|$(BINDIR)/dbexec
	echo "INSERT INTO collection_collection VALUES (1 , 4, 'r', 1)"|$(BINDIR)/dbexec
#	echo "INSERT INTO collection_collection VALUES (1 , 5, 'r', 3)"|$(BINDIR)/dbexec
	echo "INSERT INTO collection_rnkMETHOD VALUES (1, 1, 200)" | $(BINDIR)/dbexec
	echo "INSERT INTO collection_rnkMETHOD VALUES (1, 3, 100)" | $(BINDIR)/dbexec
	echo "INSERT INTO collectionname VALUES (1, 'en', 'ln', 'INSPIRE')" | $(BINDIR)/dbexec
	echo "INSERT INTO collectionname VALUES (1, 'fr', 'ln', 'INSPIRE')" |$(BINDIR)/dbexec
	echo "INSERT INTO collectionname VALUES (2, 'en', 'ln', 'HEP')" | $(BINDIR)/dbexec
	echo "INSERT INTO collectionname VALUES (2, 'fr', 'ln', 'HEP')" | $(BINDIR)/dbexec
	echo "INSERT INTO collectionname VALUES (4, 'fr', 'ln', 'Les Conf�rences')" | $(BINDIR)/dbexec
	echo "INSERT INTO collectionname VALUES (3, 'fr', 'ln', 'Les Institutions')" | $(BINDIR)/dbexec
	echo "DELETE FROM collection_externalcollection WHERE id_collection >= 2" | $(BINDIR)/dbexec
	echo "UPDATE collection_externalcollection SET type=1 WHERE type=2" | $(BINDIR)/dbexec

	$(BINDIR)/webcoll -u admin
	@echo "Please run the webcoll task just submitted, if your bibsched daemon is not in an automatic mode."

load-inspire-test-site-records:
	(cd bibconvert && make)
	$(BINDIR)/bibupload -ir bibconvert/test_record_spires_converted.xml

load-all-inspire-test-site-records:
	(cd bibconvert && make)
	$(BINDIR)/bibupload -ir bibconvert/inspire_set_converted.xml

load-large-inspire-test-site-records:
	(cd bibconvert && make)
	$(BINDIR)/bibupload -ir bibconvert/large_converted.xml

load-knowledge-base:
	cd kbs && make && cd ..

load-small-sample-of-records:
	(cd bibconvert && make load-small-sample-of-records)

load-large-sample-of-records:
	(cd bibconvert && make load-large-sample-of-records)

load-full-sample-of-records:
	(cd bibconvert && make load-full-sample-of-records)
