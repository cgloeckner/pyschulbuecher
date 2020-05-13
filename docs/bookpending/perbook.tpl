%from utils import tex_escape, shortName

%comments = []
%if book.subject is not None:
	%comments.append(book.subject.tag)
%end
%if book.inGrade < book.outGrade:
	%comments.append('Klasse {0}-{1}'.format(book.inGrade, book.outGrade))
%else:
	%comments.append('Klasse {0}'.format(book.inGrade))
%end
%if book.novices != book.advanced:
	%if book.novices:
		%comments.append('gA')
	%else:
		%comments.append('eA')
	%end
%end
%if book.comment != '':
	%comments.append(book.comment)
%end

{\LARGE {{!tex_escape(book.title)}} ({{!tex_escape(', '.join(comments))}}) }

Folgende Schüler haben ihr Leihexemplar bislang \textbf{nicht} zurückgegeben:

\rowcolors{1}{white}{black!10}
\begin{longtable}[l]{ | c | p{2cm} | p{3cm} | p{3cm} | c | }
	\hiderowcolors
	\hline
	& Kurs & Name & Vorname & \\ \hline
%i = 1
%for l in loans:
	%if l.person.student is None or l.person.student.class_ is None or l.person.student.class_.grade != 12:
		%# ignore everybody except 12th grade
		%continue
	%end
	%if i % 2 == 0:
		\showrowcolors
	%else:
		\hiderowcolors
	%end
	{{i}} &
	%i += 1
	{{!tex_escape(l.person.student.class_.toString())}} &
	{{!tex_escape(l.person.name)}} &
	{{!tex_escape(shortName(l.person.firstname))}} &
	{{l.count}}x
	\\ \hline
%end

\end{longtable}

\pagebreak
