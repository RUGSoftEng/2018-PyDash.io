#!/bin/bash

pdflatex changelog_architectural.tex
pandoc ArchitecturalDesign.tex -o ArchitecturalDesign.pdf -V geometry:margin=1in
