%from db.orm import Currency

%include("header")
<h1>Einstellungen</h1>

<form action="/admin/settings" id="settings" method="post">

<table>
	<tr>
		<td>Schuljahr</td>
		<td><input type="text" name="school_year" value="{{s.data['general']['school_year']}}" /></td>
	</tr>
	<tr>
		<td>Preis Schulplaner</td>
		<td><input type="text" name="planner_price" value="{{Currency.toString(int(s.data['general']['planner_price']))}}" />€</td>
	</tr>
	<tr>
		<td>Spätester Abgabetermin Bücherzettel</td>
		<td><input type="text" name="deadlines_booklist_return" value="{{s.data['deadline']['booklist_return']}}" /></td>
	</tr>
	<tr>
		<td>Letzter Änderungstermin Bücherzettel</td>
		<td><input type="text" name="deadlines_booklist_changes" value="{{s.data['deadline']['booklist_changes']}}" /></td>
	</tr>
	<tr>
		<td></td>
		<td><input type="submit" value="Ändern" /></td>
	</tr>
</table>

</form>

%include("footer")
