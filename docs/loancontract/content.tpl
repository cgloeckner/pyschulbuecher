%from db.orm import Currency
%from utils import tex_escape
%from db import loans
%import datetime

{\Large Schulbuchübersicht } \hfill {\large {{!tex_escape(student.person.name)}}, {{!tex_escape(student.person.firstname)}} ({{student.class_.toString()}}) }

Bitte überprüfen Sie den Erhalt folgender Lehrbücher und bewerten Sie deren \linebreak Zustand: \hfill neu \textbf{++} \quad gut \textbf{+} \quad mittel \textbf{$\circ$} \quad schlecht \textbf{-}

\rowcolors{1}{white}{black!10}
\begin{tabular}[c]{ | p{1cm} | c | p{6.5cm} | c | }
	\hline
	
	\textbf{Fach} &
	\textbf{Klasse} &
	\textbf{Lehrbuch} &
	\textbf{Zustand}
	\\ \hline

%i = 0
%prev_classes = list()
%for l in lns:
	%if l.book.inGrade == student.class_.grade:
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

%if len(lns) == 0:
	\multicolumn{4}{c}{ keine Lehrbücher }
%end

\end{tabular}

{ \large Weiterführung aus \\
%if len(prev_classes) > 0:
 Klasse {{min(prev_classes)}}
	%if min(prev_classes) < max(prev_classes):
 bis {{max(prev_classes)}}
	%end
%else:
 früheren Klassenstufen
%end
}

Bitte überprüfen Sie den Zustand folgender Lehrbücher:

\rowcolors{1}{white}{black!10}
\begin{tabular}[c]{ | p{1cm} | c| p{6.5cm} | c | }
	\hline
	
	\textbf{Fach} &
	\textbf{Klasse} &
	\textbf{Lehrbuch} &
	\textbf{Zustand}
	\\ \hline

	%i = 0
	%for l in lns:
		%if l.book.inGrade < student.class_.grade:
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
	\\ \hline
	
			%i += 1
	
			%if i % 2 == 0:
		\showrowcolors
			%else:
		\hiderowcolors
			%end
		%end
	%end
	
	%if len(prev_classes) == 0:
	\multicolumn{4}{c}{ keine Lehrbücher }
	%end

\end{tabular}

%end

\vfill

Hiermit bestätige ich im Besitz der oben genannten Bücher zu sein.

\vspace{1.5cm}

\hfill \hrulefill \hfill \hrulefill

\hfill Datum, Ort \hfill Unterschrift


\pagebreak

