%import db.orga as orga
%import db.loans as loans

%include("header")
%c = orga.db.Class.get(grade=grade, tag=tag)
<h1>Bücherzettel Klasse {{c.toString()}} (für Klasse {{grade+1}})</h1>

<form action="/classes/requests/{{grade}}/{{tag}}" id="requests" method="post">

<table class="simple">
	<!-- ==================== book titles ==================== //-->
	<tr>
		<th></th>
		<th></th>
		<th><span class="button" style="font-size: 500%;" onClick="toggleAll();" title="Auswahl für alle umkehren">↺</span></th>
%i = 1
%for b in books:
	%if b.workbook:
		%continue
	%end
		<th class="rotate">{{b.title}}</th>
	%if i % 3 == 0:
		<th>&nbsp;</th>
	%end
	%i += 1
%end
		<th></th>
	</tr>
	<!-- ==================== subjects titles ==================== //-->
	<tr>
		<td></td>
		<td></td>
		<td></td>
%i = 1
%for b in books:
	%if b.workbook or b.classsets:
		%continue
	%end
		<td class="rotate">\\
	%if b.subject is not None:
{{b.subject.tag}}\\
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
		<td></td>
	</tr>
	
	<!-- ==================== book negation switches ==================== //-->
	<tr>
		<th></th>
		<th>Nr.</th>
		<th>Name, Vorname</th>
%i = 1
%for b in books:
	%if b.workbook or b.classsets:
		%continue
	%end
		<td><span class="button" onClick="toggleCol({{b.id}});" title="Auswahl für dieses Buch umkehren">↺</span></td>
	%if i % 3 == 0:
		<td></td>
	%end
	%i += 1
%end
		<td></td>
	</tr>
	
%i = 1
%for s in orga.getStudentsIn(grade, tag):
	<!-- ==================== student #{{s.id}} ({{s.person.name}}, {{s.person.firstname}}) ==================== //-->
	%if i % 2 == 0:
	<tr class="gray" id="{{s.id}}">
	%else:
	<tr id="{{s.id}}">
	%end
		<td><a class="edit" href="/admin/students/edit/{{s.id}}">&#9998;</a></td>
		<td>{{i}}</td>
		<td><a href="/loan/{{s.person.id}}">{{s.person.name}}, {{s.person.firstname}}</a></td>
	%i += 1
	%j = 1
	%for b in books:
		%if b.workbook or b.classsets:
			%continue
		%end
		%id = '%i_%i' % (s.id, b.id)
		%if loans.isRequested(s, b):
			%checked = 'checked="checked"'
		%else:
			%checked = ''
		%end
		<td name="{{b.id}}"><input class="selection" type="checkbox" name="{{id}}" {{!checked}}/></td>
		%if j % 3 == 0:
		<td></td>
		%end
		%j += 1
	%end
		<td><span class="button" onClick="toggleRow({{s.id}});" title="Auswahl für diesen Schüler umkehren">↺</span></td>
	</tr>
%end
</table>

<input type="submit" value="Änderungen speichern" /><input type="button" value="Abbrechen" onclick="history.back()" />

</form>

%include("footer")
