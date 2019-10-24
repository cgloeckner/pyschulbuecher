<form action="/loan/person/{{person.id}}/add" id="loan" method="post">
	<table>
		<tr>
			<th>Buch</th>
			<th>Fach</th>
			<th>Klassenstufe</th>
			<th>Anzahl</th>
		</tr>
	%for b in bks:
		<tr>
			<td>{{b.title}}</td>
		%if b.subject is None:
			<td>verschiedene</td>
		%else:
			<td>{{b.subject.tag}}</td>
		%end
		%if b.inGrade < b.outGrade:
			<td>{{b.inGrade}}-{{b.outGrade}}</td>
		%else:
			<td>{{b.inGrade}}</td>
		%end
			<td><input type="text" name="{{b.id}}" id="{{b.id}}" size="1" maxlength="3" /></td>
		</tr>
	%end
		<tr>
			<td colspan="4"><input type="submit" value="Speichern" /></td>
		</tr>
	</table>
</form>
