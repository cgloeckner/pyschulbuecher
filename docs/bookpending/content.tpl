%from utils import tex_escape
%from db import loans
%from db.orm import Currency

{\LARGE Ausstehende Leihexemplare \hfill {{!tex_escape(person.name)}}, {{!tex_escape(person.firstname)}}}

Folgende Leihexemplare wurden bislang \textbf{nicht} zurückgegeben:

\rowcolors{1}{white}{black!10}
\begin{longtable}[l]{ | c | c | c | p{5.75cm} | r | }
	\hiderowcolors
	\hline
	& Fach & Klasse & Titel & Anzahl \\ \hline

%wert = 0
%i = 1
%for l in person.loan:
	{{i}} &
	%i += 1
	%if l.book.subject is not None:
	{{l.book.subject.tag}} &
	%else:
	versch. &
	%end
	{{l.book.inGrade}}\\
	%if l.book.inGrade != l.book.outGrade:
-{{l.book.outGrade}}\\
	%end
 &
 	{{!tex_escape(l.book.title)}} &
	%#if l.book.price is not None:
	%#{{!tex_escape(Currency.toString(l.book.price))}} &
	%#wert += l.count * l.book.price
	%#else:
	%#	\textit{Nicht mehr lieferbar} &
	%#end
	{{l.count}} $\times$
	\\
	\hline
	
%end
\end{longtable}

%#\textbf{Gesamtwert:} {{!tex_escape(Currency.toString(wert))}}

%if n % 2 == 0:
\pagebreak
%else:
\vspace{0.5\textheight}
%end

