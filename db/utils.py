#!/usr/bin/python3
# -*- coding: utf-8 -*-

from db.orm import db
from pony.orm import *
from io import StringIO
import unittest
import os
import configparser
import datetime
import xlsxwriter

from bottle import template
from latex import build_pdf

from db import books, orga, loans
from db.orm import Currency


def shortName(firstname):
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


class Settings(object):

    def __init__(self):
        self.data = configparser.ConfigParser()
        self.data['general'] = {
            'school_year': '2019',
            'address': 'Example School \\ Neustadt \\ Tel: 123-456-78900',
            'headteacher': 'Mr. Boss'
        }
        self.data['deadline'] = {
            'booklist_return': '17.03.',
            'booklist_changes': '19.06.',
            'bookreturn_graduate': '17.03.'
        }

    def load_from(self, fhandle):
        tmp = configparser.ConfigParser()
        tmp.read_file(fhandle)
        # overwrite internal data
        self.data = tmp

    def save_to(self, fhandle):
        self.data.write(fhandle)

# -----------------------------------------------------------------------------


class SubjectCouncilXls(object):
    def __init__(self, settings_handle, export='export'):
        # prepare output directory
        if not os.path.isdir(export):  # base dir
            os.mkdir(export)
        self.export = os.path.join(export, 'councils')
        if not os.path.isdir(self.export):  # councils dir
            os.mkdir(self.export)
        # load settings
        self.s = Settings()
        self.s.load_from(settings_handle)
        self.data = None

    def getPath(self, subject):
        return os.path.join(self.export, '%s.xlsx' % subject.tag)

    def __call__(self, subject):
        self.data = xlsxwriter.Workbook(self.getPath(subject))

        """
        # create sheets
        sheets = [
            {'name': 'Lehrbücher', 'items': books.getRealBooksBySubject(subject, False)},
            {'name': 'Arbeitshefte', 'items': books.getWorkbooksBySubject(subject)},
            {'name': 'Klassensätze', 'items': books.getClasssetsBySubject(subject)},
        ]
        """

        items = {
            'Leihbuch': books.getRealBooksBySubject(subject, False),
            'AH': books.getWorkbooksBySubject(subject),
            'Klassensatz': books.getClasssetsBySubject(subject)
        }

        title_format = self.data.add_format()
        title_format.set_bold()

        euro_format = self.data.add_format({'num_format': '#,##0.00€'})

        center_format = self.data.add_format()
        center_format.set_align('center')

        """
        for s in sheets:
            tab = self.data.add_worksheet(s['name'])

            tab.set_column(0, 0, 40)
            tab.set_column(1, 1, 25)
            tab.set_column(2, 2, 20)
            tab.set_column(3, 3, 8, euro_format)
            tab.set_column(4, 4, 15, grade_format)
            tab.set_column(5, 5, 30)

            for col, caption in enumerate(['Titel', 'Verlag', 'ISBN', 'Preis', 'Klassenstufe', 'Bemerkungen']):
                tab.write(0, col, caption, title_format)

            for row, b in enumerate(s['items']):
                tab.write(row+1, 0, b.title)
                if b.publisher is not None:
                    tab.write(row+1, 1, b.publisher.name)
                if b.isbn is not None:
                    tab.write(row+1, 2, b.isbn)
                if b.price is not None:
                    tab.write(row+1, 3, b.price / 100.0)
                if b.inGrade == b.outGrade:
                    tab.write(row+1, 4, b.inGrade)
                else:
                    tab.write(row+1, 4, '%d-%d' % (b.inGrade, b.outGrade))

                comments = list()
                if b.comment != '':
                    comments.append(b.comment)
                if b.novices:
                    comments.append('gA')
                if b.advanced:
                    comments.append('eA')
                tab.write(row+1, 5, ' '.join(comments))
        """

        tab = self.data.add_worksheet(subject.tag)
        tab.set_landscape()
        tab.set_footer('Bücherbedarf &A (Stand &D)')
        tab.set_margins(top=1.25)

        tab.set_column(0, 0, 25)
        tab.set_column(1, 1, 20)
        tab.set_column(2, 2, 20)
        tab.set_column(3, 3, 8, euro_format)
        tab.set_column(4, 4, 8, center_format)
        tab.set_column(5, 5, 10, center_format)
        tab.set_column(6, 6, 25)

        for col, caption in enumerate(
                ['Titel', 'Verlag', 'ISBN', 'Preis', 'Klasse', 'Art', 'Bemerkungen']):
            tab.write(0, col, caption, title_format)

        row = 0
        for kind in ['Leihbuch', 'AH', 'Klassensatz']:
            for b in items[kind]:
                tab.write(row + 1, 0, b.title)
                if b.publisher is not None:
                    tab.write(row + 1, 1, b.publisher.name)
                if b.isbn is not None:
                    tab.write(row + 1, 2, b.isbn)
                if b.price is not None:
                    tab.write(row + 1, 3, b.price / 100.0)
                if b.inGrade == b.outGrade:
                    tab.write(row + 1, 4, b.inGrade)
                else:
                    tab.write(row + 1, 4, '%d-%d' % (b.inGrade, b.outGrade))
                tab.write(row + 1, 5, kind)

                comments = list()
                if b.comment != '':
                    comments.append(b.comment)
                if b.novices:
                    comments.append('gA')
                if b.advanced:
                    comments.append('eA')
                tab.write(row + 1, 6, ' '.join(comments))

                row += 1

    def saveToFile(self):
        assert(self.data is not None)
        self.data.close()

# -----------------------------------------------------------------------------


class PlannerXls(object):
    def __init__(self, export='export'):
        # prepare output directory
        if not os.path.isdir(export):  # base dir
            os.mkdir(export)
        self.fname = 'planner.xlsx'
        self.path = os.path.join(export, self.fname)
        self.data = xlsxwriter.Workbook(self.path)

    def __call__(self, classes, advance):
        tab = self.data.add_worksheet('Schulplaner')

        title_format = self.data.add_format()
        title_format.set_bold()
        title_format.set_align('center')

        center_format = self.data.add_format()
        center_format.set_align('center')

        tab.set_column(0, 0, 10, center_format)
        tab.set_column(1, 1, 10, center_format)
        tab.write(0, 0, 'Klasse', title_format)
        tab.write(0, 1, 'Anzahl', title_format)

        # query planner
        planner = db.Book.select(
            lambda b: b.publisher.name == 'schulintern').first()

        row = 1
        for c in classes:
            n = 0
            for s in c.student:
                for l in s.person.request:
                    if l.book == planner:
                        n += 1
                        break
            tab.write(row, 0, c.toString(advance=advance))
            tab.write(row, 1, n)
            row += 1

    def saveToFile(self):
        assert(self.data is not None)
        self.data.close()

# -----------------------------------------------------------------------------


class DatabaseDumpXls(object):
    def __init__(self, settings_handle, export='export'):
        # prepare output directory
        if not os.path.isdir(export):  # base dir
            os.mkdir(export)
        self.export = export
        # load settings
        self.s = Settings()
        self.s.load_from(settings_handle)
        # setup xlsx file
        path = os.path.join(
            self.export, '%s.xlsx' %
            self.s.data['general']['school_year'])
        self.data = xlsxwriter.Workbook(path)

    def getPath(self):
        return os.path.join(
            self.export, '%s.xlsx' %
            self.s.data['general']['school_year'])

    def __call__(self, class_, bks):
        # local import to avoid cycles
        from db import loans

        # pre-order students abd books
        bks = books.orderBooksList(bks)
        students = list(class_.student)
        orga.sortStudents(students)

        title_format = self.data.add_format()
        title_format.set_bold()

        rotate_format = self.data.add_format()
        rotate_format.set_rotation(90)

        # create tab sheet for this class
        tab = self.data.add_worksheet(class_.toString())
        tab.set_column(0, 1, 12)
        tab.set_column(2, 2 + len(bks), 4)
        tab.set_row(0, 150, rotate_format)

        fields = ['Name', 'Vorname']
        for col, b in enumerate(bks):
            fields.append(b.subject.tag if b.subject is not None else '')
            tab.write(0, col + 2, b.title)  # todo: 90° rotated format
        for col, caption in enumerate(fields):
            tab.write(1, col, caption, title_format)

        # fill students in
        for row, s in enumerate(students):
            tab.write(row + 2, 0, s.person.name)
            tab.write(row + 2, 1, shortName(s.person.firstname))
            for col, b in enumerate(bks):
                n = loans.getLoanCount(s.person, b)
                tab.write(row + 2, col + 2, n if n > 0 else '')

    def saveToFile(self):
        assert(self.data is not None)
        self.data.close()

# -----------------------------------------------------------------------------


class ClasssetsPdf(object):
    def __init__(self, prefix, settings_handle, threshold, export='export'):
        """ All books, that are either class sets or if more than `threshold`
        pieces are loaned by a person, are written to the PDF. """
        # load LaTeX templates
        with open('docs/classsets/header.tpl') as f:
            self.header = f.read()
        with open('docs/classsets/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/classsets/content.tpl') as f:
            self.content = f.read()
        # prepare output directory
        self.prefix = prefix
        self.export = export
        self.texdir = os.path.join(export, 'tex')
        if not os.path.isdir(self.texdir):
            os.mkdir(self.texdir)
        # load settings
        self.s = Settings()
        self.s.load_from(settings_handle)

        self.tex = template(self.header)
        self.threshold = threshold

        # used to page break not too often
        self.page_count = 0

    def getPath(self):
        return os.path.join(self.export, 'Klassensätze_%s.pdf' % self.prefix)

    def __call__(self, person):
        """Generate loan report pdf file for the given person. This will contain
        all books that are currently given to this person
        """
        # count books before running template
        lns = loans.orderLoanOverview(person.loan)
        n = 0
        for l in lns:
            if l.count > self.threshold:
                n += 1

        if n > 0:
            self.page_count += 1
            # run template only if books are relevant
            self.tex += template(self.content,
                                 s=self.s,
                                 p=person,
                                 lns=lns,
                                 threshold=self.threshold,
                                 pagebreak=self.page_count % 2 == 0)

    def saveToFile(self):
        self.tex += template(self.footer)

        # export tex (debug purpose)
        dbg_fname = os.path.join(
            self.texdir,
            'Klassensätze_%s.tex' %
            self.prefix)
        with open(dbg_fname, 'w') as h:
            h.write(self.tex)

        # export PDF
        fname = self.getPath()
        pdf = build_pdf(self.tex)
        pdf.save_to(fname)

# -----------------------------------------------------------------------------


class InventoryReport(object):
    def __init__(self, settings_handle, export='export'):
        # load LaTeX templates
        with open('docs/inventoryreport/header.tpl') as f:
            self.header = f.read()
        with open('docs/inventoryreport/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/inventoryreport/content.tpl') as f:
            self.content = f.read()
        # prepare output directory
        self.export = export
        self.texdir = os.path.join(export, 'tex')
        if not os.path.isdir(self.texdir):
            os.mkdir(self.texdir)
        # load settings
        self.s = Settings()
        self.s.load_from(settings_handle)

        self.tex = template(self.header)

    def getPath(self):
        return os.path.join(self.export, 'Inventarbericht.pdf')

    def __call__(self):
        """Collect all books (existing, loaned, remaining)
        """
        all_bks = books.getRealBooks()
        all_bks = books.orderBooksIndex(all_bks)

        loan_count = dict()
        for b in all_bks:
            loan_count[b] = loans.getLoanCount(person=None, book=b)

        self.tex += template(self.content, s=self.s,
                             all_bks=all_bks, loan_count=loan_count)

    def saveToFile(self):
        self.tex += template(self.footer)

        # export tex (debug purpose)
        dbg_fname = os.path.join(self.texdir, 'Inventarbericht.tex')
        with open(dbg_fname, 'w') as h:
            h.write(self.tex)

        # export PDF
        fname = self.getPath()
        pdf = build_pdf(self.tex)
        pdf.save_to(fname)

# -----------------------------------------------------------------------------


class LoanReportPdf(object):
    def __init__(self, prefix, settings_handle, export='export'):
        # load LaTeX templates
        with open('docs/loanreport/header.tpl') as f:
            self.header = f.read()
        with open('docs/loanreport/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/loanreport/content.tpl') as f:
            self.content = f.read()
        # prepare output directory
        self.prefix = prefix
        self.export = export
        self.texdir = os.path.join(export, 'tex')
        if not os.path.isdir(self.texdir):
            os.mkdir(self.texdir)
        # load settings
        self.s = Settings()
        self.s.load_from(settings_handle)

        self.tex = template(self.header)

    def getPath(self):
        return os.path.join(self.export, 'Leihübersicht_%s.pdf' % self.prefix)

    def __call__(self, person):
        """Generate loan report pdf file for the given person. This will contain
        all books that are currently given to this person
        """
        lns = loans.orderLoanOverview(person.loan)
        self.tex += template(self.content, s=self.s, p=person, lns=lns)

    def saveToFile(self):
        self.tex += template(self.footer)

        # export tex (debug purpose)
        dbg_fname = os.path.join(
            self.texdir,
            'Leihübersicht_%s.tex' %
            self.prefix)
        with open(dbg_fname, 'w') as h:
            h.write(self.tex)

        # export PDF
        fname = self.getPath()
        pdf = build_pdf(self.tex)
        pdf.save_to(fname)

# -----------------------------------------------------------------------------


class LoanContractPdf(object):
    def __init__(
            self,
            prefix,
            settings_handle,
            export='export',
            advance=False):
        # load LaTeX templates
        with open('docs/loancontract/header.tpl') as f:
            self.header = f.read()
        with open('docs/loancontract/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/loancontract/content.tpl') as f:
            self.content = f.read()
        # prepare output directory
        self.prefix = prefix
        if not os.path.isdir(export):  # base dir
            os.mkdir(export)
        self.export = os.path.join(export, 'contracts')
        self.texdir = os.path.join(export, 'tex')
        if not os.path.isdir(self.export):  # specific dir
            os.mkdir(self.export)
        if not os.path.isdir(self.texdir):
            os.mkdir(self.texdir)
        # load settings
        self.s = Settings()
        self.s.load_from(settings_handle)

        self.tex = template(self.header)
        self.advance = advance

    def getPath(self):
        return os.path.join(self.export, 'Leihverträge_%s.pdf' % self.prefix)

    def __call__(self, student, include_requests=False, loan_report=False):
        """Generate loan contract pdf file for the given student. This contains
        all books that are currently given to him or her. With 'loan_report'
        all books are listed as "you loan these books"
        """
        lns = loans.orderLoanOverview(student.person.loan)
        rqs = list()
        if include_requests:
            rqs = loans.orderRequestOverview(student.person.request)
        self.tex += template(self.content,
                             s=self.s,
                             student=student,
                             lns=lns,
                             rqs=rqs,
                             advance=self.advance,
                             loan_report=loan_report)

    def saveToFile(self):
        self.tex += template(self.footer)

        # export tex (debug purpose)
        dbg_fname = os.path.join(
            self.texdir,
            'Leihverträge_%s.tex' %
            self.prefix)
        with open(dbg_fname, 'w') as h:
            h.write(self.tex)

        # export PDF
        fname = self.getPath()
        pdf = build_pdf(self.tex)
        pdf.save_to(fname)

# -----------------------------------------------------------------------------


class BooklistPdf(object):
    def __init__(self, settings_handle, export='export'):
        # load LaTeX templates
        with open('docs/booklist/header.tpl') as f:
            self.header = f.read()
        with open('docs/booklist/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/booklist/info.tpl') as f:
            self.info = f.read()
        with open('docs/booklist/select.tpl') as f:
            self.select = f.read()
        with open('docs/booklist/empty.tpl') as f:
            self.empty = f.read()
        with open('docs/booklist/special.tpl') as f:
            self.special = f.read()
        # prepare output directory
        if not os.path.isdir(export):  # base dr
            os.mkdir(export)
        self.export = os.path.join(export, 'booklists')
        self.texdir = os.path.join(export, 'tex')
        if not os.path.isdir(self.export):  # specific dir
            os.mkdir(self.export)
        if not os.path.isdir(self.texdir):
            os.mkdir(self.texdir)
        # load settings
        self.s = Settings()
        self.s.load_from(settings_handle)

    def __call__(self, grade: int, exclude: set, new_students: bool = False):
        """Generate booklist pdf file for the given grade. A separate booklist
        can be generated for new_students, which include additional books other
        students already have from earlier classes.
        The provided exclude set can be used to exclude books from the
        booklist. The keys are built from <grade>_<bookid>, if excluded this
        key's value is set to false.
        """
        # fetch special books
        spec_bks = books.getBooksUsedIn(0, True)

        # fetch and order books
        if new_students:
            bks = books.getBooksUsedIn(grade, booklist=True)
            suffix = '_Neuzugänge'
            deadline = 'Abgabe bei Anmeldung'
        else:
            bks = books.getBooksStartedIn(grade, booklist=True)
            suffix = ''
            date = self.s.data['deadline']['booklist_return']
            year = int(self.s.data['general']['school_year'])
            deadline = f'Abgabe bis spätestens {date}{year+1}'
        bks = books.orderBooksList(bks)
        if grade == 5:
            deadline = 'Abgabe bei Anmeldung'

        # determine number of books
        num_books = sum(1 for b in bks if not b.workbook)

        # render templates
        tex = template(
            self.header,
            s=self.s,
            grade=grade,
            new_students=new_students,
            deadline=deadline)
        # render pure books
        if num_books > 0:
            tex += template(self.select,
                            grade=grade,
                            bs=bks,
                            workbook=False,
                            exclude=exclude,
                            new_students=new_students)
        else:
            tex += template(self.empty, workbook=False,
                            new_students=new_students)
        # render pure workbooks
        if num_books < len(bks):
            tex += template(self.select,
                            grade=grade,
                            bs=bks,
                            workbook=True,
                            exclude=exclude,
                            new_students=new_students)
        else:
            tex += template(self.empty, workbook=True,
                            new_students=new_students)
        tex += template(self.special, grade=grade, s=self.s, spec_bks=spec_bks)
        tex += template(self.footer, s=self.s)

        # export tex (debug purpose)
        dbg_fname = os.path.join(self.texdir, '%d_%s.tex' % (grade, suffix))
        with open(dbg_fname, 'w') as h:
            h.write(tex)

        # export PDF
        fname = os.path.join(
            self.export, 'Bücherzettel%d%s.pdf' %
            (grade, suffix))
        pdf = build_pdf(tex)
        pdf.save_to(fname)

    def infosheet(self):
        # render templates
        tex = template(self.info, s=self.s)

        # export tex (debug purpose)
        dbg_fname = os.path.join(self.texdir, 'info.tex')
        with open(dbg_fname, 'w') as h:
            h.write(tex)

        # export PDF
        fname = os.path.join(self.export, 'Bücherzettel_Information.pdf')
        pdf = build_pdf(tex)
        pdf.save_to(fname)

# -----------------------------------------------------------------------------


class RequestlistPdf(object):

    def __init__(self, settings_handle, export='export'):
        # load LaTeX templates
        with open('docs/requestlist/header.tpl') as f:
            self.header = f.read()
        with open('docs/requestlist/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/requestlist/content.tpl') as f:
            self.content = f.read()
        # prepare output directory
        self.export = export
        self.texdir = os.path.join(export, 'tex')
        if not os.path.isdir(self.texdir):
            os.mkdir(self.texdir)
        # load settings
        self.s = Settings()
        self.s.load_from(settings_handle)

        self.tex = template(self.header)

    def getPath(self):
        return os.path.join(self.export, 'Bücherzettel_Erfassungsliste.pdf')

    def __call__(self, class_):
        """Generate requestlist pdf file for the given class.
        """
        # fetch specific books
        spec_bks = books.getBooksUsedIn(0, True)

        # fetch and order books that are used next year by this class
        bks = books.getBooksStartedIn(class_.grade + 1, booklist=True)
        bks = books.orderBooksList(bks)

        # query students
        students = orga.getStudentsIn(class_.grade, class_.tag)

        # render template
        self.tex += template(self.content,
                             s=self.s,
                             class_=class_,
                             bks=bks,
                             students=students,
                             spec_bks=spec_bks)

    def saveToFile(self):
        self.tex += template(self.footer)

        # export tex (debug purpose)
        dbg_fname = os.path.join(self.texdir, 'Erfassungsliste.tex')
        with open(dbg_fname, 'w') as h:
            h.write(self.tex)

        # export PDF
        fname = self.getPath()
        pdf = build_pdf(self.tex)
        pdf.save_to(fname)

# -----------------------------------------------------------------------------


class BookreturnPdf(object):

    def __init__(self, settings_handle, export='export'):
        # load LaTeX templates
        with open('docs/bookreturn/header.tpl') as f:
            self.header = f.read()
        with open('docs/bookreturn/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/bookreturn/content.tpl') as f:
            self.content = f.read()
        with open('docs/bookreturn/overview.tpl') as f:
            self.overview = f.read()
        # prepare output directory
        self.export = export
        self.texdir = os.path.join(export, 'tex')
        if not os.path.isdir(self.texdir):
            os.mkdir(self.texdir)
        # load settings
        self.s = Settings()
        self.s.load_from(settings_handle)

        self.tex = template(self.header)

    def getPath(self):
        return os.path.join(self.export, 'Rückgaben.pdf')

    def addOverview(self, grade):
        """Generate overviews for class teachers about returning books.
        """
        # fetch and order books that are used next year by this class
        bks = books.getBooksFinishedIn(grade)
        bks = books.orderBooksList(bks)

        # render template
        self.tex += template(self.overview, s=self.s, grade=grade, bks=bks)

    def __call__(self, class_):
        """Generate requestlist pdf file for the given class.
        """
        # fetch and order books that are used next year by this class
        bks = books.getBooksFinishedIn(class_.grade)
        bks = books.orderBooksList(bks)

        # query students
        students = orga.getStudentsIn(class_.grade, class_.tag)

        # render template
        self.tex += template(self.content, s=self.s,
                             class_=class_, bks=bks, students=students)

    def saveToFile(self):
        self.tex += template(self.footer)

        # export tex (debug purpose)
        dbg_fname = os.path.join(self.texdir, 'Rückgaben.tex')
        with open(dbg_fname, 'w') as h:
            h.write(self.tex)

        # export PDF
        fname = self.getPath()
        pdf = build_pdf(self.tex)
        pdf.save_to(fname)


# -----------------------------------------------------------------------------

class BookloanPdf(object):

    def __init__(self, settings_handle, export='export'):
        # load LaTeX templates
        with open('docs/bookloan/header.tpl') as f:
            self.header = f.read()
        with open('docs/bookloan/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/bookloan/content.tpl') as f:
            self.content = f.read()
        # prepare output directory
        self.export = export
        self.texdir = os.path.join(export, 'tex')
        if not os.path.isdir(self.texdir):
            os.mkdir(self.texdir)
        # load settings
        self.s = Settings()
        self.s.load_from(settings_handle)

        self.tex = template(self.header)

    def getPath(self):
        return os.path.join(self.export, 'Ausgaben.pdf')

    def __call__(self, class_, request=False):
        """Generate requestlist pdf file for the given class. If `requests` is
        provided with true, the request list for this year is used.
        """
        grade = class_.grade
        if request:
            grade += 1

        # fetch and order books that were requested by this class
        bks = books.getBooksUsedIn(grade)
        bks = books.orderBooksList(bks)

        # fetch special books
        spec_bks = books.getBooksUsedIn(0, True)

        # query students
        students = orga.getStudentsIn(class_.grade, class_.tag)

        if request:
            query_func = loans.getRequestCount
        else:
            query_func = loans.getLoanCount

        # render template
        self.tex += template(self.content,
                             s=self.s,
                             class_=class_,
                             bks=bks,
                             students=students,
                             spec_bks=spec_bks,
                             query_func=query_func,
                             advance=request)

    def saveToFile(self):
        self.tex += template(self.footer)

        # export tex (debug purpose)
        dbg_fname = os.path.join(self.texdir, 'Ausgaben.tex')
        with open(dbg_fname, 'w') as h:
            h.write(self.tex)

        # export PDF
        fname = self.getPath()
        pdf = build_pdf(self.tex)
        pdf.save_to(fname)

# -----------------------------------------------------------------------------


class BookpendingPdf(object):

    def __init__(self, settings_handle, export='export'):
        # load LaTeX templates
        with open('docs/bookpending/header.tpl') as f:
            self.header = f.read()
        with open('docs/bookpending/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/bookpending/page_header.tpl') as f:
            self.page_header = f.read()
        with open('docs/bookpending/page_footer.tpl') as f:
            self.page_footer = f.read()
        with open('docs/bookpending/page_content.tpl') as f:
            self.page_content = f.read()
        # prepare output directory
        self.texdir = os.path.join(export, 'tex')
        if not os.path.isdir(self.texdir):
            os.mkdir(self.texdir)
        self.export = os.path.join(export, 'pending')
        if not os.path.isdir(self.export):
            os.mkdir(self.export)
        # load settings
        self.s = Settings()
        self.s.load_from(settings_handle)

        self.tex = template(self.header)

        self.n = 0

    def queryBooks(self, grade: int, tooLate=False):
        """Query and add all pending books for the given grade.
        """
        if tooLate:
            def test(l): return l.tooLate()
        else:
            def test(l): return l.isPending()

        n = 0
        # iterate students in classes in grade
        for b in books.getBooksFinishedIn(grade):
            k = 0
            # ignore class sets
            if b.classsets:
                continue
            # add all pending loan records
            page = template(self.page_header, book=b)
            for l in loans.queryLoansByBook(b):
                # add if pending
                if test(l):
                    page += template(self.page_content, l=l, i=k)
                    k += 1
            page += template(self.page_footer)
            # add page to document if at least one student was found
            if k > 0:
                self.tex += page
            n += k

        return n

    def saveToFile(self, suffix, with_date=False):
        self.tex += template(self.footer)

        ext = ''
        if with_date:
            ext = '_%s' % datetime.datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
        pdfname = 'AusstehendeBücher_%s%s' % (suffix, ext)

        # export tex (debug purpose)
        dbg_fname = os.path.join(self.texdir, '%s.tex' % pdfname)
        with open(dbg_fname, 'w') as h:
            h.write(self.tex)

        # export PDF
        fname = os.path.join(self.export, '%s.pdf' % pdfname)
        pdf = build_pdf(self.tex)
        pdf.save_to(fname)

        return pdfname

# -----------------------------------------------------------------------------


class ClassListPdf(object):
    def __init__(self, settings_handle, export='export'):
        # load LaTeX templates
        with open('docs/classlist/header.tpl') as f:
            self.header = f.read()
        with open('docs/classlist/footer.tpl') as f:
            self.footer = f.read()
        with open('docs/classlist/content.tpl') as f:
            self.content = f.read()
        # prepare output directory
        self.export = export
        self.texdir = os.path.join(export, 'tex')
        if not os.path.isdir(self.texdir):
            os.mkdir(self.texdir)
        # load settings
        self.s = Settings()
        self.s.load_from(settings_handle)

        self.tex = template(self.header)

    def getPath(self):
        return os.path.join(self.export, 'Klassenliste.pdf')

    def __call__(self, classes):
        """Add classes to the listing
        """
        self.tex += template(self.content, s=self.s, classes=classes)

    def saveToFile(self):
        self.tex += template(self.footer)

        # export tex (debug purpose)
        dbg_fname = os.path.join(self.texdir, 'Klassenliste.tex')
        with open(dbg_fname, 'w') as h:
            h.write(self.tex)

        # export PDF
        fname = self.getPath()
        pdf = build_pdf(self.tex)
        pdf.save_to(fname)

# -----------------------------------------------------------------------------


class Tests(unittest.TestCase):

    @staticmethod
    @db_session
    def prepare():
        import db.orga
        import db.books
        import db.orga

        db.orga.Tests.prepare()
        db.books.Tests.prepare()

    def setUp(self):
        db.create_tables()

    def tearDown(self):
        db.drop_all_tables(with_all_data=True)

    @db_session
    def test_create_custom_booklist(self):
        # create custom database content (real world example)
        books.addSubjects(
            "Mathematik\tMa\nDeutsch\tDe\nEnglisch\tEn\nPhysik\tPh")
        books.addPublishers("Klett\nCornelsen")
        books.addBooks(
            """Ein Mathe-Buch\t978-3-7661-5000-4\t32,80 €\tCornelsen\t5\t12\tMa\tTrue\tTrue\tFalse\tFalse\tTrue
Mathe AH\t978-3-7661-5007-3\t8,80 €\tCornelsen\t5\t12\tMa\tTrue\tTrue\tTrue\tFalse\tTrue
Deutsch-Buch mit sehr langam Titel und damit einigen Zeilenumbrüchen .. ach und Umlaute in größeren Mengen öÖäÄüÜß sowie Sonderzeichen !"§$%&/()=?.:,;-_@\t978-3-12-104104-6\t35,95 €\tKlett\t11\t12\tDe\tTrue\tTrue\tFalse\tFalse\tTrue
Old English Book\t\t\tKlett\t5\t12\tEn\tTrue\tTrue\tFalse\tTrue\tTrue
Grundlagen der Physik\t\t\tCornelsen\t5\t12\tPh\tTrue\tTrue\tFalse\tFalse\tTrue
Tafelwerk\t978-3-06-001611-2\t13,50 €\tCornelsen\t7\t12\tFalse\tFalse\tFalse\tFalse\tTrue""")

        exclude = set()
        exclude.add('11_1')  # "Ein Mathe-Buch"

        # create booklist
        with open('settings.ini') as h:
            booklist = BooklistPdf(h, export='/tmp/export')
        booklist(11, new_students=True, exclude=exclude)
        print('PLEASE MANUALLY VIEW /tmp/export/Buecherzettel11.pdf')

    @db_session
    def test_create_custom_requestlist(self):
        Tests.prepare()

        # create custom database content (real world example)
        books.addSubjects("Deutsch\tDe\nPhysik\tPh")
        books.addBooks(
            """Ein Mathe-Buch\t978-3-7661-5000-4\t32,80 €\tCornelsen\t5\t12\tMa\tTrue\tTrue\tFalse\tFalse\tTrue
Mathe AH\t978-3-7661-5007-3\t8,80 €\tCornelsen\t5\t12\tMa\tTrue\tTrue\tTrue\tFalse\tTrue
Deutsch-Buch mit sehr langam Titel und damit einigen Zeilenumbrüchen .. ach und Umlaute in größeren Mengen öÖäÄüÜß sowie Sonderzeichen !"§$%&/()=?.:,;-_@\t978-3-12-104104-6\t35,95 €\tKlett\t11\t12\tDe\tTrue\tTrue\tFalse\tFalse\tTrue
Old English Book\t\t\tKlett\t5\t12\tEn\tTrue\tTrue\tFalse\tTrue\tTrue
Grundlagen der Physik\t\t\tCornelsen\t5\t12\tPh\tTrue\tTrue\tFalse\tFalse\tTrue
Tafelwerk\t978-3-06-001611-2\t13,50 €\tCornelsen\t7\t12\tFalse\tFalse\tFalse\tFalse\tTrue""")

        # create requestlists
        with open('settings.ini') as h:
            requestlist = RequestlistPdf(h, export='/tmp/export')
        for c in select(c for c in db.Class):
            requestlist(c)
        requestlist.saveToFile()

        print('PLEASE MANUALLY VIEW /tmp/export/Erfassungsliste.pdf')
