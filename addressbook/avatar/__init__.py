"""
This is a modified version of django-avatar.

This is just a copy of the django-avatar app from https://github.com/grantmcconnaughey/django-avatar
but modified to work when avatars are linked to contacts, not a user model at all and I'm loathe
to shoehorn the Contact model into a User model definition just for the sake of getting the app to
work so I'm overwriting it on the whole.
"""
__version__ = '2.2.1'
