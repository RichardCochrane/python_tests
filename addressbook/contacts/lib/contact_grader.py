class Grader(object):
    """This will grade the given contact in terms of overall power."""

    def __init__(self, contact):
        self.contact = contact

    def grade(self):
        return len(self.contact.powers)
