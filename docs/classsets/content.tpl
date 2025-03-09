%from app import tex_escape
%from app.db import loan_queries
%import datetime

{\large Übersicht Klassensätze \hfill {{!tex_escape(p.name)}}, {{!tex_escape(p.firstname)}} }

\rowcolors{1}{white}{black!10}
\begin{tabular}[c]{ | p{6.95cm} | c | c | r | }
	\hline
	
	\textbf{Titel} &
	\textbf{Fach} &
	\textbf{Klasse} &
	\textbf{Anzahl}
	\\ \hline

%i = 0
%for l in lns:
	%if l.count > threshold:
		{{!tex_escape(l.book.title)}} &
		%if l.book.subject is None:
		versch. &
		%else:
		{{!tex_escape(l.book.subject.tag)}} &
		%end
		%if l.book.inGrade < l.book.outGrade:
		{{l.book.inGrade}}-{{l.book.outGrade}} &
		%else:
		{{l.book.inGrade}} &
		%end
		{{l.count}}
		
		\\ \hline
		
		%i += 1
		
		%if i % 2 == 0:
			\showrowcolors
		%else:
			\hiderowcolors
		%end
	%end
%end

%if i == 0:
	\multicolumn{4}{|c|}{ keine }
	\\ \hline
%end
\end{tabular}

Hiermit bestätige ich im Besitz der oben genannten Klassensätze zu sein.

\vspace{0.5cm}

\hfill \hrulefill \hfill \hrulefill

\hfill Datum \hfill Unterschrift


%if pagebreak:
	\pagebreak
%else:
	\vfill
%end

