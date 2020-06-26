%include("header")

<h1>Ausdrucke</h1>

<a href="/admin/lists/generate/teacherloans" target="_blank">Leihen (Lehrer)</a>
<a href="/admin/lists/generate/studentloans" target="_blank">Leihen (Schüler)</a>
<hr />
Aktuelles Schuljahr:
<a href="/admin/lists/generate/bookreturn" target="_blank">Bücherrückgabe</a>
<a href="/admin/lists/generate/bookpending" target="_blank">Ausstehende Bücher Kl. 12</a>
<a href="/admin/lists/generate/classlist" target="_blank">Klassenliste</a>
<hr />
Neues Schuljahr:
<a href="/admin/lists/generate/councils" target="_blank">Bedarf Fachschaften</a> &dash;
<a href="/admin/preview/booklist" target="_blank">Bücherzettel</a> &dash;
<a href="/admin/lists/generate/requestlist" target="_blank">Erfassungsliste</a> &dash;
<a href="/admin/lists/generate/bookloan" target="_blank">Bückerausgabe (aktuelles Schuljahr)</a>
<a href="/admin/lists/generate/requestloan" target="_blank">Bückerausgabe (nächstes Schuljahr)</a>
<hr />

<a href="/admin/lists/generate/db_dump" target="_blank">Datenbank nach Excel exportieren</a>

<a href="file://{{export}}">Export-Verzeichnis</a> 

%#if full:
%#<a href="/admin/booklist/download/BücherzettelKomplett.pdf">als eine Datei</a>
%#end

%#<table>
%#	<tr>
%#		<th>Datei</th>
%#		<th>Größe</th>
%#		<th>Änderung</th>
%#	</tr>
%#for d in data:
%#	<tr>
%#		<td><a href="/admin/lists/download/{{d['name']}}" target="_blank">{{d['title']}}</a></td>
%#		<td>{{int(d['size'] / 1024)}}KB</td>
%#		<td>{{d['date']}}</td>
%#	</tr>
%#end
%#</table>

%include("footer")
