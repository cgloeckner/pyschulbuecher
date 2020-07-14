%from utils import tex_escape
%from db import loans
%from utils import shortName

{\LARGE Ausleihliste zur Bücherrückgabe {{class_.toString()}} }
\hfill
%year = int(s.data['general']['school_year'])
{\large Schuljahr {{year}}/{{year+1}} }

%if class_.teacher is not None:
	Klassenleiter(in):
	\quad
	{{class_.teacher.person.name}}, {{class_.teacher.person.firstname}}
%end

Bitte sammeln Sie die untenstehenden Bücher von Ihren Schülern ein. Beachten Sie dabei:
\begin{enumerate}
	\item \textbf{Streichen} Sie alle \textbf{bei Ihnen abgegebenen Bücher} in der Tabelle. Hat ein Schüler \textbf{alle Bücher abgegeben}, so genügt das \textbf{Streichen} der gesamten Ausleih\textbf{zeile}.
	\item \textbf{Ersatzexemplare} müssen \textbf{unbedingt} auf \textbf{einem separaten Stapel} bei mir abgegeben werden.
%if class_.grade < 12:
		\item Die Rückgabe \textbf{vergessener Bücher} erfolgt in der Regel \textbf{beim Klassenleiter}. Markieren Sie diese mit einem Kreis \textbf{O}.
%else:
	\item Die Schüler \textbf{behalten} alle Bücher in \textbf{Prüfungsfächern} bis zum \textbf{Tag der Prüfung}; diese werden an diesem Tag gesondern eingesammelt.
	\item Bitte \textbf{markieren} Sie alle \textbf{noch ausstehenden Bücher}.
%end
\end{enumerate}

%num_bks = len([b for b in bks if not b.workbook and not b.classsets])

\rowcolors{1}{white}{black!10}
\begin{longtable}[l]{ | r | l l |
%i = 0
%for b in bks:
	%if not b.workbook and not b.classsets:
		p{0.05cm} |
		%i += 1
		%if i % 3 == 0 and i != num_bks:
			|
		%end
	%end
%end
}

	\hiderowcolors
	\hline
		& &
%for b in bks:
	%if not b.workbook and not b.classsets:
		& \rotatebox{90}{\scriptsize {{!tex_escape(b.title)}} }
	%end
%end
	\\
    	{\scriptsize Nr} & {\scriptsize Name} & {\scriptsize Vorname}
%for b in bks:
	%if not b.workbook and not b.classsets:
		& \rotatebox{90}{
		%if b.subject is None:
			\quad
		%else:
			{\footnotesize {{!tex_escape(b.subject.tag)}}}
		%end
		%if class_.grade + 1 >= 11:
			%if b.advanced and not b.novices:
			{\footnotesize (eA) }
			%else:
				%if not b.advanced and b.novices:
			{\footnotesize (gA) }
				%end
			%end
		%end
		}
	%end
%end
	\\
	\hline
%i = 1
%for s in students:
	%if i % 2 == 0:
		\showrowcolors
	%else:
		\hiderowcolors
	%end
		{\small {{i}} } &
	%i += 1
		{\footnotesize {{!tex_escape(s.person.name)}} } &
		{\footnotesize {{!tex_escape(shortName(s.person.firstname))}} }
	%for b in bks:
		%if not b.workbook and not b.classsets:
		&
			%n = loans.getLoanCount(s.person, b)
			%if n > 0:
		{{n}}
			%end		
		%end
	%end
	\\
	\hline
%end
\end{longtable}

Bitte quittieren Sie die Durchführung der Bücherrückgabe. Zur Annahme der Bücher und des Hefters stehe ich Ihnen am Bücherraum zur Verfügung. Bitte sorieren Sie die Bücher fächerweise vor. \\
\\

\begin{flushright}

	\rule{5cm}{0.1mm} \\
	Unterschrift

\end{flushright}

\pagebreak
