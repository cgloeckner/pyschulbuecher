%import db.books as books
%import db.orga as orga
%from utils import bool2str
%from db.orm import Currency

%include("header")

%year = int(s.data['general']['school_year'])
<h1>Bedarfsbericht für Schuljahr {{year}}/{{year+1}}</h1>

<h2>Schülerzahlen Sekundarstufe I</h2>

<form action="/admin/demand" id="demand" method="post">

<table class="books">
	<tr>
		<th class="rotate">Klassenstufe</th>
		<th class="rotate">Gesamtzahl Schüler</th>
	%for sub in books.getSubjects(elective=True):
		<th>{{sub.tag}}</th>
	%end
	</tr>
%for grade in range(5, 10+1):
	<tr>
		<td>{{grade}}</td>
		<td id="{{grade}}_status">{{orga.getStudentsCount(grade-1)}}</td>
	%for sub in books.getSubjects(elective=True):
		<td><input type="text" class="short" maxLength="3" name="{{grade}}_{{sub.tag}}" value="{{students[str(grade)][sub.tag]}}" /></td>
	%end
	</tr>
%end
</table>

<h2>Schülerzahlen Sekundarstufe II</h2>

%subjects = books.getSubjects()
<table class="books">
	<tr>
		<th>Kurs</th>
%for s in subjects:
		<th>{{s.tag}}</th>
%end
	</tr>
%for grade in [11, 12]:
	%for level in ['novices', 'advanced']:
	<tr>
		<td>{{grade}} {{'gA' if level == 'novices' else 'eA'}}</td>
		%for s in subjects:
		<td><input type="text" class="short" maxLength="3" name="{{grade}}_{{s.tag}}_{{level}}" value="{{students[str(grade)][s.tag][level]}}"  /></td>
		%end
	</tr>
	%end
%end
</table>

<br />

<input type="submit" value="Bedarfsbericht erstellen" />

</form>

%include("footer")
