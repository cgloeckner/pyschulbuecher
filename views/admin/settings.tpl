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
	    <td>Schulanschrift</td>
	    <td><textarea rows="10" cols="50" name="address" form="settings">{{s.data['general']['address']}}</textarea></td>
	</tr>
	<tr>
	    <td>Schulleiter</td>
	    <td><input type="text" name="headteacher" value="{{s.data['general']['headteacher']}}" /></td>
	</tr>
	<tr>
		<td>Spätester Abgabetermin Bücherzettel</td>
		<td><input type="text" name="booklist_return" value="{{s.data['deadline']['booklist_return']}}" /></td>
	</tr>
	<tr>
		<td>Letzter Änderungstermin Bücherzettel</td>
		<td><input type="text" name="booklist_changes" value="{{s.data['deadline']['booklist_changes']}}" /></td>
	</tr>
	<tr>
		<td>Rückgabetermin Bücher (Klasse 12)</td>
		<td><input type="text" name="bookreturn_graduate" value="{{s.data['deadline']['bookreturn_graduate']}}" /></td>
	</tr>
	<tr>
		<td></td>
		<td><input type="submit" value="Ändern" /></td>
	</tr>
</table>

<a href="/admin/advance">Schuljahreswechsel</a>

</form>

%include("footer")
