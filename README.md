# schoollib
Python-based school book library software

## Requirements

Note that the current version is only tested on Linux-based systems. Especially the test suite (at least at the moment) won't function on Windows-based Systems.

### Running the System

Required Python Modules (e.g. through `pip`)
* pony
* bottle
* PyPDF2
* latex
(might need `pip install six --upgrade`)

Also a LaTeX-installation is required including
* Requires eurosym package (ubuntu: texlive-fonts-recommended)
* Requires makecell package (ubuntu: texlive-latex-extra)
* Requires german babel package (buntu: texlive-lang-german)

### Running the Test Suite

Required Python Modules (e.g. through `pip`)
* webtest
