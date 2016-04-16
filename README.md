### Doc Tests (in Models)

== Introduction ==
Doc tests are tests written into the docstrings of Python modules. They can be either placed alongside the methods for each module or placed together in a tests file in the tests foldet. This particular branch will look at running it for only the models-file docstring placement.

== Setting it up ==
Getting set to write doctests is a bit awkward if it's the only kind of testing being run but it doesn't require much coding. To run the doctests in contacts/models.py, add the following to the test.py file in the app's folder (contacts/test.py in my case):

        import doctest

        from path.to.module import module_to_be_tested

        __test__ = {
            'MyDescription': module_to_be_tested
        }

        def load_tests(loader, tests, ignore):
            tests.addTests(doctest.DocTestSuite())
            return tests


== Benefits ==

* These are very quick to run and they have intuitive sense about them - if it can be done in a Python shell, then it can be done in a doctest
* Requires no extra packages to create these

== Limitations ==

* They don't run on magic methods (see that the tests in __str__ in contacts/models.py are not detected)
* All of the tests in a doctest are counted as one

== Conclusion ==

These can be useful for very small tests and being able to write tests quickly is win over not writing any tess at all.
