%import db.orga as orga

%include("header")
<h1>Klassenverwaltung</h1>

<table>
	<tr>
		<th></th>
		<th>Klasse</th>
		<th>Klassenlehrer</th>
		<th>Anzahl Schüler</th>
	</tr>
%for grade in orga.getClassGrades():
	%for tag in orga.getClassTags(grade):
		%c = orga.db.Class.get(grade=grade, tag=tag)
	<tr>
		<td><a class="edit" href="/admin/classes/edit/{{c.id}}">&#9998;</a></td>
		<td><a href="/classes/{{grade}}/{{tag}}">{{c.toString()}}</a></td>
		%if c.teacher is None:
		<td>nicht zugewiesen</td>
		%else:
		<td>{{c.teacher.tag.upper()}}</td>
		%end
		<td><a href="/admin/classes/move/{{c.id}}">{{c.student.count()}}</a></td>
	</tr>
	%end
%end
</table>

<hr />

<b>Anzahl Klassen: {{orga.getClassesCount()}}</b>

<hr />

<h2>Neue Klasse hinzufügen</h2>

<h2>Excel-Export</h2>

Klassenkürzel (z.B. "08B" oder "11ABC")
<form action="/admin/classes/add" id="classes" method="post">
	<textarea rows="5" cols="50" name="data" form="classes"></textarea><br />
	<input type="submit" value="Hinzufügen" />
</form>

%include("footer")
