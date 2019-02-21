%import db.orga as orga

%include("header")
%c = orga.db.Class.get(grade=grade, tag=tag)
<h1>Übersicht Klasse {{c.toString()}}</h1>
<a href="/admin/classes/edit/{{c.id}}">Bearbeiten</a>

%i = 1
<table>
	<tr>
		<th>Nr.</th>
		<th>Name, Vorname</th>
	</tr>
%for s in orga.getStudentsIn(grade, tag):
	<tr>
		<td>{{i}}</td>
%i += 1
		<td><a href="/admin/students/edit/{{s.id}}">{{s.person.name}}, {{s.person.firstname}}</a></td>
	</tr>
%end
</table>

%include("footer")
