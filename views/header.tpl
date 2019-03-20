%import db.orga as orga

<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8"> 
	<script src="/static/jquery-3.3.1.min.js"></script>
	<script src="/static/admin.js"></script> 
	<title>Schulbuchverwaltung</title>
<style>
body {
	background-color: white;
}

th.rotate, td.rotate {
	writing-mode: sideways-lr;
	width: 25px;
}

th.gray, td.gray {
	background-color: rgb(200, 200, 200);
}

input[type=checkbox].selection {
	transform: scale(1.5);
}

input[type=text].selection {
	width: 15px;
}

td.critical {
	font-weight: bold;
	background-color: red;
}

td.low {
	font-weight: bold;
	background-color: orange;
}

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
	<span><a href="/admin/settings">Verwaltung</a>
		<ul>
			<li><a href="/admin/subjects">Fächer</a></li>
			<li><a href="/admin/publishers">Verlage</a></li>
			<li><a href="/admin/books">Bücher</a></li>
			<li><a href="/admin/teachers">Lehrer</a></li>
			<li><a href="/admin/classes">Klassen</a></li>
			<li><a href="/admin/students">Schüler</a></li>
			<li><a href="/admin/lists">Listen</a></li>
			<li><a href="/admin/settings">Einstellungen</a></li>
		</ul>
	</span>
</div>
<div class="content">

