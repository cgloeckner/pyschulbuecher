%import db.books as books
%from utils import bool2str
%from db.orm import Currency

%include("header")
<h1>Übersicht Bücher</h1>

<a href="/admin/demand" target="_blank">Bedarfsbericht</a>

<br /><br />


<!-- Single API -->

<h2>Neue Bücher hinzufügen</h2>

<form action="/admin/books/addSingle" id="books" method="post">
<b>Pflichtfelder</b> - <i>optional</i>
	<table class="simple">
		<tr>
			<td><b>Titel</b></td>
			<td><input type="text" name="title" value="" /></td>
		</tr>
		<tr>
			<td><i>ISBN</i></td>
			<td><input type="text" name="isbn" value="" /></td>
		</tr>
		<tr>
			<td><i>Preis</i></td>
			<td><input type="text" name="price" value="" />€</td>
		</tr>
		<tr>
			<td><b>Verlag</b></td>
			<td><select name="publisher_id">
%for i, p in enumerate(books.getPublishers()):
				<option value="{{p.id}}"\\
%if i == 0:
 selected\\
%end
>{{p.name}}</option>
%end
			</select></td>
		</tr>
		<tr>
			<td><b>ab Klasse</b></td>
			<td><input type="text" name="inGrade" value="" /></td>
		</tr>
		<tr>
			<td><b>bis Klasse</b></td>
			<td><input type="text" name="outGrade" value="" /></td>
		</tr>
		<tr>
			<td><b>Fach</b></td>
			<td><select name="subject_id">
				<option value="">verschiedene</option>
%for s in books.getSubjects():
				<option value="{{s.id}}">{{s.tag}} ({{s.name}})</option>
%end
			</select></td>
		</tr>
		<tr>
			<td></td>
			<td><input type="checkbox" name="novices" id="novices" />
				<label for="novices"><i>für gA geeignet</i></label></td>
		</tr>
		<tr>
			<td></td>
			<td><input type="checkbox" name="advanced" id="advanced" />
				<label for="advanced"><i>für eA geeignet</i></label><td>
		</tr>
		<tr>
			<td></td>
			<td><input type="checkbox" name="workbook" id="workbook" />
				<label for="workbook"><i>ist Arbeitsheft</i></label></td>
		</tr>
		<tr>
			<td></td>
			<td><input type="checkbox" name="classsets" id="classsets" />
				<label for="classsets"><i>als Klassensätze</i></label></td>
		</tr>
		<tr>
			<td></td>
			<td><input type="checkbox" name="for_loan" id="for_loan" checked="checked" />
				<label for="for_loan"><i>auf Bücherzettel</i></label></td>
		</tr>
		<tr>
			<td><i>Kommentare</i></td>
			<td><input type="text" name="comment" value="" /></td>
		</tr>
		<tr>
			<td></td>
			<td><input type="submit" value="Hinzufügen" /></td>
		</tr>
	</table>
</form>

<hr />

<!-- Batch API -->

<h2>Excel-Export</h2>

<i>Titel &lt;tab&gt; ISBN &lt;tab&gt; Preis &lt;tab&gt; Verlag &lt;tab&gt; ab Klasse &lt;tab&gt; bis Klasse &lt;tab&gt; Fach &lt;tab&gt; für gA &lt;tab&gt; für EA &lt;tab&gt; AH? &lt;tab&gt; Klassensatz? &lt;tab&gt; Kommentar</i>
<form action="/admin/books/add" id="books" method="post">
	<textarea rows="5" cols="50" name="data" form="books"></textarea><br />
	<input type="submit" value="Hinzufügen" />
</form>

<hr />

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

%include("footer")
