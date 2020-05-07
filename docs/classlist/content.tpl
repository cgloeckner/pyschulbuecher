%from utils import tex_escape

{\Large Klassenübersicht }

\rowcolors{1}{white}{black!10}
\begin{tabular}[c]{ | p{2cm} | p{4.5cm} | c | }
	\hline
	
	\textbf{Klasse} &
	\textbf{Klassenleiter} &
	\textbf{Anzahl Schüler}
	\\ \hline

%i = 0
%for c in classes:
	%if c.teacher is None:
		%continue # e.g. 4th grade (new 5th grade)
	%end
	%p = c.teacher.person
	{{!tex_escape(c.toString())}} &
	{{!tex_escape(p.name)}}, {{!tex_escape(p.firstname[0])}}. &
	{{len(c.student)}}
	\\ \hline

	%i += 1
	%if i % 2 == 0:
	\showrowcolors
	%else:
	\hiderowcolors
	%end
%end
\end{tabular}

