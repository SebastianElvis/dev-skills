LATEXMK ?= latexmk
PDF2SVG ?= $(shell command -v pdf2svg)
PDFTOCAIRO ?= pdftocairo
SVGO ?= $(shell command -v svgo)

SOURCE ?= system-architecture.tex
PDF := $(SOURCE:.tex=.pdf)
SVG := $(SOURCE:.tex=.svg)

.PHONY: all clean
.DELETE_ON_ERROR:

all: $(PDF) $(SVG)

$(PDF): $(SOURCE)
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error $(SOURCE)

$(SVG): $(PDF)
	$(if $(PDF2SVG),$(PDF2SVG) $(PDF) $(SVG),$(PDFTOCAIRO) -svg $(PDF) $(SVG))
	$(if $(SVGO),$(SVGO) --multipass $(SVG))

clean:
	$(LATEXMK) -c $(SOURCE)
