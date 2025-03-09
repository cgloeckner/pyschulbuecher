%from app.db import orga_queries

%include("header")
<h1>Schüler aus Klasse {{c.to_string()}} verschieben</h1>

<form action="/admin/classes/move/{{c.id}}" id="classes" method="post">
%stds = list(c.student)
%orga_queries.sort_students(stds)

<span class="button" style="font-size: 200%;" onClick="toggleAll();" title="Auswahl für alle umkehren">↺</span>
<p>
%for s in stds:
		<input type="checkbox" id="student_{{s.id}}" name="{{s.id}}" />
		<label for="student_{{s.id}}">{{s.person.name}}, {{s.person.firstname}}</label>
		<br />
%end
</p>

Neue Klasse: <select name="class_id">
%for grade in orga_queries.get_class_grades():
	%for tag in orga_queries.get_class_tags(grade):
		%c2 = orga_queries.db.Class.get(grade=grade, tag=tag)
				<option value="{{c2.id}}"\\
		%if s.class_ == c2:
 selected\\
		%end
>{{c2.to_string()}}</option>
	%end
%end
</select>

<br />

<input type="submit" value="Ausgewählte Verschieben" />
</form>

%include("footer")
