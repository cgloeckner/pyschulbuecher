
%from app.utils import shortify_name

%include("header")
<h1>Leihliste für {{book.title}}</h1>

<table>
	<tr>
		<th></th>
		<th>Name, Vorname</th>
		<th>Anzahl</th>
	</tr>
%for l in loans:
	<tr>
	%if l.person.student is not None:
		<td>{{l.person.student.class_.to_string()}}</td>
	%else:
		<td>{{l.person.teacher.tag.upper()}}</td>
	%end
		<td><a href="/loan/person/{{l.person.id}}">{{l.person.name}}, {{shortify_name(l.person.firstname)}}</a></td>
		<td>{{l.count}}</td>
	</tr>
%end
</table>

%include("footer")
