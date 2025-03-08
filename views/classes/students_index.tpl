%from app.db import orga_queries as orga
%from app.db import loan_queries as loans
%from app.utils import shortify_name

%include("header")
<h1>Bücherübersicht Klasse {{c.to_string()}}</h1>
<a href="/admin/classes/edit/{{c.id}}">Bearbeiten</a><br />

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
		<th class="rotate" name="{{b.id}}">{{b.title}}</th>
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
	<td class="rotate" name="{{b.id}}" onmouseover="enterColumn({{b.id}});" onmouseOut="leaveColumn({{b.id}});">\\
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
%for s in orga.get_students_in(grade, tag):
	<!-- ==================== student #{{s.id}} ({{s.person.name}}, {{s.person.firstname}}) ==================== //-->
	%if i % 2 == 0:
	<tr class="gray select">
	%else:
	<tr class="select">
	%end
		<td><a class="edit" href="/admin/students/edit/{{s.id}}">&#9998;</a></td>
		<td>{{i}}</td>
		<td class="name"><a href="/loan/person/{{s.person.id}}">{{s.person.name}}, {{shortify_name(s.person.firstname)}}</a></td>
	%i += 1
	%j = 1
	%for b in books:
		%if b.workbook or b.classsets:
			%continue
		%end
		%value = loans.get_loan_count(s.person, b)
		%count[b.id] += value
		%value = '' if value == 0 else value
		%id = '%i_%i' % (s.id, b.id)
		<td><input class="selection" type="text" name="{{id}}" value="{{value}}" maxlength="1" onmouseover="enterColumn({{b.id}});" onmouseOut="leaveColumn({{b.id}});" /></td>
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

<hr />

<b>Bücherzettel:</b>
<ul>
	<li><a href="/classes/requests/{{grade}}/{{tag}}/this">Klasse {{grade}}</a></li>
	<li><a href="/classes/requests/{{grade}}/{{tag}}/this-full">Klasse {{grade}} (Neuzugänge)</a></li>
%if grade < 12:
	<li><a href="/classes/requests/{{grade}}/{{tag}}/next">Klasse {{grade+1}}</a></li>
	<li><a href="/classes/requests/{{grade}}/{{tag}}/next-full">Klasse {{grade+1}} (Neuzugänge)</a></li>
%end
</ul>

%include("footer")
