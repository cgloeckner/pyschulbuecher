%from db.orm import Currency
%from utils import tex_escape, shortName
%from db import loans
%import datetime

{\Large Schulbuchübersicht } \hfill {\large {{!tex_escape(student.person.name)}}, {{!tex_escape(shortName(student.person.firstname))}} ({{student.class_.toString(advance=advance)}}) }

%if loan_report:
	Bitte überprüfen Sie folgende Lehrbücher, vermerken Sie die individuelle Buchnummer (LMF-Nr.) und bewerten Sie deren \linebreak Zustand: \hfill neu \textbf{++} \quad gut \textbf{+} \quad mittel \textbf{$\circ$} \quad schlecht \textbf{-}

	\rowcolors{1}{white}{black!10}
	\begin{tabular}[c]{ | p{0.75cm} | c | p{5.5cm} | c | c | }
		\hline
		
		\textbf{Fach} &
		\textbf{\small Klasse} &
		\textbf{Lehrbuch} &
		\textbf{LMF-Nr.} &
		\textbf{\small Zustand}
		\\ \hline

	%bks = set()

	%i = 0
	%prev_classes = list()
	%for l in lns:
		%bks.add(l.book)
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
	%end
	
	%if i == 0:
		\multicolumn{5}{c}{ keine Lehrbücher }
	%end

	\end{tabular}

% else:

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

	%bks = set()
	
	%g = student.class_.grade
	%if advance:
		% g += 1
	%end


	%i = 0
	%prev_classes = list()
	%for l in lns:
		%if l.book.inGrade == student.class_.grade:
			%if l.book in bks:
				%continue
			%end
			%bks.add(l.book)
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

	%for r in rqs:
		%if r.book.inGrade == 0:
			%# skip special book (Schulplaner etc.)
			%continue
		%end
		%if r.book in bks:
			%continue
		%end
		%bks.add(r.book)
		%if r.book.subject is None:
		versch. &
			%else:
		{{!tex_escape(r.book.subject.tag)}} &
			%end
			%if r.book.inGrade == r.book.outGrade:
		{{r.book.inGrade}} &
			%else:
		{{r.book.inGrade}}-{{r.book.outGrade}} &
			%end
		{{!tex_escape(r.book.title)}} &
		&
		\\ \hline
		
			%i += 1
		
			%if i % 2 == 0:
			\showrowcolors
			%else:
			\hiderowcolors
			%end
	%end

	%if i == 0:
		\multicolumn{5}{c}{ keine Lehrbücher }
	%end

	\end{tabular}

	{ \large Bereits ausgeliehene Bücher }

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
		
		%if i == 0:
		\multicolumn{5}{c}{ keine Lehrbücher }
		%end

	\end{tabular}

	%end
%end

\vfill

Hiermit bestätige ich im Besitz der oben genannten Bücher zu sein.

\vspace{1.5cm}

\hfill \hrulefill \hfill \hrulefill

\hfill Datum, Ort \hfill Unterschrift Eltern


\pagebreak

