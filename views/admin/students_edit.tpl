%from app.db import orga_queries as orga

%include("header")
<h1>Schüler bearbeiten</h1>

<form action="/admin/students/edit/{{s.id}}" id="students" method="post">
	<table>
		<tr>
			<td>Name</td>
			<td><input type="text" name="name" value="{{s.person.name}}" /></td>
		</tr>
		<tr>
			<td>Vorname</td>
			<td><input type="text" name="firstname" value="{{s.person.firstname}}" /></td>
		</tr>
		<tr>
			<td>Klasse</td>
			<td><select name="class_id">
%for grade in orga.get_class_grades():
	%for tag in orga.get_class_tags(grade):
		%c = orga.db.Class.get(grade=grade, tag=tag)
				<option value="{{c.id}}"\\
		%if s.class_ == c:
 selected\\
		%end
>{{c.to_string()}}</option>
	%end
%end
			</select></td>
		</tr>
		<tr>
			<td></td>
			<td><input type="submit" value="Ändern" /></td>
		</tr>
	</table>
</form>

<hr />

<form action="/admin/students/delete/{{s.id}}" id="drop" method="post">
	<input type="submit" value="Löschen" />
</form>

%include("footer")
