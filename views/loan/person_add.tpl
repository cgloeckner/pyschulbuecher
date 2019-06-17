%from db import orga, books

%include("header")
<h1>Leihexemplar hinzufügen</h1>

<form action="/loan/person/{{id}}/add" id="loan" method="post">
	<table>
		<tr>
			<td>Fach</td>
			<td><select name="subject_id" id="subject_id" onChange="queryBooks();">
				<option value="" selected>verschiedene</option>
%for s in books.getSubjects():
				<option value="{{s.id}}">{{s.tag}} ({{s.name}})</option>
%end
			</select></td>
		</tr>
		<tr>
			<td>Klassenstufe</td>
			<td><select name="grade_id" id="grade_id" onChange="queryBooks();">
				<option value="" selected>beliebig</option>
%for grade in orga.getClassGrades(regular=True):
				<option value="{{grade}}">Klasse {{grade}}</option>
%end
			</select></td>
		</tr>
		<tr>
			<td>Buch</td>
			<td><select name="book_id" id="book_id" onChange="queryCount({{id}});">
%for b in bks:
				<option value="{{b.id}}">{{b.toString()}}</option>
%end			
			</select></td>
		</tr>
		<tr>
			<td>Anzahl</td>
			<td><input type="text" name="count" id="count" value="" /></td>
		</tr>
		<tr>
			<td></td>
			<td><input type="submit" value="Ausleihen" /></td>
		</tr>
	</table>
</form>

<a href="/loan/person/{{id}}">zurück</a>

%include("footer")
