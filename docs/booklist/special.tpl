%if grade >= 11:
\textit{Hinweis:} Ist hinter dem Fach eines Buches \glqq gA\grqq{} oder \glqq eA\grqq{} angegeben, so wird dieses Buch \textbf{nur in dieser Kursart} verwendet. Bücher ohne entsprechende Angabe werden in allen Kursarten dieses Fachs verwendet.
%end


%from db.orm import Currency

\begin{longtable}{ | p{5cm} | c | c | c |}
    \hline
	& Preis & Erwerb ja & Erwerb nein \\ \hline
%for bk in spec_bks:
	{{bk.title}} ({{bk.comment}}) &
	%if grade == 5:
		kostenlos
	%else:
		{{Currency.toString(int(bk.price), addSymbol=False)}} \euro
	%end
	& & \\ \hline
\end{longtable}

