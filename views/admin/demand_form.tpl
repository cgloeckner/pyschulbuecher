%import db.books as books
%from utils import bool2str
%from db.orm import Currency

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
		<td>{{data[b.id]["diff"]}}</td>
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
