%from app import tex_escape
%from app.db import loan_queries
%from app.utils import shortify_name

{\LARGE Ausgabe der Leihexemplare in Klasse {{class_.to_string(advance=advance)}} }
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
	\item Stellen Sie jedem Schüler seine \textbf{Leihliste} (A5) zur Verfügung und quittieren Sie darauf die Ausgabe der aufgelisteten Bücher.
	\item Die Eltern quittieren den Erhalt. Fordern Sie die Leihlisten \textbf{binnen einer Woche zurück}.
	\item \textbf{Überprüfen Sie} die von den Schülern zurückgegebene \textbf{Leihlisten} auf \textbf{Vollständigkeit} und quittieren Sie den Erhalt in der zweiten Spalte. \textbf{Geben} Sie den Hefter \textbf{vollständig} beim Schulbuchverantwortlichen \textbf{ab}.
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
		  \rotatebox{90}{\scriptsize B\"ucher erhalten}
		& \rotatebox{90}{\scriptsize Leihliste abgegeben}
		&
		&
%for b in bks:
	%if not b.workbook and not b.classsets:
		& \rotatebox{90}{\scriptsize {{!tex_escape(b.title)}} }
	%end
%end
%for b in spec_bks:
		& \rotatebox{90}{\scriptsize {{!tex_escape(b.title)}} }
%end
	\\
    	  {\checkmark}
    	& {\checkmark}
    	& {\scriptsize Name}
    	& {\scriptsize Vorname}
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
		$\square$ &
	%i += 1
		{\footnotesize {{!tex_escape(s.person.name)}} } &
		{\footnotesize {{!tex_escape(shortify_name(s.person.firstname))}} }
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

Diese Übersicht verbleibt beim Klassenleiter. \\

\pagebreak
