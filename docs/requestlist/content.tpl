%from utils import tex_escape, shortName

{\LARGE Erfassung Bücherzettel {{class_.toString()}} }
\hfill
%year = int(s.data['general']['school_year'])
{\large für Klasse {{class_.grade+1}} ({{year}}/{{year+1}}) }

%if class_.teacher is not None:
	Klassenleiter(in):
	\quad
	{{class_.teacher.person.name}}, {{class_.teacher.person.firstname}}
%end

Bitte für jedes gewünschte Freiexemplar ein Kreuz setzen:

%num_bks = len([b for b in bks if not b.workbook and not b.classsets])

\rowcolors{1}{white}{black!10}
\begin{longtable}[l]{ | r | l l |
%i = 0
%for b in bks:
	%if not b.workbook and not b.classsets:
		p{0.125cm} |
		%i += 1
		%if i % 3 == 0 and i != num_bks:
			|
		%end
	%end
%end
%for b in spec_bks:
	p{0.175cm} |
%end
}

	\hiderowcolors
	\hline
		& &
%for b in bks:
	%if not b.workbook and not b.classsets:
		& \rotatebox{90}{\footnotesize {{!tex_escape(b.title)}} }
	%end
%end	
%for b in spec_bks:
		& \rotatebox{90}{\footnotesize {{!tex_escape(b.title)}} }
%end
	\\
    	\footnotesize Nr & \footnotesize Name & \footnotesize Vorname
%for b in bks:
	%if not b.workbook and not b.classsets:
		& \rotatebox{90}{
		%if b.subject is None:
			\quad
		%else:
			\footnotesize {{!tex_escape(b.subject.tag)}}
		%end
		%if class_.grade + 1 >= 11:
			%if b.advanced and not b.novices:
			{\small (eA) }
			%else:
				%if not b.advanced and b.novices:
			{\small (gA) }
				%end
			%end
		%end
		}
	%end
%end
%for b in spec_bks:
		&
%end
	\\
	\hline
%i = 1
%for s in students:
	%if i % 2 == 0:
		\showrowcolors
	%else:
		\hiderowcolors
	%end
		{\small {{i}} } &
	%i += 1
		{\footnotesize {{!tex_escape(s.person.name)}} } &
		{\footnotesize {{!tex_escape(shortName(s.person.firstname))}} }
	%for b in bks:
		%if not b.workbook and not b.classsets:
		&
		%end
	%end
	%for b in spec_bks:
		&
	%end
	\\
	\hline
%end
\end{longtable}

\begin{flushright}

	Anzahl benötiger Schulplaner: \rule[-4pt]{4cm}{0.1mm} Stück

	\textit{Vielen Dank!}

\end{flushright}

\pagebreak
