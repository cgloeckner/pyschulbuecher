import locale

from pony.orm import *
from pony import orm

from app.settings import *
from app.db import db, db_session


def get_grade_range():
    return range(entry_grade, graduation_grade + 1)

def get_persisting_grade_range(delta=0):
    return range(entry_grade + delta, graduation_grade + delta)


def get_secondary_level1_range():
    return range(entry_grade, course_grade)


def get_secondary_level2_range():
    return range(course_grade, graduation_grade + 1)


def get_class_grades(regular=False):
    """Return a list of grades for which classes exist.
    If regular class grades are queried, entry and alumni grade are excluded.
    """
    classes = None
    if regular:
        classes = select(c.grade for c in db.Class if c.grade in get_grade_range()).order_by(lambda g: g)
    else:
        classes = select(c.grade for c in db.Class).order_by(lambda g: g)
    return set(classes)


def get_class_tags(grade: int):
    """Return a list of tags for which classes exist in the given grade.
    """
    return select(c.tag for c in db.Class if c.grade == grade).order_by(lambda t: t)


def get_classes():
    """Return a list of all existing classes.
    """
    return select(c for c in db.Class)


def get_classes_by_grade(grade: int):
    """Return a list of classes which exist in the given grade.
    """
    return select(c for c in db.Class if c.grade == grade).order_by(db.Class.tag)


def get_classes_count():
    """Return total number of classes.
    """
    return db.Class.select().count()


def sort_classes(classes: list):
    """Sort classes by grade (primary) and tag (secondary)."""
    classes.sort(key=lambda c: locale.strxfrm(c.tag))
    classes.sort(key=lambda c: c.grade)


def get_students_count(grade: int):
    """Return total number of students in the given grade.
    """
    cs = get_classes_by_grade(grade)
    total = 0
    for c in cs:
        total += len(c.student)
    return total


def phonebook_key(name):
    """Normalize names for German phonebook sorting (DIN 5007-1)."""
    umlaut_map = str.maketrans("äöüß", "aous")  # Treat umlauts as base vowels
    return name.translate(umlaut_map).upper()


def sort_students(students: list):
    """Sort students by name (primary) and firstname (secondary). This
    considers Umlate while sorting, e.h. handling O and Ö equally instead of
    sorting Ö after Z, do not sort "van Something" behind "Z"
    """
    students.sort(key=lambda s: (phonebook_key(s.person.name), s.person.firstname))


def get_students_in(grade: int, tag: str):
    """Return all students in the given grade.
    """
    # Note: explicit list conversion + sort (instead directly order_by)
    l = list(db.Class.get(grade=grade, tag=tag).student)
    sort_students(l)
    return l

# -----------------------------------------------------------------------------


def parse_class(raw: str):
    """Parse class grade and tag from a raw string.
    """
    grade = raw[:2]
    tag = raw.split(grade)[1].lower()
    return int(grade), tag


def add_class(raw: str):
    """Add a new class from a ggiven raw string. This string contains the
    grade (with ALWAYS two characters, like '08') followed by the class tag
    (e.g. '08a'), where uppercase characters are ignored. No teacher is
    assigned to this class.
    """
    # split data
    grade, tag = parse_class(raw)

    existing = select(c for c in db.Class if c.grade == grade and c.tag == tag)
    if existing.count() > 0:
        raise orm.core.ConstraintError('Class %s aready existing' % raw)

    db.Class(grade=grade, tag=tag)


def add_classes(raw: str):
    """Add classes from a given raw string dump, assuming all students being
    separated by newlines. Each line is handled by add_class().
    """
    for data in raw.split('\n'):
        if len(data) > 0:
            add_class(data)


def update_class(id: int, grade: int, tag: str, teacher_id: int):
    # try to query class with grade and tag
    cs = select(c for c in db.Class if c.grade == grade and c.tag == tag)
    if cs.count() > 0:
        assert(cs.count() == 1)
        if cs.get().id != id:
            raise orm.core.ConstraintError(
                'Ambiguous class %d%s' %
                (grade, tag))

    # update class
    c = db.Class[id]
    c.grade = grade
    c.tag = tag
    if teacher_id > 0:
        c.teacher = db.Teacher[teacher_id]
    else:
        c.teacher = None

# -----------------------------------------------------------------------------


def get_student_count():
    """Return total number of students.
    """
    return db.Student.select().count()


def add_student(raw: str):
    """Add a new students from a given raw string dump, assuming all
    information being separated by tabs in the following order:
        Class, Name, FirstName
    Note that the Class must contain both, grade and tag (e.g. `08A` or
    `11ABC`). If a class does not exist, it needs to be added in the first
    place. Uppercase class tags are ignored.
    """
    # split data
    data = raw.split('\t')
    grade, tag = parse_class(data[0])
    name, firstname = data[1], data[2]

    # query referenced class
    class_ = db.Class.get(grade=grade, tag=tag)

    try:
        # create actual student
        db.Student(
            person=db.Person(
                name=name,
                firstname=firstname),
            class_=class_)
    except ValueError as e:
        raise orm.core.ConstraintError(e)


def add_students(raw: str):
    """Add students from a given raw string dump, assuming all students being
    separated by newlines. Each line is handled by add_student().
    """
    for data in raw.split('\n'):
        if len(data) > 0:
            add_student(data)


def get_students_like(name: str = "", firstname: str = ""):
    """Return a list of students by name and firstname using partial matching.
    Both parameters default to an empty string if not specified.
    """
    return select(
        s for s in db.Student
        if name.lower() in s.person.name.lower() and firstname.lower() in s.person.firstname.lower()
    ).order_by(
        lambda s: s.person.firstname
    ).order_by(
        lambda s: s.person.name
    ).order_by(
        lambda s: s.class_.tag
    ).order_by(
        lambda s: s.class_.grade
    )

# -----------------------------------------------------------------------------


def get_teacher_count():
    """Return total number of teachers.
    """
    return db.Teacher.select().count()


def get_teachers():
    """Return all teachers sorted.
    """
    return select(
        t for t in db.Teacher).order_by(
        lambda t: t.person.firstname).order_by(
            lambda t: t.person.name).order_by(
                lambda t: t.tag)


def add_teacher(raw: str):
    """Add a new teacher from a given raw string dump, assuming all
    information being separated by tabs in the following order:
        Tag, Name, FirstName
    Uppercase tags are ignored.
    """
    # split data
    data = raw.split('\t')
    tag, name, firstname = data[0], data[1], data[2]
    tag = tag.lower()

    try:
        # create actual teacher
        db.Teacher(person=db.Person(name=name, firstname=firstname), tag=tag)
    except ValueError as e:
        raise orm.core.ConstraintError(e)


def add_teachers(raw: str):
    """Add teachers from a given raw string dump, assuming all teachers being
    separated by newlines. Each line is handled by add_teacher().
    """
    for data in raw.split('\n'):
        if len(data) > 0:
            add_teacher(data)

# -----------------------------------------------------------------------------


def advance_school_year(last_grade: int, first_grade: int, new_tags: list):
    """Advance all students and classes to the next school year.
    All classes of the last_grade are dropped, so those students remain without
    any class. All remaining classes advance one grade and a new set of classes
    is created for the first_grade using a list of new_tags. Those classes are
    created without a teacher being assigned.
    """
    # drop last grade's classes
    for c in get_classes_by_grade(last_grade):
        c.delete()

    # advance all classes' grades
    for c in get_classes():
        c.grade += 1

    # create new clases for first grade
    for tag in new_tags:
        db.Class(grade=first_grade, tag=tag)
