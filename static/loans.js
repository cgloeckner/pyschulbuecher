function queryBooks() {
	var grade   = $('#grade_id option:selected').val();
	var subject = $('#subject_id option:selected').val();

	var url = "/loan/ajax/books";
	if (grade != "") {
		url += "/grade/" + grade;
	}
	if (subject != "") {
		url += "/subject/" + subject
	}

	$.get(url, function(data) {
		var books = $('#book_id');
		books.find('option').remove();
		bks = jQuery.parseJSON(data);
		for (id in bks) {
			books.append('<option value="' + id + '">' + bks[id] + '</option>');
		}
	});
}

function queryCount(person_id) {
	var book_id = $('#book_id option:selected').val();

	$.get('/loan/ajax/count/' + person_id + '/' + book_id, function(data) {
		$('#count').val(data);
	});
}
