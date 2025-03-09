%from app.db import orga_queries

%include("header")
<h1>Übersicht Klassenstufe {{grade}}</h1>

<table class="small">
	<tr>
		<th>Klasse</th>
		<th>Klassenlehrer</th>
		<th>Anzahl Schüler</th>
	</tr>
%for tag in orga_queries.get_class_tags(grade):
	%c = orga_queries.db.Class.get(grade=grade, tag=tag)
	<tr>
		<td><a href="/classes/{{grade}}/{{tag}}">{{c.to_string()}}</a></td>
	%if c.teacher is None:
		<td>nicht zugewiesen</td>
	%else:
		<td>{{c.teacher.tag.upper()}}</td>
	%end
		<td>{{c.student.count()}}</td>
	</tr>
%end
</table>

%include("footer")
