%include("header")
<h1>Bücherübersicht für {{person.name}}, {{person.firstname}}</h1>

<h3>Leihexemplare <a class="edit" href="/loan/person/{{person.id}}/add">&#9998;</a></h3>

<form action="/loan/person/{{person.id}}/back" id="loan" method="post">
	<table class="small">
		<tr>
			<td><span class="button" onClick="toggleAll();" title="Auswahl alle Bücher umkehren">↺</span></td>
			<th>Titel</th>
			<th>Fach</th>
			<th>Klassenstufe</th>
			<th>Datum</th>
			<th>Anzahl</th>
		</tr>
%for l in loan:
		<tr>
			<td><input type="checkbox" name="{{l.book.id}}" id="{{l.book.id}}" /></td>		
	%css = ''
	%if person.student is not None and person.student.class_ is not None:
		%if l.book.outGrade < person.student.class_.grade:
			%css = ' class="bookLate"'
		%else:
			%if l.book.outGrade > person.student.class_.grade:
				%css = ' class="bookKeep"'
			%end
		%end
	%end
			<td{{!css}}><label for="{{l.book.id}}">{{l.book.title}}</label></td>
	%if l.book.subject is None:
			<td>versch.</td>
	%else:
			<td>{{l.book.subject.tag}}</td>
	%end
			<td>{{l.book.inGrade}}\\
	%if l.book.outGrade != l.book.inGrade:
-{{l.book.outGrade}}\\
	%end
</td>
			<td>{{l.given}}</td>
			<td>{{l.count}}</td>
		</tr>
%end
%if len(loan) == 0:
		<tr>
			<td colspan="5">keine</td>
		</tr>
%end
		<tr>
			<td colspan="6"><input type="submit" value="Auswahl Zurückgeben" /></td>
		</tr>
	</table>
</form>

<h3>Vorgemerkt</h3>

<table class="small">
	<tr>
		<th>Titel</th>
		<th>Fach</th>
		<th>Klassenstufe</th>
	</tr>
%for r in request:
	<tr>
	%css = ''
	%if person.student is not None:
		%if r.book.outGrade < person.student.class_.grade:
			%css = ' class="bookLate"'
		%else:
			%if r.book.outGrade == person.student.class_.grade:
				%css = ' class="bookPending"'
			%end
		%end
	%end
		<td>{{r.book.title}}</td>
	%if r.book.subject is None:
		<td>versch.</td>
	%else:
		<td>{{r.book.subject.tag}}</td>
	%end
		<td>{{r.book.inGrade}}\\
	%if r.book.outGrade != r.book.inGrade:
-{{r.book.outGrade}}\\
	%end
</td>
	</tr>
%end
%if len(request) == 0:
	<tr>
		<td colspan="3">keine</td>
	</tr>
%end
</table>

%include("footer")
