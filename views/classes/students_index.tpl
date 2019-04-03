%import db.orga as orga
%import db.loans as loans

%include("header")
%c = orga.db.Class.get(grade=grade, tag=tag)
<h1>Bücherübersicht Klasse {{c.toString()}}</h1>
<a href="/admin/classes/edit/{{c.id}}">Bearbeiten</a>

%if grade < 12:
&dash; <a href="/classes/requests/{{grade}}/{{tag}}">Bücherzettel für Klasse {{grade+1}}</a>
%end

<form action="/classes/loans/{{grade}}/{{tag}}" id="requests" method="post">

%count = dict()

<table class="simple">
	<!-- ==================== book titles ==================== //-->
	<tr>
		<th></th>
		<th></th>
		<th></th>
%i = 1
%for b in books:
	%if b.workbook or b.classsets:
		%continue
	%end
	%count[b.id] = 0
		<th class="rotate">{{b.title}}</th>
	%if i % 3 == 0:
		<td></td>
	%end
	%i += 1
%end
	</tr>
	<!-- ==================== subjects titles ==================== //-->
	<tr>
		<th></th>
		<th>Nr.</th>
		<th>Name, Vorname</th>
%i = 1
%for b in books:
	%if b.workbook or b.classsets:
		%continue
	%end
	<td class="rotate">\\
	%i += 1
	%if b.subject is not None:
{{b.subject.tag}} \\
	%end
	%if b.advanced and not b.novices:
 (eA) \\
	%elif b.novices and not b.advanced:
 (gA) \\
	%end
{{b.comment}}</td>
	%if i % 3 == 0:
		<td></td>
	%end
	%i += 1
%end
	</tr>
	
%i = 1
%for s in orga.getStudentsIn(grade, tag):
	<!-- ==================== student #{{s.id}} ({{s.person.name}}, {{s.person.firstname}}) ==================== //-->
	%if i % 2 == 0:
	<tr class="gray">
	%else:
	<tr>
	%end
		<td><a class="edit" href="/admin/students/edit/{{s.id}}">&#9998;</a></td>
		<td>{{i}}</td>
		<td><a href="/loan/person/{{s.person.id}}">{{s.person.name}}, {{s.person.firstname}}</a></td>
	%i += 1
	%j = 1
	%for b in books:
		%if b.workbook or b.classsets:
			%continue
		%end
		%value = loans.getLoanCount(s.person, b)
		%count[b.id] += value
		%value = '' if value == 0 else value
		%id = '%i_%i' % (s.id, b.id)
		<td><input class="selection" type="text" name="{{id}}" value="{{value}}" maxlength="1" /></td>
		%if j % 3 == 0:
		<td></td>
		%end
		%j += 1	
	%end
	</tr>
%end
	<tr>
		<th></th>
		<th></th>
		<th>Summe:</th>
%i = 1
%for b in books:
	%if b.workbook or b.classsets:
		%continue
	%end
		<td>{{count[b.id]}}</td>
	%if i % 3 == 0:
		<td></td>
	%end
	%i += 1
%end
	</tr>
</table>

<input type="submit" value="Änderungen speichern" /><input type="button" value="Abbrechen" onclick="history.back()" />

</form>


%include("footer")
