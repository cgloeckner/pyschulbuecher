%from db.orm import Currency
%from utils import tex_escape, shortName
%from db import loans
%import datetime

{\Large Schulbuchübersicht } \hfill {\large {{!tex_escape(student.person.name)}}, {{!tex_escape(shortName(student.person.firstname))}} ({{student.class_.toString()}}) }

Bitte überprüfen Sie den Erhalt folgender Lehrbücher, vermerken Sie die individuelle Buchnummer (LMF-Nr.) und bewerten Sie deren \linebreak Zustand: \hfill neu \textbf{++} \quad gut \textbf{+} \quad mittel \textbf{$\circ$} \quad schlecht \textbf{-}

\rowcolors{1}{white}{black!10}
\begin{tabular}[c]{ | p{0.75cm} | c | p{5.5cm} | c | c | }
	\hline
	
	\textbf{Fach} &
	\textbf{\small Klasse} &
	\textbf{Lehrbuch} &
	\textbf{LMF-Nr.} &
	\textbf{\small Zustand}
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
	&
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
	\multicolumn{5}{c}{ keine Lehrbücher }
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
\begin{tabular}[c]{ | p{0.75cm} | c | p{5.5cm} | c | c | }
	\hline
	
	\textbf{Fach} &
	\textbf{\small Klasse} &
	\textbf{Lehrbuch} &
	\textbf{LMF-Nr.} &
	\textbf{\small Zustand}
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
	%#------------ note this will be used next year
	&
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
	\multicolumn{5}{c}{ keine Lehrbücher }
	%end

\end{tabular}

%end

\vfill

Hiermit bestätige ich im Besitz der oben genannten Bücher zu sein.

\vspace{1.5cm}

\hfill \hrulefill \hfill \hrulefill

\hfill Datum, Ort \hfill Unterschrift


\pagebreak

