%from db.orm import Currency

%include("header")
<h1>Einstellungen</h1>

<form action="/admin/settings" id="settings" method="post">

<table>
	<tr>
		<td>Schuljahr</td>
		<td><input type="text" name="school_year" value="{{s.school_year}}" /></td>
	</tr>
	<tr>
		<td>Preis Schulplaner</td>
		<td><input type="text" name="planner_price" value="{{Currency.toString(s.planner_price)}}" />€</td>
	</tr>
	<tr>
		<td>Spätester Abgabetermin Bücherzettel</td>
		<td><input type="text" name="deadline_booklist" value="{{s.deadline_booklist}}" /></td>
	</tr>
	<tr>
		<td>Letzter Änderungstermin Bücherzettel</td>
		<td><input type="text" name="deadline_changes" value="{{s.deadline_changes}}" /></td>
	</tr>
	<tr>
		<td></td>
		<td><input type="submit" value="Ändern" /></td>
	</tr>
</table>

</form>

%include("footer")
