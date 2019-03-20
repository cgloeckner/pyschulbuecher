%import db.orga as orga
%import db.loans as loans

%include("header")
%c = orga.db.Class.get(grade=grade, tag=tag)
<h1>Bücherübersicht Klasse {{c.toString()}}</h1>
<a href="/admin/classes/edit/{{c.id}}">Bearbeiten</a> &dash;
<a href="/classes/requests/{{grade}}/{{tag}}">Bücherzettel für Klasse {{grade+1}}</a>

<form action="/classes/loans/{{grade}}/{{tag}}" id="requests" method="post">

%count = dict()

<table>
	<tr>
		<th></th>
		<th></th>
%i = 1
%for b in books:
	%if b.workbook or b.classsets:
		%continue
	%end
	
	%count[b.id] = 0
	
	%if i % 2 == 0:
		<th class="rotate gray">
	%else:
		<th class="rotate">
	%end
	%i += 1
	{{b.title}}</th>
%end
	</tr>
	<tr>
		<th>Nr.</th>
		<th>Name, Vorname</th>
%i = 1
%for b in books:
	%if b.workbook or b.classsets:
		%continue
	%end
	%if i % 2 == 0:
		<td class="rotate gray">
	%else:
		<td class="rotate">
	%end
	%i += 1
	%if b.subject is not None:
		{{b.subject.tag}}
	%end
	%if b.advanced and not b.novices:
		(eA)
	%elif b.novices and not b.advanced:
		(gA)
	%end
		{{b.comment}}
%end
	</tr>
	
%i = 1
%for s in orga.getStudentsIn(grade, tag):
	<tr>
	%if i % 2 == 0:
		%cl = ' class="gray"'
	%else:
		%cl = ''
	%end
		<td{{!cl}}>{{i}}</td>
		<td{{!cl}}><a href="/admin/students/edit/{{s.id}}">{{s.person.name}}, {{s.person.firstname}}</a></td>
	
	%i += 1
	
	%j = 1
	%for b in books:
		%if b.workbook or b.classsets:
			%continue
		%end
		
		%value = loans.getLoanCount(s.person, b)
		%count[b.id] += value
		
		%id = '%i_%i' % (s.id, b.id)
		%if j % 2 == 0:
		<td class="gray">
		%else:
		<td{{!cl}}>
		%end
		%j += 1
		
		%if value == 0:
		%	value = ""
		%end
		<input class="selection" type="text" name="{{id}}" value="{{value}}" maxlength="1" /></td>
	%end
	</tr>
%end
	<tr>
		<th></th>
		<th>Summe:</th>
%for b in books:
	%if b.workbook or b.classsets:
		%continue
	%end
		<td>{{count[b.id]}}</td>
%end
	</tr>
</table>

<input type="submit" value="Änderungen speichern" /><input type="button" value="Abbrechen" onclick="history.back()" />

</form>


%include("footer")
