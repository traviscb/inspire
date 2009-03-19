include ../config.mk


CONF = etc/*.pm 
CONFDEST = $(RTDIR)/etc/
RTLOCALDIRS = html lib 

install:
	$(foreach LOCALDIR, $(RTLOCALDIRS), cp -a $(LOCALDIR) $(RTDIR)/local/ && chown -R root:inspire $(RTDIR)/local/$(LOCALDIR);)
	$(INSTALL) -m 664 $(CONF) $(CONFDEST)
	echo "You should look at rt3.conf and consider adding it, with modification, to your /etc/httpd/conf.d directory"
