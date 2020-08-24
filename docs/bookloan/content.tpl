%from utils import tex_escape
%from db import loans
%from utils import shortName

{\LARGE Ausgabe der Leihexemplare in Klasse {{class_.toString()}} }
\hfill
%year = int(s.data['general']['school_year'])
{\large Schuljahr {{year}}/{{year+1}} }\\

Bitte beachten Sie:
%if class_.teacher is not None:
	\hfill 
	Klassenleiter(in): {{class_.teacher.person.name}}, {{class_.teacher.person.firstname}}
%end

\begin{enumerate}
	\item Überprüfen Sie die Anzahl der Ihnen zur Verfügung gestellten Bücher. Bitten melden Sie \textbf{fehlende oder beschädigte Bücher} umgehend, sodass Sie Ersatz erhalten können.
	\item Bitte kennzeichnen Sie in der Tabelle \textbf{nur Änderungen}, z.B. wenn Bücher doch gekauft wurden und nutzen Sie die erste Spalte zur Dokumentation Schüler, die ihre Bücher erhalten haben.
	\item Stellen Sie jedem Schüler seine \textbf{Ausleihliste} zur Verfügung, damit die Eltern den Erhalt quittieren.
%if class_.grade in [5, 7, 9, 11]:
	\item Fordern Sie die Ausleihlisten bitte binnen einer Woche zurück und geben Sie den Hefter möglichst vollständig beim Schulbuchverantwortlichen ab.
%end
\end{enumerate}

%num_bks = len([b for b in bks if not b.workbook and not b.classsets])

\rowcolors{1}{white}{black!10}
\begin{longtable}[l]{ | p{0.1cm} | p{0.15cm} | p{1.75cm} p{1.75cm} |
%i = 0
%for b in bks:
	%if not b.workbook and not b.classsets:
		p{0.045cm} |
		%i += 1
		%if i % 3 == 0 and i != num_bks:
			|
		%end
	%end
%end
%for b in spec_bks:
	p{0.045cm} |
%end
}

	\hiderowcolors
	\hline
		&
		& &
%for b in bks:
	%if not b.workbook and not b.classsets:
		& \rotatebox{90}{\scriptsize {{!tex_escape(b.title)}} }
	%end
%end
%for b in spec_bks:
		& \rotatebox{90}{\scriptsize {{!tex_escape(b.title)}} }
%end
	\\
    	{\checkmark} & {\scriptsize Nr} & {\scriptsize Name} & {\scriptsize Vorname}
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
%for b in spec_bks:
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
%for b in spec_bks:
	%count[b] = 0
%end

%i = 1
%for s in students:
	%if i % 2 == 0:
		\showrowcolors
	%else:
		\hiderowcolors
	%end
		$\square$ &
		{\small {{i}} } &
	%i += 1
		{\footnotesize {{!tex_escape(s.person.name)}} } &
		{\footnotesize {{!tex_escape(shortName(s.person.firstname))}} }
	%for b in bks:
		%if not b.workbook and not b.classsets:
		&
			%n = query_func(s.person, b)
			%if n > 0:
		{\scriptsize ${{n}}$}
				%count[b] += n
			%end		
		%end
	%end
	%for b in spec_bks:
		&
		%n = query_func(s.person, b)
		%if n > 0:
			{\scriptsize ${{n}}$}
			%count[b] += n
		%end
	%end
	\\
	\hline
%end
	& & & \textbf{Gesamt}:
	%for b in bks:
		%if not b.workbook and not b.classsets:
		&
		{\scriptsize {{count[b]}} }
		%end
	%end
	%for b in spec_bks:
		&
		{\scriptsize {{count[b]}} }
	%end
	\\
	\hline
\end{longtable}

Bitte quittieren Sie die Durchführung der Bücherausgabe. \\
\\

\begin{flushright}

	\rule{5cm}{0.1mm} \\
	Unterschrift

\end{flushright}

\pagebreak
