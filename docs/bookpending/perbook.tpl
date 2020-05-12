%from utils import tex_escape

{\LARGE Ausstehende Leihexemplare \newline

{{!tex_escape(book.title)}}
%if book.subject is not None:
	({{!tex_escape(book.subject.tag)}})
%end
}

Folgende Schüler haben ihr Leihexemplar bislang \textbf{nicht} zurückgegeben:

\rowcolors{1}{white}{black!10}
\begin{longtable}[l]{ | c | p{2cm} | p{3cm} | p{3cm} | c | }
	\hiderowcolors
	\hline
	& Kurs & Name & Vorname & \\ \hline
%i = 1
%for l in loans:
	%if l.person.student is None or l.person.student.class_ is None or l.person.student.class_.grade != 12:
		%# ignore everybody except 12th grade
		%continue
	%end
	%if i % 2 == 0:
		\showrowcolors
	%else:
		\hiderowcolors
	%end
	{{i}} &
	%i += 1
	{{!tex_escape(l.person.student.class_.toString())}} &
	{{!tex_escape(l.person.name)}} &
	{{!tex_escape(l.person.firstname)}} &
	{{l.count}}x
	\\ \hline
%end

\end{longtable}

\pagebreak
