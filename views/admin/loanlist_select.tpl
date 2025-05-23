%from app.db import orga_queries
%from app.db import loan_queries
%from app.utils import shortify_name

%include("header")
<h1>Leihlisten für Schüler: <span class="button" style="font-size: 100%;" onClick="toggleAll();" title="Auswahl für Klassen umkehren">↺</span></h1>

<form action="/admin/lists/generate/studentloans" id="students" method="post">

<input type="checkbox" name="next_year" id="next_year" /><label for="next_year">für nächstes Schuljahr</label><br />
<input type="checkbox" name="use_requests" id="use_requests" /><label for="use_requests">Bücherzettel einbinden</label><br />
<input type="checkbox" name="split_pdf" id="split_pdf" checked="checked" /><label for="split_pdf">PDFs nach Klassen trennen</label><br />
<input type="checkbox" name="loan_report" id="loan_report" /><label for="loan_report">nur bereits ausgeliehene Bücher</label><br />

<input type="submit" value="Leihlisten erzeugen" /><input type="button" value="Abbrechen" onclick="history.back()" />

%for c in classes:
	<hr />
	<h2>Klasse {{c.to_string()}}: <span class="button" onClick="toggleClass('{{c.id}}');" title="Auswahl für {{c.to_string()}} umkehren">↺</span></h2>
	
	<ol id="{{c.id}}">
	%students = list(c.student)
	%sort_students(students)
	%for s in students:
		<li>
			<input type="checkbox" name="{{s.person.id}}" id="{{s.person.id}}" />
			<label for="{{s.person.id}}">{{s.person.name}}, {{shortify_name(s.person.firstname)}}</label>
		</li>
	%end
	</ol>
%end

</form>

%include("footer")
