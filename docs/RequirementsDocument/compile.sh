#!/bin/bash

pdflatex changelog_requirements.tex
pandoc RequirementsDocument.tex -o RequirementsDocument.pdf -V geometry:margin=1in
