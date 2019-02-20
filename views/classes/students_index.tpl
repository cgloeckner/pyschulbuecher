%import db.orga as orga

%include("header")
<h1>Übersicht Klasse {{grade}}{{tag}}</h1>
<a href="/admin/classes/edit/{{orga.db.Class.get(grade=grade, tag=tag).id}}">Bearbeiten</a>

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
