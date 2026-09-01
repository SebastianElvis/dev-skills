LATEXMK ?= latexmk
PDFTOCAIRO ?= pdftocairo

SOURCE ?= system-architecture.tex
PDF := $(SOURCE:.tex=.pdf)
SVG := $(SOURCE:.tex=.svg)

.PHONY: all clean
.DELETE_ON_ERROR:

all: $(PDF) $(SVG)

$(PDF): $(SOURCE)
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error $(SOURCE)

$(SVG): $(PDF)
	$(PDFTOCAIRO) -svg $(PDF) $(SVG)

clean:
	$(LATEXMK) -c $(SOURCE)
