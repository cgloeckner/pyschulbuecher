%include("header")
<h1>Verlag bearbeiten</h1>

<form action="/admin/publishers/edit/{{p.id}}" id="publishers" method="post">
	Name: <input type="text" name="name" value="{{p.name}}" /><br />
	<input type="submit" value="Ändern" />
</form>

<form action="/admin/publishers/delete/{{p.id}}" id="drop" method="post">
	<input type="submit" value="Löschen" />
</form>

%include("footer")
