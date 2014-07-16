
import unittest

testmodules = [
    'tests.test_views',
    'tests.test_models',
    'tests.test_auth',
    'tests.test_API',
    ]

suite = unittest.TestSuite()

for t in testmodules:
    try:
        # Currently none of my test_modules define a suite, but for later:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(t, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        # else, just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner().run(suite)