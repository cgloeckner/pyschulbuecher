function toggleAll() {
	$("input[type='checkbox']").each(function() {
    	$(this).prop("checked", !this.checked);
	});
}

function toggle(name) {
	var obj = $("input[name='" + name + "']")[0];
	obj.checked = !obj.checked;
}

function toggleRow(id) {
	var objs = $('td input:checkbox', '#' + id);//.prop('checked', this.checked)
	for (i in objs) {
		objs[i].checked = !objs[i].checked;
	}
}

function toggleCol(id) {
	var objs = $('td[name=' + id + '] input:checkbox');//.prop('checked', this.checked)
	for (i in objs) {
		objs[i].checked = !objs[i].checked;
	}
}

function enterColumn(id) {
	$('td[name="' + id + '"]').add_class('highlight');
}

function leaveColumn(id) {
	$('td[name="' + id + '"]').removeClass('highlight');
}

function clearColumn(id) {
     $('input[type="text"][name$="_' + id + '"]').val('')
}

