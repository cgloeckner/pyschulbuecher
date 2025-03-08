%from app.db import orga_queries as orga
%from app import Settings

%s = Settings()
%try:
%	with open('settings.ini') as h:
%		s.load_from(h)
%	end
%	year = int(s.data['general']['school_year'])
%except FileNotFoundError:
%	# keep default values
%	year = 0
%end
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8"> 
	<script src="/static/jquery-3.3.1.min.js"></script>
	<script src="/static/admin.js"></script>
	<script src="/static/classes.js"></script>
	<script src="/static/loans.js"></script>
	<link rel="stylesheet" type="text/css" href="/static/normalize.css">
	<link rel="stylesheet" type="text/css" href="/static/layout.css">
	<link rel="stylesheet" type="text/css" href="/static/navigation.css">
	<link rel="stylesheet" type="text/css" href="/static/subnavigation.css">
	<title>Schulbuchverwaltung {{year}}/{{year+1}}</title>
</head>

<body>
<div class="navbar">
	<div class="dropdown">
		<button class="dropbtn"><a href="/">Startseite</a>
		</button>
	</div>
	<div class="dropdown">
		<button class="dropbtn"><a href="/classes">Klassen <span class="downarrow">&#9660;</span></a>
		</button>
		<div class="dropdown-content">
%for grade in orga.get_class_grades():
	%if grade == 4:
			<a href="/classes/{{grade}}">zukünftige 5</a>
	%else:
			<div class="submenu">
				<a href="/classes/{{grade}}">{{grade}}. Klasse <span class="rightarrow">&#9654;</span></a>
				<div class="dropdown-content">
	%for tag in orga.get_class_tags(grade):
		%c = orga.db.Class.get(grade=grade, tag=tag)
					<a href="/classes/{{grade}}/{{tag}}">{{c.to_string()}}</a>
	%end
				</div>
			</div>
	%end
%end
		</div>
	</div>
	
	<div class="dropdown">
		<button class="dropbtn"><a href="/admin/settings">Verwaltung <span class="downarrow">&#9660;</span></a>
		</button>
		<div class="dropdown-content">
			<div class="submenu">
				<span class="section">Allgemein <span class="rightarrow">&#9654;</span></span>
				<div class="dropdown-content">
					<a href="/admin/subjects">Fächer</a>
					<a href="/admin/publishers">Verlage</a>
				</div>
			</div>
			<div class="submenu">
				<span class="section">Organisation <span class="rightarrow">&#9654;</span></span>
				<div class="dropdown-content">
					<a href="/admin/teachers">Lehrer</a>
					<a href="/admin/classes">Klassen</a>
					<a href="/admin/students">Schüler</a>
				</div>
			</div>
			<a href="/admin/books">Bücher</a>
			<a href="/admin/lists">Ausdrucke</a>
			<a href="/admin/settings">Einstellungen</a>
		</div>
	</div>
	
	<span class="info">Schulbuchverwaltung ({{year}}/{{year+1}}) - v0.2.1</span>
</div>
<div class="content">

