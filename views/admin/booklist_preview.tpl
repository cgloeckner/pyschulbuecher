%from app.db import book_queries as books
%from app import bool2str
%from app.db import Currency

%include("header")
<h1>Vorschau Bücherzettel</h1>

<form action="/admin/lists/generate/booklist" id="generate_booklist" method="post">

<input type="submit" value="Bücherzettel erstellen" />

%grades = list(all_books.keys())
%grades.sort()
%for grade in grades:
	%key = f'{grade:02d}'
	%books = all_books[key]
<h2>Klassenstufe {{grade}}</h2>
<table>
	<tr>
		<th></th>
		<th>Titel</th>
		<th>Fach</th>
		<th>Verlag</th>
		<th>Bemerkungen</th>
	</tr>
	%for b in books:
		%if b.workbook:
			%continue
		%end
	<tr>
		<td><input type="checkbox" id="{{grade}}_{{b.id}}" name="{{grade}}_{{b.id}}" checked="checked" /></td>
		<td><label for="{{grade}}_{{b.id}}">{{b.title}}</label></td>
		%if b.subject:
		<td>{{b.subject.tag}}</td>
		%else:
		<td>versch.</td>
		%end
		<td>{{b.publisher.name}}</td>
		%info = []
		%if b.workbook:
			%info.append('Arbeitsheft')
		%end
		%if b.novices:
			%info.append('gA')
		%end
		%if b.advanced:
			%info.append('eA')
		%end
		%if b.comment:
			%info.append(b.comment)
		%end
		<td>{{', '.join(info)}}</td>
	</tr>
	%end
	
	
	%for b in books:
		%if not b.workbook:
			%continue
		%end
	<tr>
		<td><input type="checkbox" id="{{grade}}_{{b.id}}" name="{{grade}}_{{b.id}}" checked="checked" /></td>
		<td><label for="{{grade}}_{{b.id}}">{{b.title}}</label></td>
		%if b.subject:
		<td>{{b.subject.tag}}</td>
		%else:
		<td>versch.</td>
		%end
		<td>{{b.publisher.name}}</td>
		<td>Arbeitsheft</td>
	</tr>
	%end
</table> 
%end

</form>

%include("footer")
