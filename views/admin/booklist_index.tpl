%include("header")

<h1>Bücherzettel</h1>

<a href="/admin/booklist/generate" target="_blank">generieren</a>

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
		<td><a href="/admin/booklist/download/{{d['name']}}" target="_blank">Klasse {{d['grade']}}
	%if d['new']:
 (Neuzugänge)
	%end
		</a></td>
		<td>{{int(d['size'] / 1024)}}KB</td>
		<td>{{d['date']}}</td>
	</tr>
%end
</table>

%include("footer")
