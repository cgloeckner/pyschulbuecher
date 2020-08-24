%include("header")

<h1>Ausdrucke</h1>

<h2>Leihen und Zurückgeben</h2>
<ul>
	<li><a href="/admin/lists/generate/bookloan" target="_blank">Bückerausgabe (aktuelles Schuljahr, gemäß Bücherzettel)</a></li>
	<li><a href="/admin/lists/generate/studentloans" target="_blank">Leihübersicht (Schüler)</a></li>
	<li><a href="/admin/lists/generate/teacherloans" target="_blank">Leihübersicht (Lehrer)</a></li>
	<li><a href="/admin/lists/generate/bookpending" target="_blank">Leihübersicht (Klasse 12, ausstehend)</a></li>
	<li><a href="/admin/lists/generate/bookreturn" target="_blank">Bücherrückgabe (Listen und Übersichtszettel)</a></li>
	<li><a href="/admin/lists/generate/requestloan" target="_blank">Büchervorschau (nächstes Schuljahr, gemäß Bücherzettel)</a></li>
</ul>

<h2>Bedarf</h2>
<ul>
	<li><a href="/admin/lists/generate/councils" target="_blank">Bedarf Fachschaften</a></li>
	<li><a href="/admin/preview/booklist" target="_blank">Bücherzettel</a></li>
	<li><a href="/admin/lists/generate/requestlist" target="_blank">Erfassungsliste</a></li>
</ul>

<h2>Administratives</h2>
<ul>
	<li><a href="/admin/lists/generate/classlist" target="_blank">Klassenliste</a></li>
	<li><a href="/admin/lists/generate/db_dump" target="_blank">Datenbank nach Excel exportieren</a></li>
</ul>

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
