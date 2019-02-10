%import db.orga as orga

%include("header")
<h1>Klassenübersicht</h1>
<table>
%for grade in orga.getClassGrades():
	<tr>
	%for tag in orga.getClassTags(grade):
		<td><a href="/classes/{{grade}}/{{tag}}">{{grade}}{{tag}}</a></td>
	%end
	</tr>
%end
</table>
%include("footer")
