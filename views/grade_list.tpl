%include("header")
<h1>Klassenübersicht</h1>
<table>
%for grade in all_classes:
	<tr>
	%for tag in all_classes[grade]:
		<td><a href="/classes/{{grade}}/{{tag}}">{{grade}}{{tag}}</a></td>
	%end
	</tr>
%end
</table>
%include("footer")
