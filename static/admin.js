function showBooks(css_class) {
	// toggle 'display' between 'none' and 'table-row' (default)
	if ($('.' + css_class).css('display') == 'table-row') {
		$('.' + css_class).css('display', 'none');
	} else {
		$('.' + css_class).css('display', 'table-row');
	}
}

