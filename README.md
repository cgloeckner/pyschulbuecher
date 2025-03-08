# pyschulbuecher
Python-basierte Software zur Schulbuchverwaltung in Schulen.

## Bemerkungen

Aktuell handelt es sich hierbei um eine unveröffentlichte Software, die für dein Einsatz auf Linux-Systemen konzipiert ist. Eine zukünftige Unterstützung anderer Systeme ist bislang nicht geplant.

## Voraussetzungen

erforderliche: Python-Module (z.B. via `pip`)
* `pony` (Datenbank)
* `bottle` (Webserver)
* `PyPDF2` (PDF-Erstellung)
* `latex` (PDF-Erstellung)
* `xlsxwriter` (XLSX-Erstellung)
(evtl. `pip install six --upgrade`)

Folgende LaTeX-Pakete werden außerdem vorausgesetzt:
* eurosym package (ubuntu: texlive-fonts-recommended)
* makecell package (ubuntu: texlive-latex-extra)
* german babel package (buntu: texlive-lang-german)

Alternativ zu einem lokalen LaTeX-Compiler kann in der `settings.yaml` der [latex-online Compiler von Andrey Lushnikov](https://github.com/aslushnikov/latex-online) konfiguriert werden:
```
hosting:
  remote_latex: 'https://compiler.my-server.de:2700'
```
Der Compiler sollte DSGVO-konform gehostet werden, da die zu erstellen PDFs teilweise personenbezogene Daten beeinhalten können.

### Notizen

Convert XLSX to single PDF
```soffice --headless --convert-to pdf *.xlsx
pdfunite *.pdf out.pdf
```



