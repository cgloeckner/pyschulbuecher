%from db.orm import Currency
%from utils import tex_escape

\def\arraystretch{1.25}

{\large
%if workbook:
    Arbeitshefte
%else:
    Lehrbücher \hfill  \footnotesize (\textbf{\large V}orhanden, privater \textbf{\large K}auf oder \textbf{\large F}reiexemplar)
%end
}

%if workbook:
\begin{longtable}{ | c | p{6cm} | p{2.8cm} | c | r | }
%else:
\begin{longtable}{ | c | p{4.5cm} | p{2cm} | c | r | p{0.66cm} | p{0.66cm} | p{0.66cm} | }
%end
\hline
\textbf{Fach} & \textbf{Titel} & \textbf{Verlag} & \textbf{ISBN} & \textbf{Preis}
%if not workbook:
 & \textbf{\enspace V} & \textbf{\enspace K} & \textbf{\enspace F}
%end
\\ \hline
%for b in bs:
    %if new_students:
        %key = '{0}_neu_{1}'.format(grade, b.id)
    %else:
        %key = '{0}_{1}'.format(grade, b.id)
    %end
    %if b.workbook == workbook:
        %if key in exclude:
            %print('Skip {0} for grade {1}'.format(b.title, grade))
            %continue
        %end
        %if b.subject is not None:
            %ga = b.novices
            %ea = b.advanced
            %cmt = len(b.comment) > 0
            %if ga or ea or cmt:
    \makecell{
            %end
        {\small {{!tex_escape(b.subject.tag)}} }
            %if grade > 10:
                %if ea and ga:
                    %pass
                %else:
                    %if ea:
        {\footnotesize eA }
                    %end
                    %if ga:
        {\footnotesize gA }
                    %end
                %end
            %end
            %if cmt:
        \\ {\footnotesize {{!tex_escape(b.comment)}} }
            %end
            %if cmt or ga or ea:
    }
            %end
        %else:
    {\small versch. }
        %end
    & 
    {\small {{!tex_escape(b.title)}} }
    &
    {\small {{!tex_escape(b.publisher.name)}}}
    &
        %if b.isAvailable():
    {\small {{!tex_escape(b.isbn)}} }
        &
    {\small {{!tex_escape(Currency.toString(b.price, addSymbol=False))}} \euro }
            %if not b.workbook:
    &
                %if b.classsets:
    \multicolumn{3}{c|} { \small { Klassens\"atze } }
                %else:
                    %if not b.isAvailable():
    \cellcolor{black!75}
    &
    \cellcolor{black!75}
    &
    \checkinput
                    %else:
    \checkinput & \checkinput & \checkinput
                    %end
                %end
            %end
        %else:
    \multicolumn{4}{c|}{\small {\textit {{nicht mehr erh\"altlich}} } }
            %if b.inGrade > 10:
    & \checkinput
            %else:
    & \checkedinput
            %end
        %end
    \\
    \hline
    %end
%end
\end{longtable}
