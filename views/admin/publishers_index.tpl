%import db.books as books

%include("header")
<h1>Übersicht Verlage</h1>

<table>
	<tr>
		<th>Name</th>
		<th></th>
	</tr>
%for s in books.getPublishers():
	<tr>
		<td>{{s.name}}</td>
		<td><a href="/admin/publishers/edit/{{s.id}}">Bearbeiten</a></td>
	</tr>
%end

%if len(books.getPublishers()) == 0:
	<tr>
		<td colspan="2">keine Verläge vorhanden</td>
	</tr>
%end
</table>

<h2>Neue Verläge hinzufügen</h2>
<form action="/admin/publishers/add" id="publishers" method="post">
	<textarea rows="5" cols="50" name="data" form="publishers"></textarea><br />
	<input type="submit" value="Hinzufügen" />
</form>

%include("footer")
