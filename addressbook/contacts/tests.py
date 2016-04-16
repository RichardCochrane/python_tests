import doctest

from contacts.models import Contact


__test__ = {
    'Contact': Contact
}


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite())
    return tests
