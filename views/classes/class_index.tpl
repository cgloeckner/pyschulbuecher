%from app.db import orga_queries as orga

%include("header")
<h1>Klassenübersicht</h1>

<table class="small">
%for grade in orga.get_class_grades():
	<tr>
		<th>\\
	%if grade == 4:
zukünftige 5\\
	%else:
Klasse {{grade}}\\
	%end
</th>
	%for tag in orga.get_class_tags(grade):
		%c = orga.db.Class.get(grade=grade, tag=tag)
		<td><a href="/classes/{{grade}}/{{tag}}">{{c.to_string()}}</a></td>
	%end
	</tr>
%end
</table>

%include("footer")
