%import db.orga as orga

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

<b>Anzahl Schüler: {{orga.getStudentCount()}}</b>

<hr />

<h2>Neue Schüler hinzufügen</h2>
<i>Klasse &lt;tab&gt; Name &lt;tab&gt; Vorname</i>
wobei Klasse "08B" oder "11ABC"
<form action="/admin/students/add" id="students" method="post">
	<textarea rows="5" cols="50" name="data" form="students"></textarea><br />
	<input type="submit" value="Hinzufügen" />
</form>

%include("footer")
