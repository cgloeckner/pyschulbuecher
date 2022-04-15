%from utils import tex_escape, shortName

%if i % 2 == 0:
    \showrowcolors
%else:
    \hiderowcolors
%end
{{i+1}} &
{{!tex_escape(l.person.student.class_.toString())}} &
{{!tex_escape(l.person.name)}} &
{{!tex_escape(shortName(l.person.firstname))}} &
{{l.count}}x
\\ \hline
