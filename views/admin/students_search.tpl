%import db.orga as orga

%include("header")
<h1>Schülersuche</h1>

<table>
	<tr>
		<th>Name</th>
		<th>Vorname</th>
		<th>Klasse</th>
		<th></th>
	</tr>
%for s in data:
	<tr>
		<td>{{s.person.name}}</td>
		<td>{{s.person.firstname}}</td>
		<td><a href="/classes/{{s.class_.grade}}/{{s.class_.tag}}">{{s.class_.toString()}}</a></td>
		<td>Bearbeiten</a></td>
	</tr>
%end
</table>

%include("footer")
