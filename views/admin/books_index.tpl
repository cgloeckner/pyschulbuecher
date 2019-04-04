%import db.books as books
%from utils import bool2str
%from db.orm import Currency

%include("header")
<h1>Übersicht Bücher</h1>

<a href="/admin/demand" target="_blank">Bedarfsbericht</a>

<br /><br />

<input type="checkbox" id="show_regular" onClick="showBooks('regular');" checked /><label for="show_regular">Lehrbücher</label>
<input type="checkbox" id="show_workbooks" onClick="showBooks('workbook');" checked /><label for="show_workbooks">Arbeitshefte</label>
<input type="checkbox" id="show_classsets" onClick="showBooks('classsets');" checked /><label for="show_classsets">Klassensätze</label>

<br /><br />

%for s in books.getSubjects():
<a href="#{{s.tag}}">{{s.tag}}</a> &nbsp;
%end

<table class="books">
%old = None
%bs = books.orderBooksIndex(books.getAllBooks())
%for b in bs:
	%tag = b.subject.tag if b.subject is not None else 'versch.'
	%if old is None or old != tag:
		%if old is not None:
	<tr>
		<td colspan="14"><hr /><a name="{{tag}}"></a></td>
	</tr>
		%end
		%old = tag
	<tr>
		<th></th>
		<th>Titel</th>
		<th>ISBN</th>
		<th>Preis</th>
		<th>Verlag</th>
		<th class="rotate">Bestand</th>
		<th class="rotate">Klassen-<br />stufen</th>
		<th class="rotate">Fach</th>
		<th class="rotate">für gA</th>
		<th class="rotate">für eA</th>
		<th class="rotate">AH?</th>
		<th class="rotate">Klassen-<br />satz?</th>
		<th class="rotate">auf Bücher-<br>zettel?</th>
		<th>Kommentar</th>
	</tr>	
	%end
	%if b.workbook:
	<tr class="workbook">
	%else:
		%if b.classsets:
	<tr class="classsets">
		%else:
	<tr class="regular">
		%end
	%end
		<td><a class="edit" href="/admin/books/edit/{{b.id}}">&#9998;</a></td>
		<td>{{b.title}}</td>
		<td>{{b.isbn}}</td>
	%if b.price is not None:
		<td>{{Currency.toString(b.price)}}</td>
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
		<td>{{tag}}</td>
	%end
		<td>{{bool2str(b.novices)}}</td>
		<td>{{bool2str(b.advanced)}}</td>
		<td>{{bool2str(b.workbook)}}</td>
		<td>{{bool2str(b.classsets)}}</td>
		<td>{{bool2str(b.for_loan)}}</td>
		<td>{{b.comment}}</td>
	</tr>
%end

%if len(bs) == 0:
	<tr>
		<td colspan="2">keine Bücher vorhanden</td>
	</tr>
%end
</table>

<h2>Neue Bücher hinzufügen</h2>
<i>Titel &lt;tab&gt; ISBN &lt;tab&gt; Preis &lt;tab&gt; Verlag &lt;tab&gt; Bestand &lt;tab&gt; ab Klasse &lt;tab&gt; bis Klasse &lt;tab&gt; Fach &lt;tab&gt; für eA &lt;tab&gt; für gA &lt;tab&gt; AH? &lt;tab&gt; Klassensatz? &lt;tab&gt; Kommentar</i>
<form action="/admin/books/add" id="books" method="post">
	<textarea rows="5" cols="50" name="data" form="books"></textarea><br />
	<input type="submit" value="Hinzufügen" />
</form>

%include("footer")
