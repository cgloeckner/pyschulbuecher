%import db.books as books
%from utils import bool2str
%from db.orm import Currency

%include("header")
<h1>Vorschau Bücherzettel</h1>

<form action="/admin/lists/generate/booklist" id="generate_booklist" method="post">

<input type="submit" value="Bücherzettel erstellen" />

%for grade, books in sorted(all_books.items(), key=lambda item: item[1]):
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
