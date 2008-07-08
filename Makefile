# Builds generated files
ts_files := $(shell find . -name '*.ts')
qm_files := $(ts_files:.ts=.qm)
build: $(qm_files)

%.qm: %.ts
	lrelease-qt4 -compress $< -qm $@

# Removes generated files
.PHONY: clean
clean:
	find . \( -name '*.py[co]' -o -name '*.qm' \) -print0 | xargs -0 --no-run-if-empty rm
