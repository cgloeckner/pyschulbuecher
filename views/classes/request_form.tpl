%from app.db import orga_queries
%from app.db import loan_queries

%include("header")
<h1>Bücherzettel Klasse {{c.to_string()}} (für Klasse {{grade+1}})</h1>

<p>Parallelklassen: 
%for other_tag in orga_queries.get_class_tags(grade):
	%if other_tag != tag:
		<a href="/classes/requests/{{grade}}/{{other_tag}}/{{version}}">{{grade}}{{other_tag}}</a>
	%end
%end
</p>

<form action="/classes/requests/{{grade}}/{{tag}}/{{version}}" id="requests" method="post">

%total = dict()

<table class="simple">
	<!-- ==================== book titles ==================== //-->
	<tr class="titles">
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
		<td class="rotate" name="{{b.id}}">\\
	%if b.subject is not None:
{{b.subject.tag}}\\
	%end
	%if b.advanced and not b.novices:
 (eA) \\
	%elif b.novices and not b.advanced:
 (gA) \\
	%end
	%if len(b.comment) < 10:
{{b.comment}} \\
	%end
</td>
	%if i % 3 == 0:
		<td></td>
	%end
	%i += 1
%end
		<td></td>
		<td></td>
	</tr>
	
	<!-- ==================== book toggle switches ==================== //-->
	<tr>
		<th></th>
		<th>Nr.</th>
		<th>Name, Vorname</th>
%i = 1
%for b in books:
	%if b.workbook or b.classsets:
		%continue
	%end
	%total[b.id] = 0
		<td><span class="button" onClick="toggleCol({{b.id}});" title="Auswahl für dieses Buch umkehren">↺</span></td>
	%if i % 3 == 0:
		<td></td>
	%end
	%i += 1
%end
		<td></td>
		<td></td>
	</tr>
	
%i = 1
%for s in orga_queries.get_students_in(grade, tag):
	<!-- ==================== student #{{s.id}} ({{s.person.name}}, {{s.person.firstname}}) ==================== //-->
	%if i % 2 == 0:
	<tr class="gray select" id="{{s.id}}">
	%else:
	<tr class="select" id="{{s.id}}">
	%end
		<td><a class="edit" href="/admin/students/edit/{{s.id}}">&#9998;</a></td>
		<td>{{i}}</td>
		<td class="name"><a href="/loan/person/{{s.person.id}}">{{s.person.name}}, {{s.person.firstname}}</a></td>
	%i += 1
	%j = 1
	%for b in books:
		%if b.workbook or b.classsets:
			%continue
		%end
		%id = '%i_%i' % (s.id, b.id)
		%if loan_queries.is_requested(s, b):
			%total[b.id] += 1
			%checked = 'checked="checked"'
		%else:
			%checked = ''
		%end
		<td title="\\
		%if b.subject is not None:
{{b.subject.name}}\\
		%else:
versch.\\
		%end
		%if b.inGrade < b.outGrade:
 {{b.inGrade}}-{{b.outGrade}}\\
		%else:
 {{b.inGrade}}\\
		%end
 &#8222{{b.title}}&#8220" name="{{b.id}}" onmouseover="enterColumn({{b.id}});" onmouseOut="leaveColumn({{b.id}});"><input class="selection" type="checkbox" name="{{id}}" {{!checked}}/></td>
		%if j % 3 == 0:
		<td></td>
		%end
		%j += 1
	%end
		<td><span class="button" onClick="toggleRow({{s.id}});" title="Auswahl für diesen Schüler umkehren">↺</span></td>
	</tr>

	%if i % 30 == 1:
	<!-- ==================== repeated subjects ==================== //-->
	<tr>
		<td></td>
		<td></td>
		<td></td>
%k = 1
%for b in books:
	%if b.workbook or b.classsets:
		%continue
	%end
		<td class="rotate" name="{{b.id}}">\\
	%if b.subject is not None:
{{b.subject.tag}}\\
	%end
	%if b.advanced and not b.novices:
 (eA) \\
	%elif b.novices and not b.advanced:
 (gA) \\
	%end
	%if len(b.comment) < 10:
{{b.comment}} \\
	%end
</td>
	%if k % 3 == 0:
		<td></td>
	%end
	%k += 1
%end
		<td></td>
		<td></td>
	</tr>

	%end
%end
	<tr>
		<td></td>
		<td></td>
		<td>Summe:</td>
%j = 1
%for b in books:
	%if b.workbook or b.classsets:
		%continue
	%end
		<td class="booksum">{{total[b.id]}}</td>
	%if j % 3 == 0:
		<td></td>
	%end
	%j += 1
%end
		<td></td>
	</tr>
</table>

<input type="submit" value="Änderungen speichern" /><input type="button" value="Abbrechen" onclick="history.back()" />

</form>

%include("footer")
