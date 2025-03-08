
def shortify_name(firstname: str) -> str:
    """Abbreviate first name by reducing secondary first names to a single
    letter."""
    parts = firstname.split(' ')
    more = parts[0].split('-')
    out = more[0]
    for i in range(1, len(more)):
        out += '-%s.' % more[i][0]
    for i in range(1, len(parts)):
        out += ' %s.' % parts[i][0]
    return out
