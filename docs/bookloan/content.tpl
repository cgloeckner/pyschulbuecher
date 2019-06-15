%from utils import tex_escape
%from db import loans

{\LARGE Leihexemplare zur Ausgabe {{class_.toString(advance=True)}} }
\hfill
%year = int(s.data['general']['school_year'])
{\large Schuljahr {{year+1}}/{{year+2}} }

%if class_.teacher is not None:
	Klassenleiter(in):
	\quad
	{{class_.teacher.person.name}}, {{class_.teacher.person.firstname}}
%end

Ihre Schüler haben mit dem Bücherzettel um folgende Leihexemplare gebeten. Beachten Sie dabei:
\begin{enumerate}
	\item Überprüfen Sie die Anzahl der Ihnen zur Verfügung gestellten Bücher.
	\item \textbf{Markieren} Sie in der untenstehenden Tabelle bitte \textbf{fehlende oder beschädigte Bücher} farbig.
	\item \textbf{Verzichten} Sie bitte auf eine Kennzeichnung ausgegebener Bücher.
	\item Stellen Sie jedem Schüler seine \textbf{Ausleihliste} zur Verfügung, damit die Eltern den Erhalt quittieren.
\end{enumerate}

Bitte fordern Sie die Ausleihlisten binnen einer Woche zurück und geben Sie die Hefter möglichst vollständig beim Schulbuchverantwortlichen ab.

\begin{flushright}

	\textit{Vielen Dank!}

\end{flushright}

%num_bks = len([b for b in bks if not b.workbook and not b.classsets])

\rowcolors{1}{white}{black!10}
\begin{longtable}[l]{ | r | l l |
%i = 0
%for b in bks:
	%if not b.workbook and not b.classsets:
		p{0.09cm} |
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
    	Nr & Name & Vorname
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


%count = dict()
%for b in bks:
	%if not b.workbook and not b.classsets:
		%count[b] = 0
	%end
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
		{\footnotesize {{!tex_escape(s.person.firstname)}} }
	%for b in bks:
		%if not b.workbook and not b.classsets:
		&
			%if loans.isRequested(s, b):
		{\scriptsize $\times$}
				%count[b] += 1
			%end		
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
	\\
	\hline
\end{longtable}

\pagebreak
