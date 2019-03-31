function showBooks(css_class) {
	// toggle 'display' between 'none' and 'table-row' (default)
	if ($('.' + css_class).css('display') == 'table-row') {
		$('.' + css_class).css('display', 'none');
	} else {
		$('.' + css_class).css('display', 'table-row');
	}
}

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

