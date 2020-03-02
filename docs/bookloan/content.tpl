%from utils import tex_escape
%from db import loans
%from utils import shortName

{\LARGE Ausgabe der Leihexemplare in Klasse {{class_.toString()}} }
\hfill
%year = int(s.data['general']['school_year'])
{\large Schuljahr {{year}}/{{year+1}} }\\

%if class_.teacher is not None:
	Klassenleiter(in):
	\quad
	{{class_.teacher.person.name}}, {{class_.teacher.person.firstname}}
%end

Bitte beachten Sie:
\begin{enumerate}
	\item Überprüfen Sie die Anzahl der Ihnen zur Verfügung gestellten Bücher. Bitten melden Sie \textbf{fehlende oder beschädigte Bücher} umgehend, sodass Sie Ersatz erhalten können.
	\item Bitte kennzeichnen Sie in der untenstehenden Tabelle \textbf{keine ausgegebenen Bücher}, sondern \textbf{nur Änderungen} farbig. (z.B. wenn Bücher doch gekauft wurden) 
	\item Stellen Sie jedem Schüler seine \textbf{Ausleihliste} zur Verfügung, damit die Eltern den Erhalt quittieren.
%if class_.grade in [5, 7, 9, 11]:
	\newline Die Schüler der Klassenstufen 5, 7, 9 und 11 erhalten \textbf{neue Ausleihlisten}, um eine übersichtliche Dokumentation der Leihexemplare zu ermöglichen. Alte Leihlisten \textbf{verbleiben} im Hefter.
	\item Fordern Sie die Ausleihlisten bitte binnen einer Woche zurück und geben Sie den Hefter möglichst vollständig beim Schulbuchverantwortlichen ab.
%end
\end{enumerate}

\begin{flushright}

	\textit{Vielen Dank!}

\end{flushright}

Ihre Schüler haben um folgende Leihexemplare gebeten:

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
%for b in misc:
	p{0.05cm} |
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
%for b in misc:
		& \rotatebox{90}{\scriptsize {{!tex_escape(b.title)}} }
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
%for b in misc:
		&
%end
	\\
	\hline


%count = dict()
%for b in bks:
	%if not b.workbook and not b.classsets:
		%count[b] = 0
	%end
%end
%for b in misc:
	%count[b] = 0
%end

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
		{\scriptsize ${{n}}$}
				%count[b] += n
			%end		
		%end
	%end
	%for b in misc:
		&
		%n = loans.getLoanCount(s.person, b)
		%if n > 0:
			{\scriptsize ${{n}}$}
			%count[b] += n
		%end
	%end
	\\
	\hline
%end
	& & \textbf{Gesamt}:
	%for b in bks:
		%if not b.workbook and not b.classsets:
		&
		{\scriptsize {{count[b]}} }
		%end
	%end
	%for b in misc:
		&
		{\scriptsize {{count[b]}} }
	%end
	\\
	\hline
\end{longtable}

\pagebreak
