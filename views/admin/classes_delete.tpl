%import db.orga as orga

%include("header")
<h1>Klasse {{c.toString()}} löschen</h1>

Folgende Schüler befinden sich in dieser Klasse:
<ol>
%m = 0
%students = orga.getStudentsIn(c.grade, c.tag)
%for s in students:
	<li>{{s.person.name}}, {{s.person.firstname}} \\
	%n = len(s.person.loan)
	%if n > 0:
({{n}} Leiheinträge)\\
		%m += n
	%end
</li>
%end
</ol>

%if m > 0:
Diese Klasse kann nicht gelöscht werden, da noch Bücher ausgeliehen sind
%else:
Soll die Klasse {{c.toString()}} WIRKLICH gelöscht werden? <a href="/admin/classes/delete/{{c.id}}/confirm">Löschen bestätigen</a>
%end

<hr />

<a href="/admin/classes/edit/{{c.id}}">Zurück zur Klasse</a>


%include("footer")
