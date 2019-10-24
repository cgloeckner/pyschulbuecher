function queryBooks(person_id, by) {
	var value     = $('#' + by + '_id option:selected').val();
	var classsets = $('#classsets')[0].checked;
	
	$.get("/loan/ajax/books",
		 {
		 	by: by,
		 	value: value,
		 	person_id: person_id,
		 	classsets: classsets
		 }, function(data) {
		$('#books').html(data);
	});
}
