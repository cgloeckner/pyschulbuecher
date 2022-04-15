%from utils import tex_escape

%from db.orm import Currency

\begin{longtable}{ | p{5cm} | c | c | c |}
    \hline
	& Preis & Erwerb ja & Erwerb nein \\ \hline
%for bk in spec_bks:
	{{!tex_escape(bk.title)}} ({{bk.comment}}) &
	%if grade == 5:
		kostenlos
	%else:
		{{Currency.toString(int(bk.price), addSymbol=False)}} \euro
	%end
	& \checkinput & \checkinput \\ \hline
%end
\end{longtable}

