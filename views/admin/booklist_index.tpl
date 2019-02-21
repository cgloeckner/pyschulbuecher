%include("header")

<h1>Bücherzettel</h1>

<a href="/admin/booklist/generate" target="_blank">Bücherzettel erstellen</a> &dash;
<a href="/admin/requestlist/generate" target="_blank">Erfassungsliste erstellen</a>

<hr />

%if full:
<a href="/admin/booklist/download/BücherzettelKomplett.pdf">als eine Datei</a>
%end

<table>
	<tr>
		<th>Datei</th>
		<th>Größe</th>
		<th>Änderung</th>
	</tr>
%for d in data:
	<tr>
		<td><a href="/admin/booklist/download/{{d['name']}}" target="_blank">{{d['title']}}</a></td>
		<td>{{int(d['size'] / 1024)}}KB</td>
		<td>{{d['date']}}</td>
	</tr>
%end
</table>

%include("footer")
