%import db.orga as orga
%import db.loans as loans

%include("header")
%c = orga.db.Class.get(grade=grade, tag=tag)
<h1>Bücherzettel Klasse {{c.toString()}} (für Klasse {{grade+1}})</h1>

<form action="/classes/requests/{{grade}}/{{tag}}" id="requests" method="post">

<table>
	<tr>
		<th></th>
		<th><input type="button" value="Auswahl umkehren" onClick="checkAll();" /></th>
%i = 1
%for b in books:
	%if b.workbook:
		%continue
	%end
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
		%id = '%i_%i' % (s.id, b.id)
		%if j % 2 == 0:
		<td class="gray">
		%else:
		<td{{!cl}}>
		%end
		%j += 1
		%if loans.isRequested(s, b):
			%checked = 'checked="checked"'
		%else:
			%checked = ''
		%end
		<input class="selection" type="checkbox" name="{{id}}" {{!checked}} /></td>
	%end
	</tr>
%end
</table>

<input type="submit" value="Änderungen speichern" /><input type="button" value="Abbrechen" onclick="history.back()" />

</form>

%include("footer")
