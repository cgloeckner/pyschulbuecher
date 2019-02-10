%from db.orm import Currency
%from utils import tex_escape

%if workbook:
	Arbeitshefte
%else:
	Lehrbücher
%end

\begin{tabular}{ | c | p{5cm} | l | c | c |
%if not workbook:
 r | r |
%end
}
    \hline
		Fach & Titel & Verlag & ISBN & Preis
%if not workbook:
 & V & F
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
\end{tabular}
\vspace{0.2cm}

