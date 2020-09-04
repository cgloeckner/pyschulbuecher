%import db.orga as orga
%import db.loans as loans
%from utils import shortName

%include("header")
<h1>Leihlisten für Schüler: <span class="button" style="font-size: 100%;" onClick="toggleAll();" title="Auswahl für Klassen umkehren">↺</span></h1>

<form action="/admin/lists/generate/studentloans" id="students" method="post">

<input type="checkbox" name="next_year" id="next_year" /><label for="next_year">für nächstes Schuljahr</label><br />
<input type="checkbox" name="use_requests" id="use_requests" /><label for="use_requests">Bücherzettel einbinden</label><br />
<input type="checkbox" name="split_pdf" id="use_requests" checked="checked" /><label for="use_requests">PDFs nach Klassen trennen</label><br />

<input type="submit" value="Leihlisten erzeugen" /><input type="button" value="Abbrechen" onclick="history.back()" />

%for c in classes:
	<hr />
	<h2>Klasse {{c.toString()}}: <span class="button" onClick="toggleClass('{{c.id}}');" title="Auswahl für {{c.toString()}} umkehren">↺</span></h2>
	
	<ol id="{{c.id}}">
	%students = list(c.student)
	%sortStudents(students)
	%for s in students:
		<li>
			<input type="checkbox" name="{{s.person.id}}" id="{{s.person.id}}" />
			<label for="{{s.person.id}}">{{s.person.name}}, {{shortName(s.person.firstname)}}</label>
		</li>
	%end
	</ol>
%end

</form>

%include("footer")
