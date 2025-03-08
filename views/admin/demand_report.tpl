%from app.db import book_queries as books
%from app.db import orga_queries as orga
%from utils import bool2str
%from app.db import Currency

%include("header")

%year = int(s.data['general']['school_year'])
<h1>Bedarfsbericht für Schuljahr {{year+1}}/{{year+2}}</h1>

<p><b>Gesamtsumme:</b> {{Currency.to_string(total)}}</p>

<center><b>Anmerkung:</b> In der untenstehenden Auflistung sind <b>keine</b> Klassensätze berücksichtigt.</center>

<br />

<a href="javascript:toggleDemand();">Ansicht umschalten</a>

<br />
<br />

<table class="books">
	<tr>
		<th>Fach</th>
		<th>Klasse</th>
	
		<th>Titel</th>
		<th>Verlag</th>
		<th>ISBN</th>
		<th>Preis</th>
		
		<th></th>
		<th class="rotate">Gesamtbedarf</th>
		<th class="rotate">Vorhanden</th>
		<th class="rotate">Puffer</th>
		
		<th></th>		
		<th class="rotate">Beschaffung</th>		
		<th class="rotate">Beschaffung Eltern</th>
		<th class="rotate">Beschaffung Schule</th>
		
		<th></th>
		<th class="rotate">Kosten</th>
	</tr>
%for b in bks:
	%if b.id not in data:
		%continue
	%end
	%if data[b.id]["costs"] > 0:
	<tr>
	%else:
	<tr class="trivial">
	%end
	%if b.subject is not None:
		<td>{{b.subject.tag}}</td>
	%else:
		<td>versch. </td>
	%end
	%if b.inGrade < b.outGrade:
		<td>{{b.inGrade}}-{{b.outGrade}}</td>
	%else:
		<td>{{b.inGrade}}</td>
	%end
	
		<td>{{b.title}}</td>
		<td>{{b.publisher.name}}</td>
		<td>{{b.isbn}}</td>
		<td>{{Currency.to_string(b.price)}}</td>
	
		<td></td>
		<td title="{{data[b.id]["in_use"]}} weiterhin in Ausleihe, {{data[b.id]["requested"]}} via Bücherzettel">{{data[b.id]["raw_demand"]}}</td>
		<td title="{{data[b.id]["available"]}} von {{b.stock}} vorhandenen Büchern">{{data[b.id]["available"]}}</td>
	%remaining_books = data[b.id]["available"] - data[b.id]["raw_demand"]
	%if remaining_books < 0:
		%remaining_books = '-'
	%end
		<td title="übrig wenn {{data[b.id]["raw_demand"]}} von {{data[b.id]["available"]}} ausgegeben">{{remaining_books}}</td>
		
		<td></td>
		<td title="nötig um {{data[b.id]["raw_demand"]}} ausgeben zu können">{{data[b.id]["required"]}}</td>
		<td title="Differenz aus \"Beschaffung\" und \"von Schule\"">{{data[b.id]["by_parents"]}}</td>
		<td title="nötige Freiexemplare laut Bücherzettel">{{data[b.id]["by_school"]}}</td>
		
		<td></td>
	%if data[b.id]["costs"] > 0:
		%css = ' class="demand"'
	%else:
		%css = ''
	%end
		<td{{!css}}>{{Currency.to_string(data[b.id]["costs"])}}</td>
	</tr>
%end
</table>

%include("footer")
