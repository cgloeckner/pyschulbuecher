%import db.orga as orga

%include("header")
%c = orga.db.Class.get(grade=grade, tag=tag)
<h1>Übersicht Klasse {{c.toString()}}</h1>
<a href="/admin/classes/edit/{{c.id}}">Bearbeiten</a> &dash;
<a href="/classes/requests/{{grade}}/{{tag}}">Bücherzettel für Klasse {{grade+1}}</a>

%i = 1
<table>
	<tr>
		<th>Nr.</th>
		<th>Name, Vorname</th>
		<th>Freiexemplare<br />aktuell</th>
		<th>Freiexemplare<br />Klasse {{grade+1}}</th>
	</tr>
%for s in orga.getStudentsIn(grade, tag):
	<tr>
		<td>{{i}}</td>
%i += 1
		<td><a href="/admin/students/edit/{{s.id}}">{{s.person.name}}, {{s.person.firstname}}</a></td>
		<td>{{len(s.person.loan)}}</td>
		<td>{{len(s.person.request)}}</td>
	</tr>
%end
</table>

%include("footer")
