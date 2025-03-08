from datetime import date

from pony.orm import *


db = Database()


class Person(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    firstname = Required(str)
    # reverse attributes
    teacher = Optional("Teacher", cascade_delete=True)  # cascade to teacher
    student = Optional("Student", cascade_delete=True)  # cascade to person
    loan = Set("Loan", cascade_delete=False)  # restrict if loans assigned
    request = Set("Request", cascade_delete=True)  # cascade to request


class Teacher(db.Entity):
    id = PrimaryKey(int, auto=True)
    person = Required("Person")
    tag = Required(str, unique=True)
    # reverse attribute
    # restrict if class assigned
    class_ = Optional("Class", cascade_delete=False)

    def delete(self):
        self.person.delete()


class Class(db.Entity):
    id = PrimaryKey(int, auto=True)
    grade = Required(int)
    tag = Required(str)
    teacher = Optional(Teacher)
    # reverse attribute
    # restrict if students assigned
    student = Set("Student", cascade_delete=False)

    def to_string(self, advance=False, twoPlace=False):
        g = self.grade
        if advance:
            g += 1
        if twoPlace and g < 10:
            g = '0%d' % g
        else:
            g = str(g)
        return "%s%s" % (g,
                         self.tag.upper() if len(
                             self.tag) > 1 else self.tag)


class Student(db.Entity):
    id = PrimaryKey(int, auto=True)
    person = Required("Person")
    class_ = Required(Class)
    planner = Required(bool, default=False)

    def delete(self):
        self.person.delete()


class Subject(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    tag = Required(str, unique=True)
    elective = Required(bool, default=False)
    # reverse attribute
    book = Set("Book")


class Publisher(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    # reverse attribute
    book = Set("Book", cascade_delete=False)  # restrict if books assigned


class Book(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    isbn = Optional(str)  # book could be out of the shops
    price = Optional(int)  # in Euro Cents; book could be out of the shops
    publisher = Required(Publisher)
    stock = Required(int, default=0)  # not used for workbooks
    inGrade = Required(int)  # first grade that uses the book
    outGrade = Required(int)  # last grade that uses the book
    subject = Optional(Subject)  # None for subject-independent
    novices = Required(bool, default=False)  # suitable for novice courses?
    advanced = Required(bool, default=False)  # suitable for advanced courses?
    workbook = Required(bool, default=False)
    classsets = Required(bool, default=False)  # hence no loan
    for_loan = Required(bool, default=True)
    comment = Optional(str)
    # reverse attribute (not used for workbooks)
    loan = Set("Loan", cascade_delete=False)  # restrict if loans assigned
    # restrict if request assigned
    request = Set("Request", cascade_delete=False)

    def is_available(self):
        return self.isbn is not None and self.isbn != '' and self.price != None and self.price != 0

    def is_long_term(self):
        return self.outGrade - self.inGrade > 1

    def to_string(self):
        caption = self.title
        comments = list()
        if self.novices:
            comments.append('gA')
        if self.advanced:
            comments.append('eA')
        if self.comment:
            comments.append(self.comment)
        if self.classsets:
            comments.append('Klassensatz')
        comments.append(self.publisher.name)

        return caption + ' (%s)' % (', '.join(comments))

    def get_query_url(self):
        return 'https://www.google.com/search?q=%s %s %s' % (
            self.title, self.isbn, self.publisher.name)

    def get_grade_range(self) -> str:
        if self.inGrade == self.outGrade:
            return str(self.inGrade)
        
        return f'{self.inGrade}-{self.outGrade}'


class Currency(object):
    @staticmethod
    def to_string(cents: int, addSymbol=True):
        sym = '€' if addSymbol else ''
        eu = cents // 100
        ct = cents % 100
        if ct < 10:
            ct = '0{0}'.format(ct)
        return '{0},{1}{2}'.format(eu, ct, sym)

    @staticmethod
    def from_string(raw: str):
        tmp = raw.split('€')[0]
        if ',' in tmp:
            euro, cents = tmp.split(',')
            return int(euro) * 100 + int(cents)
        else:
            return int(tmp) * 100


class Loan(db.Entity):
    id = PrimaryKey(int, auto=True)
    person = Required(Person)
    book = Required(Book)
    given = Required(date)
    count = Required(int, default=1)

    def is_pending(self):
        if self.person.student is None:
            return False
        return self.person.student.class_.grade == self.book.outGrade

    def too_late(self):
        if self.person.student is None:
            return False
        return self.person.student.class_.grade > self.book.outGrade


class Request(db.Entity):
    id = PrimaryKey(int, auto=True)
    person = Required(Person)
    book = Required(Book)
