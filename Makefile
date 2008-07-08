# Hierarchy under which Jabbim can expect to be installed.
# Can be changed on the command line, eg.:
#   make PREFIX=/usr
PREFIX = /usr/local

# But you'd better leave these alone
bindir := $(PREFIX)/bin
datadir := $(PREFIX)/share
jabbimdata := $(datadir)/jabbim

# Builds generated files
ts_files := $(shell find . -name '*.ts')
qm_files := $(ts_files:.ts=.qm)
build: $(qm_files) jabbim .configured-prefix

.configured-prefix: jabbim
	echo $(PREFIX) > .configured-prefix

# Fills in the template for the starting script
jabbim: jabbim.in
	sed -e "s|@JABBIMDATA@|$(jabbimdata)|g" $< > $@

%.qm: %.ts
	lrelease-qt4 -compress $< -qm $@


# Installs Jabbim into the system.
# DESTDIR is mainly useful for packagers.
# This variable can be overridden on the command line, eg.:
#    make install DESTDIR=/var/tmp/buildroot
DESTDIR =
configured_prefix = $(shell cat .configured-prefix)
.PHONY: install
install: build
	@echo "configured prefix is $(configured_prefix)"
	@echo "bindir is $(bindir)"
	@echo "datadir is $(datadir)"
	@echo "jabbimdata is $(jabbimdata)"
	@[ -n "$(DESTDIR)" ] && echo "DESTDIR is $(DESTDIR)" ||:
	python install-files.py -v -b installation-blacklist . "$(DESTDIR)$(jabbimdata)"
	@#cp -dR --preserve=mode,timestamps,context,links . "$(DESTDIR)$(jabbimdata)"
	install -D -p -m 755 jabbim "$(DESTDIR)$(bindir)/jabbim"
	install -D -p -m 644 jabbim.desktop "$(DESTDIR)$(datadir)/applications/jabbim.desktop"
	for i in 16 22 32 48 ; do \
        	d="$(DESTDIR)$(datadir)/icons/hicolor/$${i}x$${i}/apps" ;\
        	install -D -m 644 -p images/$${i}x$${i}/apps/jabbim.png "$$d/jabbim.png" ;\
	done
	d="$(DESTDIR)$(datadir)/icons/hicolor/scalable/apps" ;\
	install -D -m 644 -p images/scalable/apps/jabbim.svg "$$d/jabbim.svg"
	install -dm 755 $(DESTDIR)$(datadir)/pixmaps
	pushd $(DESTDIR)$(datadir)/pixmaps ;\
	ln -sf ../icons/hicolor/48x48/apps/jabbim.png . ;\
	ln -sf ../icons/hicolor/scalable/apps/jabbim.svg . ;\
	popd
	@echo Jabbim has been installed.


# Removes generated files
.PHONY: clean
clean:
	find . \( -name '*.py[co]' -o -name '*.qm' \) -print0 | xargs -0 --no-run-if-empty rm
	rm -f jabbim .configured-prefix
