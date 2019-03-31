%import db.orga as orga

<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8"> 
	<script src="/static/jquery-3.3.1.min.js"></script>
	<script src="/static/admin.js"></script>
	<link rel="stylesheet" type="text/css" href="/static/normalize.css">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
	<link rel="stylesheet" type="text/css" href="/static/layout.css">
	<link rel="stylesheet" type="text/css" href="/static/navigation.css">
	<title>Schulbuchverwaltung</title>
</head>

<body>
<div class="navbar">
	<div class="dropdown">
		<button class="dropbtn"><a href="/">Startseite</a>
		</button>
	</div>
	<div class="dropdown">
		<button class="dropbtn"><a href="/classes">Klassen</a>
			<i class="fa fa-caret-down"></i>
		</button>
		<div class="dropdown-content">
%for grade in orga.getClassGrades():
	%if grade == 4:
			<a href="/classes/{{grade}}">zukünftige 5</a>
	%else:
			<a href="/classes/{{grade}}">{{grade}}. Klasse</a>
	%end
%end
		</div>
	</div>
	
	<div class="dropdown">
		<button class="dropbtn"><a href="/admin/settings">Verwaltung</a>
			<i class="fa fa-caret-down"></i>
		</button>
		<div class="dropdown-content">
			<a href="/admin/subjects">Fächer</a>
			<a href="/admin/publishers">Verlage</a>
			<a href="/admin/books">Bücher</a>
			<a href="/admin/teachers">Lehrer</a>
			<a href="/admin/classes">Klassen</a>
			<a href="/admin/students">Schüler</a>
			<a href="/admin/lists">Listen</a>
			<a href="/admin/settings">Einstellungen</a>
		</div>
	</div>
	
	<span class="info">Schulbuchverwaltung - v0.1-alpha</span>
</div>
<div class="content">

