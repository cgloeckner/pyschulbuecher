%if grade >= 10:
\textit{Hinweis:} Bitte beachten Sie die Angaben \glqq 2. FS\grqq{} bzw. \glqq 3. FS\grqq{} für zweite (fortgesetzte) bzw. die dritte (neu einsetzende) Fremdsprache.
	%if grade >= 11:
Ist hinter dem Fach eines Buches \glqq gA\grqq{} oder \glqq eA\grqq{} angegeben, so wird dieses Buch \textbf{nur in dieser Kursart} verwendet. Bücher ohne entsprechende Angabe werden in allen Kursarten dieses Fachs verwendet.
	%end
%end


%from db.orm import Currency

\begin{longtable}{ | p{5cm} | c | c | c |}
    \hline
	& Preis & Erwerb ja & Erwerb nein \\ \hline
	Schulplaner FSG (HA, Stundenplan, Noten, Termine) &
	%if grade == 5:
		kostenlos
	%else:
		{{Currency.toString(s.planner_price)}} \euro
	%end
	& & \\ \hline
\end{longtable}

