%from db import orga, books

%include("header")
<h1>Leihbericht</h1>

<table>
	<tr>
		<th>Fach</th>
		<th>Titel</th>
		<th>Klasse</th>
		<th>Bem.</th>
		<th>Bestand</th>
		<th>Ausleihe</th>
		<th>Übrig</th>
	</tr>

%for b in report:
	<tr>
		<td>
	%if b.subject is None:
			versch.
	%else:
			{{b.subject.tag}}
	%end
		</td>
		<td><a href="/loan/book/{{b.id}}" target="_blank">{{b.title}}</a></td>
		<td>
	%if b.inGrade < b.outGrade:
			{{b.inGrade}}-{{b.outGrade}}
	%else:
			{{b.inGrade}}
	%end
		</td>
	%comments = []
	%if b.comment != '':
		%comments.append(b.comment)
	%end
	%if b.novices:
		%comments.append('gA')
	%end
	%if b.advanced:
		%comments.append('eA')
	%end
	%if b.classsets:
		%comments.append('Klassensätze')
	%end
		<td>{{', '.join(comments)}}</td>
		<td>{{b.stock}}</td>
		<td>{{report[b]}}</td>
	%remain = b.stock - report[b]
	%if remain < 0:
		<td class="highlight">{{remain}}</td>
	%else:
		<td>{{remain}}</td>
	%end
		</td>
	</tr>
%end

</table>

%include("footer")
