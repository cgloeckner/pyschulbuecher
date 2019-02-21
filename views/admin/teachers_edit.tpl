%from db import orga

%include("header")
<h1>Lehrer bearbeiten</h1>

<form action="/admin/teachers/edit/{{t.id}}" id="teachers" method="post">
	<table>
		<tr>
			<td>Name</td>
			<td><input type="text" name="name" value="{{t.person.name}}" /></td>
		</tr>
		<tr>
			<td>Vorname</td>
			<td><input type="text" name="firstname" value="{{t.person.firstname}}" /></td>
		</tr>
		<tr>
			<td>Kürzel</td>
			<td><input type="text" name="tag" value="{{t.tag}""</td>
		</tr>
		<tr>
			<td></td>
			<td><input type="submit" value="Ändern" /></td>
		</tr>
	</table>
</form>

<hr />

<form action="/admin/teachers/delete/{{t.id}}" id="drop" method="post">
	<input type="submit" value="Löschen" />
</form>

%include("footer")
