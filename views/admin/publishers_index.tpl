%import db.books as books

%include("header")
<h1>Übersicht Verlage</h1>

<ul>
%for s in books.getPublishers():
	<li><a class="edit" href="/admin/publishers/edit/{{s.id}}">&#9998;</a> {{s.name}}</li>
%end
</ul>

%if len(books.getPublishers()) == 0:
<p>keine Verlage vorhanden</p>
%end

<h2>Neue Verlage hinzufügen</h2>
<form action="/admin/publishers/add" id="publishers" method="post">
	<textarea rows="5" cols="50" name="data" form="publishers"></textarea><br />
	<input type="submit" value="Hinzufügen" />
</form>

%include("footer")
