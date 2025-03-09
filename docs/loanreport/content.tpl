%from app import tex_escape
%from app.db import loan_queries
%import datetime

{\large Übersicht Leihexemplare \hfill {{!tex_escape(p.name)}}, {{!tex_escape(p.firstname)}} }

\rowcolors{1}{white}{black!10}
\begin{tabular}[c]{ | p{5cm} | c | c | r | }
	\hline
	
	\textbf{Titel} &
	\textbf{Fach} &
	\textbf{Klasse} &
	\textbf{Anzahl}
	\\ \hline

%i = 0
%for l in lns:
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

%if len(lns) == 0:
	\multicolumn{4}{|c|}{ keine }
	\\ \hline
%end
\end{tabular}

\vfill

%n = datetime.datetime.now()
{\large \hfill {{n.strftime('%d.%m.%Y')}} }\\

\pagebreak

