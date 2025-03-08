%from app.db import orga_queries as orga

%include("header")
<h1>Schüler verwalten</h1>

<form action="/admin/students/search" id="search" method="post">
<table class="simple">
	<tr>
		<td>Name</td>
		<td><input type="text" name="name" /></td>
	</tr>
	<tr>
		<td>Vorname</td>
		<td><input type="text" name="firstname" /></td>
	</tr>
	<tr>
		<td></td>
		<td><input type="submit" value="Suchen" /></td>
	</tr>
</table>
</form>

<br />

<b>Anzahl Schüler: {{orga.get_student_count()}}</b>

<hr />

<!-- Single API -->

<h2>Neue Schüler hinzufügen</h2>

<form action="/admin/students/addSingle" id="student" method="post">
<table class="simple">
	<tr>
		<td>Name</td>
		<td><input type="text" name="name" /></td>
	</tr>
	<tr>
		<td>Vorname</td>
		<td><input type="text" name="firstname" /></td>
	</tr>
	<tr>
		<td>Klasse</td>
		<td><select name="class_id">
%for grade in orga.get_class_grades():
	%for tag in orga.get_class_tags(grade):
		%c = orga.db.Class.get(grade=grade, tag=tag)
				<option value="{{c.id}}">{{c.to_string()}}</option>
	%end
%end
			</select></td>
	</tr>
	<tr>
		<td></td>
		<td><input type="submit" value="Hinzufügen" /></td>
	</tr>
</table>
</form>

<hr />

<!-- Batch API -->

<h2>Excel-Export:</h2>
<i>Klasse &lt;tab&gt; Name &lt;tab&gt; Vorname</i>
wobei Klasse "08B" oder "11ABC"
<input type="button" onClick="addTab();" value="TAB" />
<form action="/admin/students/add" id="students" method="post">
	<textarea rows="5" cols="50" name="data" form="students"></textarea><br />
	<input type="submit" value="Hinzufügen" />
</form>

%include("footer")
