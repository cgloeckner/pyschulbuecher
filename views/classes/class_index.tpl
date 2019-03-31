%import db.orga as orga

%include("header")
<h1>Klassenübersicht</h1>

<table class="small">
%for grade in orga.getClassGrades():
	<tr>
		<th>\\
	%if grade == 4:
zukünftige 5\\
	%else:
Klasse {{grade}}\\
	%end
</th>
	%for tag in orga.getClassTags(grade):
		%c = orga.db.Class.get(grade=grade, tag=tag)
		<td><a href="/classes/{{grade}}/{{tag}}">{{c.toString()}}</a></td>
	%end
	</tr>
%end
</table>

%include("footer")
