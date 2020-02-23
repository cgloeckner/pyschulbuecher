%from db.orm import Currency

%include("header")
<h1>Einstellungen</h1>

<form action="/admin/settings" id="settings" method="post">

<table class="simple">
	<tr>
		<td>Schuljahr</td>
		<td><input type="text" name="school_year" value="{{s.data['general']['school_year']}}" /></td>
	</tr>
	<tr>
		<td>Spätester Abgabetermin Bücherzettel</td>
		<td><input type="text" name="deadline_booklist_return" value="{{s.data['deadline']['booklist_return']}}" /></td>
	</tr>
	<tr>
		<td>Letzter Änderungstermin Bücherzettel</td>
		<td><input type="text" name="deadline_booklist_changes" value="{{s.data['deadline']['booklist_changes']}}" /></td>
	</tr>
	<tr>
		<td>Rückgabetermin Bücher, inkl. Stunde<br />(Klasse 12, Nichtprüfungsfächer)</td>
		<td><input type="text" name="deadline_bookreturn_noexam" value="{{s.data['deadline']['bookreturn_noexam']}}" /></td>
	</tr>
	<tr>
		<td></td>
		<td><input type="submit" value="Ändern" /></td>
	</tr>
</table>

<a href="/admin/advance">Schuljahreswechsel</a>

</form>

%include("footer")
