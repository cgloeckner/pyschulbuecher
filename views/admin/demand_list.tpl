%import db.books as books
%from utils import bool2str
%from db.orm import Currency

%include("header")
<h1>Bedarfsbericht</h1>

<a href="/admin/order">Bestellübersicht</a>

<table>
	<tr>
		<th>Titel</th>
		<th>ISBN</th>
		<th>Preis</th>
		<th>Verlag</th>
		<th>Bestand</th>
		<th>Bedarf</th>
		<th>Übrig</th>
		<th>Beschaffung</th>
		<th>Kosten</th>
	</tr>
%for b in bks:
	%if b.workbook or b.classsets or b.price is None:
		%continue
	%end
	<tr>
		<td>{{b.title}}</td>
		<td>{{b.isbn}}</td>
		<td>{{Currency.toString(b.price)}}€</td>
		<td>{{b.publisher.name}}</td>
		<td>{{b.stock}}</td>
		<td>{{data[b.id]["need"]}}</td>
	
	%perc = 1.0
	%if data[b.id]["need"] > 0:
		%perc = data[b.id]["diff"] / data[b.id]["need"]
	%end
	
	%if perc < 0.0:
		<td class="critical">
	%elif perc <= 0.1:
		<td class="low">
	%else:
		<td>
	%end
		{{data[b.id]["diff"]}}</td>
		<td>
	%diff = data[b.id]["diff"]
	%if diff < 0:
		{{-diff}}
	%end
		</td>
		<td>
	%p = data[b.id]["price"]
	%if p > 0:
		{{Currency.toString(data[b.id]["price"])}}&euro;
	%end
		</td>
	</tr>
%end

%include("footer")
