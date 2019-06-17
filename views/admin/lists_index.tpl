%include("header")

<h1>Ausdrucke</h1>

Aktuelles Schuljahr:
<a href="/admin/lists/generate/bookreturn" target="_blank">Bücherrückgabe</a>
<a href="/admin/lists/generate/bookpending" target="_blank">Ausstehende Bücher</a>
<hr />
Neues Schuljahr:
<a href="/admin/lists/generate/booklist" target="_blank">Bücherzettel</a> &dash;
<a href="/admin/lists/generate/requestlist" target="_blank">Erfassungsliste</a> &dash;
<a href="/admin/lists/generate/bookloan" target="_blank">Bückerausgabe</a>
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
		<td><a href="/admin/lists/download/{{d['name']}}" target="_blank">{{d['title']}}</a></td>
		<td>{{int(d['size'] / 1024)}}KB</td>
		<td>{{d['date']}}</td>
	</tr>
%end
</table>

%include("footer")
