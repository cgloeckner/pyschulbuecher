%import db.orga as orga
%from utils import shortName

%include("header")
<h1>Schülersuche</h1>

<table>
	<tr>
		<th></th>
		<th>Name</th>
		<th>Vorname</th>
		<th>Klasse</th>
		<th>Leihen</th>
	</tr>
%for s in data:
	<tr>
		<td><a class="edit" href="/admin/students/edit/{{s.id}}">&#9998;</a></td>
		<td>{{s.person.name}}</td>
		<td>{{shortName(s.person.firstname)}}</td>
		<td><a href="/classes/{{s.class_.grade}}/{{s.class_.tag}}">{{s.class_.toString()}}</a></td>
		<td><a href="/loan/person/{{s.person.id}}">ansehen</a></td>
	</tr>
%end
</table>

%include("footer")
