# Makefile for LaTeX UrbanSim journal paper

# Set of all .tex files
TEX = abstract.tex acknowledgements.tex conclusion.tex intro.tex lessons.tex main.tex model-coordinator.tex models.tex object-store.tex overview.tex relatedwork.tex tal.tex title.tex USArchFig.tex
# Set of .eps figures
FIGURES = USDiag1.eps
PPTS = USDiag1.ppt
MISC = 
BIB = urbansim.bib

default: main.dvi

clean:
	rm -f *.aux *.bbl *.dvi main.pdf *.blg *.log

force:
	del main.dvi main.aux
	make default

main.dvi: $(TEX) $(BIB) $(FIGURES) $(MISC)
	latex main
	bibtex main
	latex main
	latex main
	latex main

ps: main.dvi
	dvips -o main.ps main.dvi 

pdf: main.dvi
	dvipdfm -o main.pdf main.dvi

%.zip:
	zip -9 `./getdate.exe`_$*.zip $(FIGURES) $(TEX) $(BIB) $(PPTS) Makefile $(MISC)

zip:
	zip -9 `./getdate.exe`.zip $(FIGURES) ukepaper.tex urbansim.bib $(PPTS) Makefile $(MISC)
