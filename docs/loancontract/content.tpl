%from app.db import Currency
%from app import tex_escape, shortify_name
%from app.db import loan_queries
%import datetime

{\Large Schulbuchübersicht } \hfill {\large {{!tex_escape(student.person.name)}}, {{!tex_escape(shortify_name(student.person.firstname))}} ({{student.class_.to_string(advance=advance)}}) }

%if loan_report:
	Ihnen wurden folgende Lehrbücher als Leihexemplare überlassen. Vermerken Sie die Inventarnummer und notieren Sie die Anzahl \linebreak der vorherigen Leihen des Buchs (siehe Ausleihstempel).

	\rowcolors{1}{white}{black!10}
	\begin{tabular}[c]{ | p{0.75cm} | c | p{6.5cm} | c | c | }
		\hline
		
		\textbf{\small Fach} &
		\textbf{\small Klasse} &
		\textbf{\small Lehrbuch} &
		\textbf{\small Inv.-Nr.} &
		\textbf{\small Anz. Leihen}
		\\ \hline

	%bks = set()

	%i = 0
	%prev_classes = list()
	%for l in lns:
		%bks.add(l.book)
		%if l.book.subject is None:
		versch. &
		%else:
		{{!tex_escape(l.book.subject.tag)}} &
		%end
		%if l.book.inGrade == l.book.outGrade:
		{{l.book.inGrade}} &
		%else:
		{{l.book.inGrade}}-{{l.book.outGrade}} &
		%end
		{{!tex_escape(l.book.title)}} &
		&
		\\ \hline
		
		%i += 1
		
		%if i % 2 == 0:
			\showrowcolors
		%else:
			\hiderowcolors
		%end
	%end
	
	%if i == 0:
		\multicolumn{5}{c}{ keine Lehrbücher }
	%end

	\end{tabular}

	\vspace{1cm}

	\rule{4.5cm}{0.4pt} \hfill \rule{4.5cm}{0.4pt} \\
	Datum \hfill Unterschrift Klassenleitung \\

% else:

	Ihnen wurden folgende Lehrbücher als Leihexemplare überlassen. Vermerken Sie die Inventarnummer und notieren Sie die Anzahl \linebreak der vorherigen Leihen des Buchs (siehe Ausleihstempel).

	\rowcolors{1}{white}{black!10}
	\begin{tabular}[c]{ | p{0.75cm} | c | p{6.5cm} | c | c | }
		\hline
		
		\textbf{\small Fach} &
		\textbf{\small Klasse} &
		\textbf{\small Lehrbuch} &
		\textbf{\small Inv.-Nr.} &
		\textbf{\small Anz. Leihen}
		\\ \hline

	%bks = set()

    %g = student.class_.grade
    %if advance:
        % g += 1
    %end

	%i = 0
	%prev_classes = list()
	%for l in lns:
		%if l.book.inGrade == g:
			%if l.book in bks:
				%continue
			%end
			%bks.add(l.book)
			%if l.book.subject is None:
		versch. &
			%else:
		{{!tex_escape(l.book.subject.tag)}} &
			%end
			%if l.book.inGrade == l.book.outGrade:
		{{l.book.inGrade}} &
			%else:
		{{l.book.inGrade}}-{{l.book.outGrade}} &
			%end
		{{!tex_escape(l.book.title)}} &
		&
		\\ \hline
		
			%i += 1
		
			%if i % 2 == 0:
			\showrowcolors
			%else:
			\hiderowcolors
			%end
		%else:
			%prev_classes.append(l.book.inGrade)
		%end
	%end

	%for r in rqs:
		%if r.book.inGrade == 0:
			%# skip special book (Schulplaner etc.)
			%continue
		%end
		%if r.book in bks:
			%continue
		%end
		%bks.add(r.book)
		%if r.book.subject is None:
		versch. &
			%else:
		{{!tex_escape(r.book.subject.tag)}} &
			%end
			%if r.book.inGrade == r.book.outGrade:
		{{r.book.inGrade}} &
			%else:
		{{r.book.inGrade}}-{{r.book.outGrade}} &
			%end
		{{!tex_escape(r.book.title)}} &
		&
		\\ \hline
		
			%i += 1
		
			%if i % 2 == 0:
			\showrowcolors
			%else:
			\hiderowcolors
			%end
	%end

	%if i == 0:
		\multicolumn{5}{c}{ keine Lehrbücher }
	%end

	\end{tabular}
	
	\vspace{1cm}

	\rule{4.5cm}{0.4pt} \hfill \rule{4.5cm}{0.4pt} \\
	Datum \hfill Unterschrift Klassenleitung \\
	
	{ \large Bereits ausgeliehene Bücher }

	Bitte überprüfen Sie folgende bereits ausgeliehene Lehrbücher:

	\rowcolors{1}{white}{black!10}
	\begin{tabular}[c]{ | p{0.75cm} | c | p{6.5cm} | c | c | }
		\hline
		
		\textbf{\small Fach} &
		\textbf{\small Klasse} &
		\textbf{\small Lehrbuch} &
		\textbf{\small Inv.-Nr.} &
		\textbf{\small seit}
		\\ \hline

		%i = 0
		%for l in lns:
			%if l.book.inGrade < g:
				%if l.book.subject is None:
		versch. &
				%else:
		{{!tex_escape(l.book.subject.tag)}} &
				%end
				%if l.book.inGrade == l.book.outGrade:
		{{l.book.inGrade}} &
				%else:
		{{l.book.inGrade}}-{{l.book.outGrade}} &
				%end
		{{!tex_escape(l.book.title)}} &
		&
		{{l.getSchoolYear()}}
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
		\multicolumn{5}{c}{ keine Lehrbücher }
		%end

	\end{tabular}

	%end
%end

Hiermit bestätige ich im Besitz der oben genannten Bücher zu sein.

\vspace{1cm}

\rule{4.5cm}{0.4pt} \hfill \rule{4.5cm}{0.4pt} \\
Datum \hfill Unterschrift Eltern \\

\null\vfill

\pagebreak

