%from db import orga

%include("header")
<h1>Schüler aus Klasse {{c.toString()}} verschieben</h1>

<form action="/admin/classes/move/{{c.id}}" id="classes" method="post">
%stds = list(c.student)
%orga.sortStudents(stds)

<span class="button" style="font-size: 200%;" onClick="toggleAll();" title="Auswahl für alle umkehren">↺</span>
<p>
%for s in stds:
		<input type="checkbox" id="student_{{s.id}}" name="{{s.id}}" />
		<label for="student_{{s.id}}">{{s.person.name}}, {{s.person.firstname}}</label>
		<br />
%end
</p>

Neue Klasse: <select name="class_id">
%for grade in orga.getClassGrades():
	%for tag in orga.getClassTags(grade):
		%c2 = orga.db.Class.get(grade=grade, tag=tag)
				<option value="{{c2.id}}"\\
		%if s.class_ == c2:
 selected\\
		%end
>{{c2.toString()}}</option>
	%end
%end
</select>

<br />

<input type="submit" value="Ausgewählte Verschieben" />
</form>

%include("footer")
