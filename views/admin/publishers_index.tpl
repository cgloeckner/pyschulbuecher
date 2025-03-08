%from app.db import book_queries as books

%include("header")
<h1>Übersicht Verlage</h1>

<ul>
%for s in books.get_publishers():
	<li><a class="edit" href="/admin/publishers/edit/{{s.id}}">&#9998;</a> {{s.name}}</li>
%end
</ul>

%if len(books.get_publishers()) == 0:
<p>keine Verlage vorhanden</p>
%end

<h2>Neue Verlage hinzufügen</h2>

<!-- Batch API -->

<h2>Excel-Export</h2>

<form action="/admin/publishers/add" id="publishers" method="post">
	<textarea rows="5" cols="50" name="data" form="publishers"></textarea><br />
	<input type="submit" value="Hinzufügen" />
</form>

%include("footer")
