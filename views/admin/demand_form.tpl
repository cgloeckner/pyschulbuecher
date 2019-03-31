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
		<th>Fr</th>
		<th>La</th>
		<th>Ru</th>
		<th>Eth</th>
		<th>eR</th>
	</tr>
%for grade in range(5, 10+1):
	<tr>
		<td>{{grade}}</td>
		<td id="{{grade}}_status">{{orga.getStudentsCount(grade-1)}}</td>
	%# TODO: fix hardcoding
		<td><input type="text" class="short" maxLength="3" name="{{grade}}_Fr" value="{{students[str(grade)]['Fr']}}" /></td>
		<td><input type="text" class="short" maxLength="3" name="{{grade}}_La" value="{{students[str(grade)]['La']}}" /></td>
		<td><input type="text" class="short" maxLength="3" name="{{grade}}_Ru" value="{{students[str(grade)]['Ru']}}" /></td>
		<td><input type="text" class="short" maxLength="3" name="{{grade}}_Eth" value="{{students[str(grade)]['Eth']}}" /></td>
		<td><input type="text" class="short" maxLength="3" name="{{grade}}_eR" value="{{students[str(grade)]['eR']}}" /></td>
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
	%for level in ['gA', 'eA']:
	<tr>
		<td>{{grade}} {{level}}</td>
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
