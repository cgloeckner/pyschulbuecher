%from app.db import orga_queries

%include("header")
<h1>Klasse {{c.to_string()}} löschen</h1>

Folgende Schüler befinden sich in dieser Klasse:
<ol>
%m = 0
%bks = dict()
%students = orga_queries.get_students_in(c.grade, c.tag)
%for s in students:
	<li>{{s.person.name}}, {{s.person.firstname}} \\
	%lns = s.person.loan
	%n = len(lns)
	%if n > 0:
({{n}} Leiheinträge)\\
		%m += n
		%bks[s] = lns
	%end
</li>
%end
</ol>

%if m > 0:
Diese Klasse kann nicht gelöscht werden, da noch Bücher ausgeliehen sind:
	<ul>
	%for s in bks:
		<li><b>{{s.person.name}}, {{s.person.firstname}}
	%end
	</ul>
%else:
Soll die Klasse {{c.to_string()}} WIRKLICH gelöscht werden? <a href="/admin/classes/delete/{{c.id}}/confirm">Löschen bestätigen</a>
%end

<hr />

<a href="/admin/classes/edit/{{c.id}}">Zurück zur Klasse</a>


%include("footer")
