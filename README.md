# pyschulbuecher
Python-basierte Software zur Schulbuchverwaltung in Schulen.

## Bemerkungen

Aktuell handelt es sich hierbei um eine in Entwicklung befindliche Software, die für dein Einsatz auf Linux-Systemen konzipiert ist. Eine zukünftige Unterstützung anderer Systeme ist bislang nicht geplant.

## Voraussetzungen

siehe `requirements.txt`

Folgende LaTeX-Pakete werden außerdem vorausgesetzt:
* eurosym package (ubuntu: texlive-fonts-recommended)
* makecell package (ubuntu: texlive-latex-extra)
* german babel package (buntu: texlive-lang-german)

### Notizen

Convert XLSX to single PDF
```soffice --headless --convert-to pdf *.xlsx
pdfunite *.pdf out.pdf
```



