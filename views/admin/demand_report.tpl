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
		<th>Titel</th>
		<th>Klassen</th>
		<th>ISBN</th>
		<th>Preis</th>
		<th>Verlag</th>
		
		<th class="rotate">Bestand</th>
		<th class="rotate">Benötigt</th>
		<th class="rotate">davon Freiexemplare</th>
		<th class="rotate">Klassensätze</th>
		<th class="rotate">davon Beschaffung Eltern</th>
		
		<th class="rotate">Beschaffung Schule</th>
		<th class="rotate">Kosten</th>
	</tr>
%for b in bks:
	%if b.workbook or b.price is None:
		%continue
	%end
	%if data[b.id]["price"] == 0:
		%continue
	%end
	<tr>
		<td>{{b.title}}</td>
		<td>\\
	%if b.subject is not None:
{{b.subject.tag}} \\
	%else:
versch. \\
	%end
	%if b.inGrade < b.outGrade:
{{b.inGrade}}-{{b.outGrade}}\\
	%else:
{{b.inGrade}}\\
	%end
</td>
		<td>{{b.isbn}}</td>
		<td>{{Currency.toString(b.price)}}</td>
		<td>{{b.publisher.name}}</td>
		
		<td>{{b.stock}}</td>
		<td>{{data[b.id]["required"]}}</td>
	%if b.classsets:
		<td>0</td>
		<td>{{data[b.id]["free"]}}</td>
	%else:
		<td>{{data[b.id]["free"]}}</td>
		<td>0</td>
	%end
		<td>{{data[b.id]["parents"]}}</td>
		<td>{{!data[b.id]["diff"]}}</td>
		<td>{{Currency.toString(data[b.id]["price"])}}</td>
	</tr>
%end
</table>


<hr />

<h3>Detailierter Bericht</h3>

<table class="books">
	<tr>
		<th>Titel</th>
		<th>Klassen</th>
		<th>ISBN</th>
		<th>Preis</th>
		<th>Verlag</th>
		
		<th class="rotate">Bestand</th>
		<th class="rotate">Benötigt</th>
		<th class="rotate">Freiexemplare</th>
		<th class="rotate">Klassensätze</th>
		<th class="rotate">Beschaffung Eltern</th>
		
		<th class="rotate">Beschaffung Schule</th>
		<th class="rotate">Kosten</th>
	</tr>
%for b in bks:
	%if b.workbook or b.price is None:
		%continue
	%end
	<tr>
		<td>{{b.title}}</td>
		<td>\\
	%if b.subject is not None:
{{b.subject.tag}} \\
	%else:
versch. \\
	%end
	%if b.inGrade < b.outGrade:
{{b.inGrade}}-{{b.outGrade}}\\
	%else:
{{b.inGrade}}\\
	%end
</td>
		<td>{{b.isbn}}</td>
		<td>{{Currency.toString(b.price)}}</td>
		<td>{{b.publisher.name}}</td>
		
		<td title="Bestand">{{b.stock}}</td>
		<td title="Benötigt">{{data[b.id]["required"]}}</td>
	%if b.classsets:
		<td title="Freiexemplare">0</td>
		<td title="Klassensätze">{{data[b.id]["free"]}}</td>
	%else:
		<td title="Freiexemplare">{{data[b.id]["free"]}}</td>
		<td title="Klassensätze">0</td>
	%end
		
		<td title="Beschaffung Eltern">{{data[b.id]["parents"]}}</td>
		
		<td title="Beschaffung Schule">{{!data[b.id]["diff"]}}</td>
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
