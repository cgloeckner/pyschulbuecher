%from db.orm import Currency
%from utils import tex_escape

{\large
%if workbook:
	Arbeitshefte
%else:
	Lehrbücher
%end
}

%if workbook:
	\begin{longtable}{ | c | p{6cm} | p{2.8cm} | c | r | }
%else:
	\begin{longtable}{ | c | p{4.5cm} | p{2cm} | c | r | p{1cm} | p{1cm} | }
%end
    \hline
		\textbf{Fach} & \textbf{Titel} & \textbf{Verlag} & \textbf{ISBN} & \textbf{Preis}
%if not workbook:
 & \textbf{\enskip V/K} & \textbf{\quad F}
%end
\\ \hline
%for b in bs:
	%if b.workbook == workbook:
		%if b.subject is not None:
			%ga = b.novices
			%ea = b.advanced
			%cmt = len(b.comment) > 0
			%if ga or ea or cmt:
	\makecell{
			%end
		{\small {{!tex_escape(b.subject.tag)}} }
			%if grade > 10:
				%if ea and ga:
					%pass
				%else:
					%if ea:
		{\footnotesize eA }
					%end
					%if ga:
		{\footnotesize gA }
					%end
				%end
			%end
			%if cmt:
		{\footnotesize {{!tex_escape(b.comment)}} }
	}
			%end
			%if ga or ea:
	}
			%end
		%else:
	{\small versch. }
		%end
	& 
	{\small {{!tex_escape(b.title)}} }
	&
	{\small {{!tex_escape(b.publisher.name)}}}
	&
		%if b.isbn is not None and b.price is not None:
		{\small {{!tex_escape(b.isbn)}} }
		&
		{\small {{!tex_escape(Currency.toString(b.price))}} \euro }
		%else:
	\multicolumn{2}{c|}{\small {\textit {{nicht mehr verf\"ugbar}} } }
		%end
		%if not b.workbook:
	&
			%if b.classsets:
	\multicolumn{2}{c|} { \small { Klassens\"atze } }
			%else:
				%if b.isbn is None or b.price is None:
	\cellcolor{black!75}
	&
				%else:
	&
				%end
			%end
		%end
	\\
	\hline
	%end
%end
\end{longtable}

