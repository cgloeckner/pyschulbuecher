%from app import tex_escape, shortify_name

%if i % 2 == 0:
    \showrowcolors
%else:
    \hiderowcolors
%end
{{i+1}} &
{{!tex_escape(l.person.student.class_.to_string())}} &
{{!tex_escape(l.person.name)}} &
{{!tex_escape(shortify_name(l.person.firstname))}} &
{{l.count}}x
\\ \hline
