%include("header")
<h1>Fach bearbeiten</h1>

<form action="/admin/subjects/edit/{{s.id}}" id="subjects" method="post">
	Kürzel: <input type="text" name="tag" value="{{s.tag}}" /><br />
	Name: <input type="text" name="name" value="{{s.name}}" /><br />
	<input type="submit" value="Ändern" />
</form>

<form action="/admin/subjects/delete/{{s.id}}" id="drop" method="post">
	<input type="submit" value="Löschen" />
</form>

%include("footer")
