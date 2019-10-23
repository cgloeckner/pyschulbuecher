%import db.orga as orga

%include("header")
<h1>Lehrer verwalten</h1>

<table>
	<tr>
		<th></th>
		<th>Kürzel</th>
		<th>Name</th>
		<th>Vorname</th>
		<th>Klasse</th>
		<th>Leihen</th>
	</tr>
%for t in orga.getTeachers():
	<tr>
		<td><a class="edit" href="/admin/teachers/edit/{{t.id}}">&#9998;</a></td>
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
		<td><a href="/loan/person/{{t.person.id}}">ansehen</a></td>
	</tr>
%end
</table>
</form>

<hr />

<h2>Neue Lehrer hinzufügen</h2>

<!-- Single API -->


<form action="/admin/teachers/addSingle" id="teachers" method="post">
	<table>
		<tr>
			<td>Name</td>
			<td><input type="text" name="name" value="" /></td>
		</tr>
		<tr>
			<td>Vorname</td>
			<td><input type="text" name="firstname" value="" /></td>
		</tr>
		<tr>
			<td>Kürzel</td>
			<td><input type="text" name="tag" value=""</td>
		</tr>
		<tr>
			<td></td>
			<td><input type="submit" value="Ändern" /></td>
		</tr>
	</table>
</form>

<hr />

<!-- Batch API -->

<h2>Excel-Export</h2>

<i>Tag &lt;tab&gt; Name &lt;tab&gt; Vorname</i>
<form action="/admin/teachers/add" id="teachers" method="post">
	<textarea rows="5" cols="50" name="data" form="teachers"></textarea><br />
	<input type="submit" value="Hinzufügen" />
</form>

%include("footer")
