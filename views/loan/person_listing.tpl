%include("header")
<h1>Bücherübersicht für {{person.name}}, {{person.firstname}}</h1>

<h3>Leihexemplare</h3>
<table class="small">
	<tr>
		<th>Titel</th>
		<th>Fach</th>
		<th>Jahrgang</th>
		<th>Datum</th>
		<th>Anzahl</th>
	</tr>
	</tr>
%for l in loan:
	<tr>
		<td>{{l.book.title}}</td>
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
%else:
	<tr>
		<td colspan="5">keine</td>
	</tr>
%end
</table>

<h3>Vorgemerkt</h3>

<table class="small">
	<tr>
		<th>Titel</th>
		<th>Fach</th>
		<th>Jahrgang</th>
	</tr>
	</tr>
%for r in request:
	<tr>
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
%else:
	<tr>
		<td colspan="3">keine</td>
	</tr>
%end
</table>

%include("footer")
