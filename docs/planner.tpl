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

