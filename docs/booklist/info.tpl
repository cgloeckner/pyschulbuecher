%import datetime

\documentclass[10pt,twoside,a4paper]{article}
\usepackage[a4paper, left=3cm, right=2cm, top=1.25cm, bottom=2cm]{geometry}
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

\cfoot{}
\rfoot{Letzte Änderung: {{datetime.date.today().strftime('%d.%m.%Y')}}}

\newcommand{\strike}[1]{#1} % Some LaTeX wizardry here

%# Arial
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}

\begin{document}

{\footnotesize
	\begin{tabular}{ c }
        {{s.data['general']['address']}}
	\end{tabular}
}

\vspace{0.5cm}

%year = int(s.data['general']['school_year'])
\begin{center}
	{\LARGE B\"ucherzettel f\"ur das Schuljahr {{year+1}}/{{year+2}}}
\end{center}

\vspace{0.5cm}

Sehr geehrte Eltern,

bitte f\"ullen Sie nach Ihren M\"oglichkeiten und W\"unschen den B\"ucherzettel f\"ur Ihr Kind aus. Beachten Sie dabei:

\begin{enumerate}
	\item Die Arbeitshefte werden nicht aus Landesmitteln bezahlt und m\"ussen von Ihnen finanziell selbst getragen \textbf{und} bestellt werden.
	\item Wir \textbf{empfehlen} B\"ucher, die \"uber viele Schuljahre hinweg verwendet werden (z.B. \textbf{Atlas}, \textbf{Liederbuch}, \textbf{Tafelwerk}) oder in die zu \"Ubersetzungszwecken hineingeschrieben wird (Fremdsprachen), zu \textbf{kaufen}, da sie einem starken Verschleiß unterliegen.
	\item Bitte setzen Sie in jeder Zeile \textbf{genau ein Kreuz} (nicht mit Bleistift!). Erklärung der Abkürzungen:
	\begin{description}
		\item[V] Vorhanden (Dieses Buch ist bereits in Ihrem Besitz. Bitte beachten Sie die angegebene ISBN.)
		\item[K] Kauf (Dieses Buch m\"ochten Sie kaufen. Bitte beachten Sie die angegebene ISBN.)
		\item[F] Freiexemplar (Dieses Buch m\"ochten Sie von der Schule, nach den geltenden Bestimmungen des Landes Thüringen, ausleihen.)
	\end{description}
	\item Bitte \textbf{streichen} Sie die Zeilen der Kurse oder F\"acher, die \textbf{nicht belegt werden} (z.B. Wahlkurse, Ethik / Religion, Fremdsprache).
	\item Der Erwerb der Kaufexemplare und Arbeitshefte erfolgt in den f\"ur den Schulbuchverkauf zust\"andigen Verkaufsstellen (nicht im Gymnasium) durch die Eltern. Bitte den B\"ucherzettel erst nach dem {{s.data['deadline']['booklist_changes']}}{{year+1}} dort abgeben, falls \"Anderungen eintreten sollten.
	\item Wir bitte Sie den \textbf{ausgef\"ullten B\"ucherzettel} zwecks sp\"aterer Kontrolle und Buchkauf unbedingt mehrfach zu \textbf{kopieren}.
	\item Der Bücherzettel ist nach Erhalt auszufüllen und unverzüglich, jedoch \textbf{bis sp\"atestens {{s.data['deadline']['booklist_return']}}{{year+1}} beim Klassenleiter abzugeben}.

	\item Es besteht die M\"oglichkeit einen \textbf{Schulplaner} (HA, Termine, Noten\"ubersicht uvm.) von der Schule k\"auflich zu erwerben. Kreuzen Sie dies bitte an, wenn Sie einen solchen Schulplaner erwerben m\"ochten.

\end{enumerate}

\vspace{1cm}

Mit freundlichen Gr\"ußen

gez. {{s.data['general']['headteacher']}} \newline
Schulleiter

\vspace{1cm}

\newpage

\def\arraystretch{1.5}

\end{document}
