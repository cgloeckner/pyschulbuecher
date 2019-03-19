function showBooks(css_class) {
	// toggle 'display' between 'none' and 'table-row' (default)
	if ($('.' + css_class).css('display') == 'table-row') {
		$('.' + css_class).css('display', 'none');
	} else {
		$('.' + css_class).css('display', 'table-row');
	}
}

function checkAll() {
	$("input[type='checkbox']").each(function() {
    	$(this).prop("checked", !this.checked);
	});
}

function toggle(name) {
	var obj = $("input[name='" + name + "']")[0];
	obj.checked = !obj.checked;
}
