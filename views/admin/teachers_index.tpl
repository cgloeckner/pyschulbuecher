%import db.orga as orga

%include("header")
<h1>Lehrer verwalten</h1>

<table>
	<tr>
		<th>Kürzel</th>
		<th>Name</th>
		<th>Vorname</th>
		<th>Klasse</th>
		<th></th>
	</tr>
%for t in orga.getTeachers():
	<tr>
		<td>{{t.tag.upper()}}</td>
		<td>{{t.person.name}}</td>
		<td>{{t.person.firstname}}</td>
		<td>
%if t.class_ is not None:
	<a href="/classes/{{t.class_.grade}}/{{t.class_.tag}}">{{t.class_.toString()}}</a>
%else:
	keine
%end
		</td>
		<td><a href="/admin/teachers/edit/{{t.id}}">Bearbeiten</a></td>
	</tr>
%end
</table>
</form>

<hr />

<h2>Neue Lehrer hinzufügen</h2>
<i>Tag &lt;tab&gt; Name &lt;tab&gt; Vorname</i>
<form action="/admin/teachers/add" id="teachers" method="post">
	<textarea rows="5" cols="50" name="data" form="teachers"></textarea><br />
	<input type="submit" value="Hinzufügen" />
</form>

%include("footer")
