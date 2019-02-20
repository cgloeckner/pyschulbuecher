%from db import orga

%include("header")
<h1>Klasse bearbeiten</h1>

<form action="/admin/classes/edit/{{c.id}}" id="classes" method="post">
	<table>
		<tr>
			<td>Klassenstufe</td>
			<td><select name="grade">
%for grade in range(5, 12+1):
				<option value="{{grade}}"\\
	%if c.grade == grade:
 selected\\
 	%end
>{{grade}}. Klasse</option>
%end			
				</select></td>
		</tr>
		<tr>
			<td>Kürzel</td>
			<td><input type="text" name="tag" value="{{c.tag}}" /></td>
		</tr>
		<tr>
			<td>Klassenlehrer</td>
			<td>TODO: SELECT-OPTION WITH TEACHER LIST</td>
		</tr>
		<tr>
			<td></td>
			<td><input type="submit" value="Ändern" /></td>
		</tr>
	</table>
</form>

<hr />

<form action="/admin/classes/delete/{{c.id}}" id="drop" method="post">
	<input type="submit" value="Löschen" />
</form>

%include("footer")
