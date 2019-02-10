%import db.books as books
%from utils import bool2str
%from db.orm import Currency

%include("header")
<h1>Übersicht Bücher</h1>

<table>
	<tr>
		<th>Titel</th>
		<th>ISBN</th>
		<th>Preis</th>
		<th>Verlag</th>
		<th>Bestand</th>
		<th>Klassen-<br />stufe</th>
		<th>Fach</th>
		<th>für gA</th>
		<th>für eA</th>
		<th>AH?</th>
		<th>Klassen-<br />satz?</th>
		<th>Kommentar</th>
		<th></th>
	</tr>
%bs = books.getAllBooks()
%for b in bs:
	<tr>
		<td>{{b.title}}</td>
		<td>{{b.isbn}}</td>
	%if b.price is not None:
		<td>{{Currency.toString(b.price)}}€</td>
	%else:
		<td>-</td>
	%end
		<td>{{b.publisher.name}}</td>
		<td>{{b.stock}}</td>
	%if b.inGrade != b.outGrade:
		<td>{{b.inGrade}}-{{b.outGrade}}</td>
	%else:
		<td>{{b.inGrade}}</td>
	%end
	%if b.subject is None:
		<td>-</td>
	%else:
		<td>{{b.subject.tag}}</td>
	%end
		<td>{{bool2str(b.novices)}}</td>
		<td>{{bool2str(b.advanced)}}</td>
		<td>{{bool2str(b.workbook)}}</td>
		<td>{{bool2str(b.classsets)}}</td>
		<td>{{b.comment}}</td>
		<td><a href="/admin/books/edit/{{b.id}}">Bearbeiten</a></td>
	</tr>
%end

%if len(bs) == 0:
	<tr>
		<td colspan="2">keine Bücher vorhanden</td>
	</tr>
%end
</table>

<h2>Neue Bücher hinzufügen</h2>
<i>Titel &lt;tab&gt; ISBN Preis &lt;tab&gt; Verlag &lt;tab&gt; Bestand &lt;tab&gt; ab Klasse &lt;tab&gt; bis Klasse &lt;tab&gt; Fach &lt;tab&gt; für eA &lt;tab&gt; für gA &lt;tab&gt; AH? &lt;tab&gt; Klassensatz? &lt;tab&gt; Kommentar</i>
<form action="/admin/books/add" id="books" method="post">
	<textarea rows="5" cols="50" name="data" form="books"></textarea><br />
	<input type="submit" value="Hinzufügen" />
</form>

%include("footer")
