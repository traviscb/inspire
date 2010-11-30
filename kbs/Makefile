include ../config.mk
-include ../config-local.mk

WEBDESC='Mapping of SPIRES abbreviations for URLs to Displayable names'
OADESC='Journals that are fully OA'
PWD=`pwd`

all:
	@echo "Done."

test:
	@echo "Nothing to test."

install-dbchanges:
	@echo "Loading knowledge bases into DB..."
	make delete-weblinks
	make delete-oalinks
	make delete-talktype
	make delete-synomyms
	make load-weblinks-knowledge-base
	make load-weblinks-knowledge-base
	make load-talktype-knowledge-base
	make load-synonyms-knowledge-base
	@echo "Done."

delete-weblinks:
	echo "DELETE FROM knwKBRVAL where id_knwKB=(SELECT id from knwKB where name='WEBLINKS')" | $(BINDIR)/dbexec

delete-oalinks:
	echo "DELETE FROM knwKBRVAL where id_knwKB=(SELECT id from knwKB where name='OALINKS')" | $(BINDIR)/dbexec

delete-talktype:
	echo "DELETE FROM knwKBRVAL where id_knwKB=(SELECT id from knwKB where name='TALKTYPE')" | $(BINDIR)/dbexec

delete-synomyms:
	echo "DELETE FROM knwKBRVAL where id_knwKB=(SELECT id from knwKB where name='SYNONYMS')" | $(BINDIR)/dbexec


load-weblinks-knowledge-base:
	echo "INSERT into knwKB (name, description) VALUES('WEBLINKS',$(WEBDESC)) on duplicate key update description = $(WEBDESC)" | $(BINDIR)/dbexec
	echo " create temporary table templinks like knwKBRVAL;\
LOAD DATA LOCAL INFILE '$(PWD)/weblinks.dat' replace INTO TABLE templinks;\
update templinks set id_knwKB= (select id from knwKB where name='WEBLINKS');\
insert into  knwKBRVAL  (m_key,m_value,id_knwKB) select m_key,m_value,id_knwKB from templinks ;\
"|$(BINDIR)/dbexec

load-oalinks-knowledge-base:
	echo "INSERT into knwKB (name, description) VALUES('OALINKS',$(OADESC)) on duplicate key update description = $(OADESC)" | $(BINDIR)/dbexec
	echo " create temporary table templinks like knwKBRVAL;\
LOAD DATA LOCAL INFILE '$(PWD)/oalinks.dat' replace INTO TABLE templinks;\
update templinks set id_knwKB= (select id from knwKB where name='WEBLINKS');\
insert into  knwKBRVAL  (m_key,m_value,id_knwKB) select m_key,m_value,id_knwKB from templinks ;\
"|$(BINDIR)/dbexec

load-talktype-knowledge-base:
	echo "INSERT into knwKB (name, description) VALUES('TALKTYPE',$(WEBDESC)) on duplicate key update description = $(WEBDESC)" | $(BINDIR)/dbexec
	echo " create temporary table templinks like knwKBRVAL;\
LOAD DATA LOCAL INFILE '$(PWD)/talktype.kba' replace INTO TABLE templinks;\
update templinks set id_knwKB= (select id from knwKB where name='TALKTYPE');\
insert into  knwKBRVAL  (m_key,id_knwKB) select m_key,id_knwKB from templinks ;\
"|$(BINDIR)/dbexec

load-journal-knowledge-base:
	echo "INSERT into knwKB (name, description) VALUES('SYNONYMS',$(JDESC)) on duplicate key update description = $(JDESC)" | $(BINDIR)/dbexec
	echo " create temporary table templinks like knwKBRVAL;\
LOAD DATA LOCAL INFILE '$(PWD)/synonyms.kb' replace INTO TABLE templinks;\
update templinks set id_knwKB= (select id from knwKB where name='SYNONYMS');\
insert into  knwKBRVAL  (m_key,m_value, id_knwKB) select m_key,m_value,id_knwKB from templinks ;\
"|$(BINDIR)/dbexec

clean:
	@rm -f *.orig *~
