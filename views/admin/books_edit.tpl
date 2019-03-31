%from db import books
%from db.orm import Currency
%from utils import bool2checked

%include("header")
<h1>Buch bearbeiten</h1>

<form action="/admin/books/edit/{{b.id}}" id="books" method="post">
	<table class="simple">
		<tr>
			<td>Titel</td>
			<td><input type="text" name="title" value="{{b.title}}" /></td>
		</tr>
		<tr>
			<td>ISBN</td>
			<td><input type="text" name="isbn" value="{{b.isbn}}" /></td>
		</tr>
		<tr>
			<td>Preis</td>
			<td><input type="text" name="price" value="{{Currency.toString(b.price)}}" />€</td>
		</tr>
		<tr>
			<td>Verlag</td>
			<td><select name="publisher_id">
%for p in books.getPublishers():
				<option value="{{p.id}}"\\
%if p.id == b.publisher.id:
 selected\\
%end
>{{p.name}}</option>
%end
			</select></td>
		</tr>
		<tr>
			<td>Bestand</td>
			<td><input type="text" name="stock" value="{{b.stock}}" /></td>
		</tr>
		<tr>
			<td>ab Klasse</td>
			<td><input type="text" name="inGrade" value="{{b.inGrade}}" /></td>
		</tr>
		<tr>
			<td>bis Klasse</td>
			<td><input type="text" name="outGrade" value="{{b.outGrade}}" /></td>
		</tr>
		<tr>
			<td>Fach</td>
			<td><select name="subject_id">
				<option value=""\\
%if b.subject is None:
 selected\\
%end
>verschiedene</option>
%for s in books.getSubjects():
				<option value="{{s.id}}"\\
%if b.subject is not None and b.subject.id == s.id:
 selected\\
%end
>{{s.tag}} ({{s.name}})</option>
%end
			</select></td>
		</tr>
		<tr>
			<td></td>
			<td><input type="checkbox" name="novices" id="novices" {{bool2checked(b.novices)}} />
				<label for="novices">für gA geeignet</label></td>
		</tr>
		<tr>
			<td></td>
			<td><input type="checkbox" name="advanced" id="advanced" {{bool2checked(b.advanced)}} />
				<label for="advanced">für eA geeignet</label><td>
		</tr>
		<tr>
			<td></td>
			<td><input type="checkbox" name="workbook" id="workbook" {{bool2checked(b.workbook)}} />
				<label for="workbook">ist Arbeitsheft</label></td>
		</tr>
		<tr>
			<td></td>
			<td><input type="checkbox" name="classsets" id="classsets" {{bool2checked(b.classsets)}} />
				<label for="classsets">als Klassensätze</label></td>
		</tr>
		<tr>
			<td></td>
			<td><input type="checkbox" name="for_loan" id="for_loan" {{bool2checked(b.for_loan)}} />
				<label for="for_loan">auf Bücherzettel</label></td>
		</tr>
		<tr>
			<td>Kommentare:</td>
			<td><input type="text" name="comment" value="{{b.comment}}" /></td>
		</tr>
		<tr>
			<td></td>
			<td><input type="submit" value="Ändern" /></td>
		</tr>
	</table>
</form>

<form action="/admin/books/delete/{{b.id}}" id="drop" method="post">
	<input type="submit" value="Löschen" />
</form>

%include("footer")
