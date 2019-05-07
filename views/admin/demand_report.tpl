%import db.books as books
%import db.orga as orga
%from utils import bool2str
%from db.orm import Currency

%include("header")

%year = int(s.data['general']['school_year'])
<h1>Bedarfsbericht für Schuljahr {{year}}/{{year+1}}</h1>

<p><b>Gesamtsumme:</b> {{Currency.toString(total)}}</p>

<a href="javascript:toggleDemand();">Ansicht umschalten</a>

<br />
<br />

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
		<th class="rotate">Übrig</th>
		
		<th></th>
		<th class="rotate">Beschaffung Summe</th>		
		<th class="rotate">Beschaffung Eltern</th>
		<th class="rotate">Beschaffung Schule</th>
		<th></th>
		
		<th class="rotate">Kosten</th>
	</tr>
%for b in bks:
	%if b.workbook or b.price is None:
		%continue
	%end
	%if data[b.id]["price"] > 0:
	<tr>
	%else:
	<tr class="trivial">
	%end
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
	
	%if b.classsets:
		<td title="Bedarf">{{data[b.id]["required"]}}</td>
		<td title="Bestand">{{data[b.id]["stock"]}}</td>
		<td title="übrige Bücher">{{data[b.id]["left"]}}</td>
		<td></td>
		<td title="Beschaffung">{{data[b.id]["acquire"]}}</td>
		<td>&mdash;</td>
	%else:
		<td title="Bedarf ({{data[b.id]["free"]}} Freiexemplare)">{{data[b.id]["required"]}}</td>
		<td title="Bestand">{{data[b.id]["stock"]}}</td>
		<td title="übrige Bücher">{{data[b.id]["left"]}}</td>
		<td></td>
		<td title="Beschaffung">{{data[b.id]["acquire"]}}</td>
		<td title="Eltern">{{data[b.id]["parents"]}}</td>
	%end
		
		<td title="Beschaffung Schule">{{!data[b.id]["school"]}}</td>
		
		<td></td>
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
