%from app import tex_escape
%from app.db import orga_queries as orga

{\LARGE Information zur Bücherrückgabe Klasse {{grade}} }

\hfill
%year = int(s.data['general']['school_year'])
{\large Schuljahr {{year}}/{{year+1}} }

%teachers = list()
%for c in orga.get_classes_by_grade(grade):
	%if c.teacher is not None:
		%teachers.append(c.teacher)
	%end
%end

%if len(teachers) > 0:
	Klassenleiter(in):
	\begin{itemize}
	%for t in teachers:
		\item {{t.person.name}}, {{t.person.firstname}}
	%end
	\end{itemize}
%end

Bitte informieren Sie Ihre Schüler, dass demnächst folgende Bücher eingesammelt werden:

\rowcolors{1}{white}{black!10}
\begin{longtable}[l]{ | l | c | c | }
	\hiderowcolors
	\hline
	\textbf{Titel} & \textbf{Fach} & \textbf{Klasse}
	\\ \hline

%i = 1
%for b in bks:
	%if not b.workbook and not b.classsets:
		%if i % 2 == 0:
	\showrowcolors
		%else:
	\hiderowcolors
		%end
	%i += 1
	{{!tex_escape(b.title)}} &
		%if b.subject is not None:
	{{!tex_escape(b.subject.tag)}} &
		%else:
	versch. &
		%end
		%if b.inGrade == b.outGrade:
	{{b.inGrade}}
		%else:
	{{b.inGrade}}-{{b.outGrade}}
		%end
	\\ \hline
	
	%end
%end
\end{longtable}

%if grade == 12:
Die Bücher in den \textbf{Prüfungsfächern verbleiben} bis zur Prüfung bei den Schülern und sind \textbf{am Tag der Prüfung} abzugeben.
%end

Weitere Informationen erhalten Sie in Kürze.

\begin{flushright}

	\textit{Vielen Dank!}

\end{flushright}

\pagebreak
