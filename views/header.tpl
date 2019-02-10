%import db.orga as orga

<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8"> 
	<title>Schulbuchverwaltung</title>
<style>
body {background-color: grey;}
</style>
</head>

<body>
<div class="navi">
	<span><a href="/classes">Klassen</a>
		<ul>
%for grade in orga.getClassGrades():
			<li><a href="/classes/{{grade}}">{{grade}}. Klasse</a></li>
%end
		</ul>
	</span>
	<span><a href="/teachers">Lehrer</a></span>
	<span>Suche</span>
	<span><a href="/admin/settings">Verwaltung</a>
		<ul>
			<li><a href="/admin/subjects">Fächer</a></li>
			<li><a href="/admin/publishers">Verlage</a></li>
			<li><a href="/admin/books">Bücher</a></li>
			<li><a href="/admin/generate_booklist">Bücherzettel erstellen</a></li>
		</ul>
	</span>
</div>
<div class="content">
