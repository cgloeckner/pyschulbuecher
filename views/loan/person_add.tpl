%from app.db import orga_queries, book_queries

%include("header")
<h1>Leihexemplar hinzufügen</h1>

<table>
	<tr>
		<td>Fach</td>
		<td><select name="subject_id" id="subject_id">
			<option value="" selected>verschiedene</option>
%for s in book_queries.get_subjects():
			<option value="{{s.id}}">{{s.tag}} ({{s.name}})</option>
%end
		</select></td>
		<td>Klassenstufe</td>
		<td><select name="grade_id" id="grade_id">
%for grade in orga_queries.get_class_grades(regular=True):
			<option value="{{grade}}">Klasse {{grade}}</option>
%end
		</select></td>
	</tr>
	<tr>
		<td colspan="4">
			<input type="checkbox" name="classsets" id="classsets" />
			<label for="classsets">auch Klassensätze</label>
		</td>
	</tr>
	<tr>
		<td></td>
		<td><input type="button" value="anzeigen" onClick="queryBooks({{id}}, 'subject');" /></td>
		<td></td>
		<td><input type="button" value="anzeigen" onClick="queryBooks({{id}}, 'grade');" /></td>
	</tr>
</table>

<div id="books"></div>

<a href="/loan/person/{{id}}">zurück</a>

%include("footer")
