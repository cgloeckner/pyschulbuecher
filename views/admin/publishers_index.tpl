%import db.books as books

%include("header")
<h1>Übersicht Verlage</h1>

<ul>
%for s in books.getPublishers():
	<li><a href="/admin/publishers/edit/{{s.id}}">{{s.name}}</a></li>
%end
</ul>

%if len(books.getPublishers()) == 0:
	<tr>
		<td colspan="2">keine Verlage vorhanden</td>
	</tr>
%end
</table>

<h2>Neue Verlage hinzufügen</h2>
<form action="/admin/publishers/add" id="publishers" method="post">
	<textarea rows="5" cols="50" name="data" form="publishers"></textarea><br />
	<input type="submit" value="Hinzufügen" />
</form>

%include("footer")
