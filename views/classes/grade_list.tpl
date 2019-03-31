%include("header")
<h1>Klassenübersicht</h1>

<table class="small">
%for grade in all_classes:
	<tr>
		<th>\\
	%if grade == 4:
zukünftige 5\\
	%else:
Klassenstufe {{grade}}\\
	%end
</th>
	%for tag in all_classes[grade]:
		<td><a href="/classes/{{grade}}/{{tag}}">{{tag}}</a></td>
	%end
	</tr>
%end
</table>

%include("footer")
