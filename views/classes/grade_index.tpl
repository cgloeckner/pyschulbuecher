%import db.orga as orga

%include("header")
<h1>Übersicht Klassenstufe {{grade}}</h1>

<table>
	<tr>
		<th>Klasse</th>
		<th>Klassenlehrer</th>
		<th>Anzahl Schüler</th>
	</tr>
%for tag in orga.getClassTags(grade):
	%c = orga.db.Class.get(grade=grade, tag=tag)
	<tr>
		<td><a href="/classes/{{grade}}/{{tag}}">{{c.toString()}}</a></td>
	%if c.teacher is None:
		<td>nicht zugewiesen</td>
	%else:
		<td>{{c.teacher.tag}}</td>
	%end
		<td>{{c.student.count()}}</td>
	</tr>
%end
</table>

%include("footer")
