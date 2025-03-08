%from app.db import Currency
%from utils import tex_escape, shortify_name
%from app.db import loan_queries as loans
%import datetime

%year = int(s.data['general']['school_year'])
\begin{center}
	{\LARGE Inventarbericht f\"ur das Schuljahr {{year}}/{{year+1}}}
\end{center}

\rowcolors{1}{white}{black!10}
\begin{longtable}{ | p{1cm} | p{5cm} | c | p{3.5cm} | c | c | c | }
	\hline
		
	\textbf{Fach} &
	\textbf{Titel} &
	\textbf{\small Klasse} &
	\textbf{Bemerkung} &
	\textbf{\small Bestand} &
	\textbf{\small Ausleihe} &
	\textbf{\small Übrig}
	\\ \hline

	%i = 0
	%for accept_classsets in [False, True]:
		%for b in all_bks:
			%if b.workbook or b.inGrade == 0:
				%continue
			%end
			%if b.classsets != accept_classsets:
				%continue
			%end
			%if b.subject is None:
	versch.
			%else:
	{{!tex_escape(b.subject.tag)}}
			%end
	&
	{{!tex_escape(b.title)}} &
			%if b.inGrade == b.outGrade:
	{{b.inGrade}}
			%else:
	{{b.inGrade}}-{{b.outGrade}}
			%end
	&
			%comments = []
			%if b.comment != '':
				%comments.append(b.comment)
			%end
			%if b.novices:
				%comments.append('gA')
			%end
			%if b.advanced:
				%comments.append('eA')
			%end
			%if b.classsets:
				%comments.append('Klassensätze')
			%end
	{{!tex_escape(', '.join(comments))}} &
	{{b.stock}} &
	{{loan_count[b]}} &
	{{b.stock - loan_count[b]}}

	\\ \hline
			
			%i += 1
			
			%if i % 2 == 0:
	\showrowcolors
			%else:
	\hiderowcolors
			%end
		%end
	%end
\end{longtable}
%end

