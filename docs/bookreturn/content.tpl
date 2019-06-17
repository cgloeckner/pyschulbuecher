%from utils import tex_escape
%from db import loans

{\LARGE Ausleihliste zur Bücherrückgabe {{class_.toString()}} }
\hfill
%year = int(s.data['general']['school_year'])
{\large Schuljahr {{year}}/{{year+1}} }

%if class_.teacher is not None:
	Klassenleiter(in):
	\quad
	{{class_.teacher.person.name}}, {{class_.teacher.person.firstname}}
%end

Bitte sammeln Sie die untenstehenden Bücher von Ihren Schülern an. Beachten Sie dabei:
\begin{enumerate}
	\item Für jeden Schüler existiert eine Ausleihliste (in diesem Hefter). Bitte \textbf{quittieren} Sie dabei dabei den Erhalt der einzelnen Bücher.
	\item \textbf{Markieren} Sie in der untenstehenden Tabelle bitte alle \textbf{noch nicht zurückgegebenen Bücher} (z.B. Rotstift oder Textmarker). Es liegt in der Verantwortung der entsprechenden Schüler diese beim Schulbuchverantwortlichen abzugeben.
	\item \textbf{Verzichten} Sie bitte auf eine Kennzeichnung zurückgegebener Bücher.
\end{enumerate}

Zur Annahme der Bücher und des Hefters stehe ich Ihnen am Bücherraum zur Verfügung.

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

\pagebreak