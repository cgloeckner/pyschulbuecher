%import db.books as books
%from utils import bool2str

%include("header")
<h1>Übersicht Fächer</h1>

<table>
	<tr>
		<th>Kürzel</th>
		<th>Fach</th>
		<th>Wahlfach<br />(Sek. I)</th>
	</tr>
%for s in books.getSubjects():
	<tr>
		<td><a href="/admin/subjects/edit/{{s.id}}">{{s.tag}}</a></td>
		<td>{{s.name}}</td>
		<td>{{bool2str(s.elective)}}</td>
	</tr>
%end

%if len(books.getSubjects()) == 0:
	<tr>
		<td colspan="3">keine Fächer vorhanden</td>
	</tr>
%end
</table>

<h2>Neue Fächer hinzufügen</h2>
<i>Kürzel &lt;tab&gt; Name</i>
<form action="/admin/subjects/add" id="subjects" method="post">
	<textarea rows="5" cols="50" name="data" form="subjects"></textarea><br />
	<input type="submit" value="Hinzufügen" />
</form>

%include("footer")
