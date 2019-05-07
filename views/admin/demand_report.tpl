%import db.books as books
%import db.orga as orga
%from utils import bool2str
%from db.orm import Currency

%include("header")

%year = int(s.data['general']['school_year'])
<h1>Bedarfsbericht für Schuljahr {{year}}/{{year+1}}</h1>

<p><b>Gesamtsumme:</b> {{Currency.toString(total)}}</p>

<h3>Zusammenfassung:</h3>

<table class="books">
	<tr>
		<th>Klasse</th>
		<th>Fach</th>
	
		<th>Titel</th>
		<th>Verlag</th>
		<th>ISBN</th>
		<th>Preis</th>
		
		<th class="rotate">Gesamtbedarf</th>
		<th class="rotate">Bestand</th>
		<th class="rotate">übrig</th>
		<th class="rotate">Beschaffung Eltern</th>
		
		<th class="rotate">Beschaffung Schule</th>
		<th class="rotate">Kosten</th>
	</tr>
%for b in bks:
	%if b.workbook or b.price is None:
		%continue
	%end
	%if data[b.id]["price"] == 0 and not data[b.id]["critical"]:
		%continue
	%end
	<tr>
	%if b.inGrade < b.outGrade:
		<td>{{b.inGrade}}-{{b.outGrade}}</td>
	%else:
		<td>{{b.inGrade}}</td>
	%end
	%if b.subject is not None:
		<td>{{b.subject.tag}}</td>
	%else:
		<td>versch. </td>
	%end
	
		<td>{{b.title}}</td>
		<td>{{b.publisher.name}}</td>
		<td>{{b.isbn}}</td>
		<td>{{Currency.toString(b.price)}}</td>
	
	%if data[b.id]["critical"]:
		%css = ' class="critical"'
	%else:
		%css = ''
	%end
	
	%if b.classsets:
		<td title="Bedarf">{{data[b.id]["required"]}}</td>
		<td title="Bestand">{{data[b.id]["stock"]}}</td>
		<td title="übrig"{{!css}}>{{data[b.id]["leftover"]}}</td>
		<td>&mdash;</td>
	%else:
		<td title="Bedarf">{{data[b.id]["required"]}} ({{data[b.id]["free"]}})</td>
		<td title="Bestand">{{data[b.id]["stock"]}}</td>
		<td title="übrig"{{!css}}>{{data[b.id]["leftover"]}}</td>
		<td title="Eltern">{{data[b.id]["parents"]}}</td>
	%end
		<td title="Beschaffung Schule">{{!data[b.id]["school"]}}</td>
		<td>{{Currency.toString(data[b.id]["price"])}}</td>
	</tr>
%end
</table>


<hr />

<h3>Detailierter Bericht</h3>

<table class="books">
	<tr>
		<th>Klasse</th>
		<th>Fach</th>
	
		<th>Titel</th>
		<th>Verlag</th>
		<th>ISBN</th>
		<th>Preis</th>
		
		<th class="rotate">Gesamtbedarf</th>
		<th class="rotate">Bestand</th>
		<th class="rotate">übrig</th>
		<th class="rotate">Beschaffung Eltern</th>
		
		<th class="rotate">Beschaffung Schule</th>
		<th class="rotate">Kosten</th>
	</tr>
%for b in bks:
	%if b.workbook or b.price is None:
		%continue
	%end
	<tr>
	%if b.inGrade < b.outGrade:
		<td>{{b.inGrade}}-{{b.outGrade}}</td>
	%else:
		<td>{{b.inGrade}}</td>
	%end
	%if b.subject is not None:
		<td>{{b.subject.tag}}</td>
	%else:
		<td>versch. </td>
	%end
	
		<td>{{b.title}}</td>
		<td>{{b.publisher.name}}</td>
		<td>{{b.isbn}}</td>
		<td>{{Currency.toString(b.price)}}</td>
	
	%if data[b.id]["critical"]:
		%css = ' class="critical"'
	%else:
		%css = ''
	%end
	
	%if b.classsets:
		<td title="Bedarf">{{data[b.id]["required"]}}</td>
		<td title="Bestand">{{data[b.id]["stock"]}}</td>
		<td title="übrig"{{!css}}>{{data[b.id]["leftover"]}}</td>
		<td>&mdash;</td>
	%else:
		<td title="Bedarf">{{data[b.id]["required"]}} ({{data[b.id]["free"]}})</td>
		<td title="Bestand">{{data[b.id]["stock"]}}</td>
		<td title="übrig"{{!css}}>{{data[b.id]["leftover"]}}</td>
		<td title="Eltern">{{data[b.id]["parents"]}}</td>
	%end
		
		<td title="Beschaffung Schule">{{!data[b.id]["school"]}}</td>
	%if data[b.id]["price"] > 0:
		%css = ' class="demand"'
	%else:
		%css = ''
	%end
		<td{{!css}}>{{Currency.toString(data[b.id]["price"])}}</td>
	</tr>
%end
</table>

%include("footer")
