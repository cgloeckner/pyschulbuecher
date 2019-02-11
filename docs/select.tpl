%from db.orm import Currency
%from utils import tex_escape

{\large
%if workbook:
	Arbeitshefte
%else:
	Lehrbücher
%end
}

\begin{longtable}{ | c | p{5cm} | c | c | r |
%if not workbook:
 r | r |
%end
}
    \hline
		\textbf{Fach} & \textbf{Titel} & \textbf{Verlag} & \textbf{ISBN} & \textbf{Preis}
%if not workbook:
 & \textbf{V} & \textbf{F}
%end
\\ \hline
%for b in bs:
	%if not b.classsets and b.workbook == workbook:
		%if b.subject is not None:
			%ga = b.novices
			%ea = b.advanced
			%cmt = len(b.comment) > 0
			%if ga or ea or cmt:
				\makecell{
			%end
			{{!tex_escape(b.subject.tag)}}
			%if grade > 10:
				%if ea and ga:
					\\eA+gA
				%else:
					%if ea:
						\\eA
					%end
					%if ga:
						\\gA
					%end
				%end
			%end
			%if cmt:
				\\{{!tex_escape(b.comment)}}
			%end
			%if ga or ea or cmt:
				}
			%end
		%end
		& {{!tex_escape(b.title)}} & {{!tex_escape(b.publisher.name)}} & {{!tex_escape(b.isbn)}} & {{!tex_escape(Currency.toString(b.price))}} \euro
%if not workbook:
 & &
%end
\\ \hline
	%end
%end
\end{longtable}


