%import datetime

\documentclass[10pt,twoside,a4paper]{article}
\usepackage[a4paper, left=2.5cm, right=2cm, top=1.25cm, bottom=2cm]{geometry}
\usepackage{eurosym}
\usepackage[utf8]{inputenc}
\usepackage{makecell}
\usepackage{longtable}
\usepackage[ngerman]{babel}
\usepackage[parfill]{parskip}
\usepackage[table]{xcolor}
\usepackage{fancyhdr}
\usepackage{hyperref}

\pagestyle{fancy}
\renewcommand{\headrulewidth}{0pt} %obere Trennlinie

%year = int(s.data['general']['school_year'])

\fancyhead[L]{} 
\fancyhead[C]{}
\fancyhead[R]{} 
\fancyfoot[L]{
    Bücherzettel erstellt am: {{datetime.date.today().strftime('%d.%m.%Y')}}
}
\fancyfoot[C]{} 
\fancyfoot[R]{}

\newcommand{\strike}[1]{#1} % Some LaTeX wizardry here

%# Arial
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}

\begin{document}
\pagenumbering{gobble}

\begin{center}
    {\LARGE B\"ucherzettel f\"ur das Schuljahr {{year+1}}/{{year+2}}}
\end{center}

{\large {{deadline}} }

\vspace{0.25cm}

\begin{Form}[action={}]

\newcommand{\textinput}[1] {
    \raisebox{-0.2cm}{\TextField[width=#1, height=0.75cm, bordercolor=black!25!white]{\null}}
}

\newcommand{\checkinput} {
    \raisebox{-0.125cm}{\CheckBox[width=0.35cm, height=0.35cm, bordercolor=black!25!white, checkboxsymbol=\ding{53}]{\null}}
}

\newcommand{\infoInput}[2][4in]{%
  \stepcounter{infoLineNum}%
  \makebox[0pt][l]{%
    \kern 4 pt
    \raisebox{.75ex}
      {\textField[\W0\BC{}\BG{}\TU{#2}]{name\theinfoLineNum}{#1}{12bp}}%
  }
    \dotfill
}

\begin{tabular}{ r p{4cm} r p{4cm} r c}
	Name: & \textinput{4cm} & Vorname: & \textinput{4cm} & Klasse: & {{grade}} \quad
	%if grade > 5 and not new_students:
		\textinput{1.5cm}
	%end
\end{tabular}

\vspace{0.25cm}
