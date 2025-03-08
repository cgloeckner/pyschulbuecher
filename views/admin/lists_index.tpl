%include("header")

<h1>Ausdrucke</h1>

%remote_latex = settings.data['hosting']['remote_latex']
<p>
	<b>LaTeX-Compiler:</b> 
%if remote_latex == '':
	<i>lokal</i>
%else:
	<a href="{{remote_latex}}" target="_blank">{{remote_latex}}</a>
%end
</p>

<h2>Bedarf</h2>
<ul>
	<li><a href="/admin/lists/generate/councils" target="_blank">Bedarf Fachschaften</a></li>
	<li><a href="/admin/lists/generate/inventory" target="_blank">Inventarbericht</a></li>
	<li><a href="/admin/preview/booklist" target="_blank">Bücherzettel</a></li>
	<li><a href="/admin/lists/generate/requestlist" target="_blank">Erfassungsliste für Bücherzettel</a></li>  
    <li><a href="/admin/lists/generate/planner/next" target="_blank">Übersicht Schulplaner (nächstes Schuljahr)</a></li>
    <li><a href="/admin/lists/generate/planner/current" target="_blank">Übersicht Schulplaner (aktuelles Schuljahr)</a></li>
</ul>

<h2>Bücherausgabe</h2>
<ul>	<li><a href="/admin/lists/generate/requestloan" target="_blank">Büchervorschau (nächstes Schuljahr, gemäß Bücherzettel)</a></li>
	<li><a href="/admin/lists/generate/bookloan" target="_blank">Bückerausgabe (aktuelles Schuljahr, gemäß Bücherzettel)</a></li>
</ul>

<h2>Leihberichte</h2>
<ul>
	<li><a href="/admin/lists/generate/studentloans" target="_blank">Leihübersicht (Auswahl Schüler)</a></li>
	<li><a href="/admin/lists/generate/teacherloans" target="_blank">Leihübersicht (alle Lehrer)</a></li>
	<li><a href="/admin/lists/generate/classsets" target="_blank">Klassensätze aller Lehrer</a></li>
</ul>

<h2>Bücherrückgabe</h2>
<ul>
	<li><a href="/admin/lists/generate/returnlist/normal" target="_blank">Ausstehende Bücher (alle Klassen)</li>
	<li><a href="/admin/lists/generate/loanlist/12" target="_blank">Ausstehende Bücher (nach Schülern Klasse 12)</li>
	<li><a href="/admin/lists/generate/returnlist/tooLate" target="_blank">stark verspätete Bücher (alle Klassen)</li>
	<li><a href="/admin/lists/generate/bookreturn" target="_blank">Bücherrückgabe (Listen und Übersichtszettel)</a></li>
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
