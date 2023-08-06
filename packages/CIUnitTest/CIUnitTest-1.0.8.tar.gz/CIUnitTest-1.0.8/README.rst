CI Unit Test
============

CI Unit Test is a library which enables to retrieve the results of unit tests in JSON format. This may be used in custom Continuous Integration systems which need to process the results of unit tests.

The results can be saved as is to a NoSQL database, or can be returned as a Python object in order to be combined with other information before being saved.

Usage
-----

The results in JSON format can be obtained by using `JsonTestRunner`:

.. code:: python

    suite = unittest.TestLoader().loadTestsFromTestCase(TestsDemo)
    json = ciunittest.JsonTestRunner().run(suite, formatted=True)
    print(json)

Since the first line uses unittest, all unittest features are available, such as the auto-discovery of unit tests in a project directory:

.. code:: python

    suite = unittest.TestLoader().discover(targetPath)

To obtain the results as a Python object, use `ObjectTestRunner`:

.. code:: python

    suite = unittest.TestLoader().loadTestsFromTestCase(TestsDemo)
    result = ciunittest.ObjectTestRunner().run(suite)
    print('Done %d tests in %d ms.' %
          (len(result['results']), result['spentMilliseconds']))

To perform an action at the beginning of every test (independently of the runner being used,) do:

.. code:: python

    suite = unittest.TestLoader().loadTestsFromTestCase(TestsDemo)
    runner = ciunittest.JsonTestRunner()
    runner.on_start = lambda test: print(".", end="", flush=True)
    result = runner.run(suite)
    ...

In the previous code sample, every time the runner is ready to start a new test, a dot is displayed in the terminal.

Similarly, one can execute arbitrary code at the end of every test. The test result, that is `ciunittest.Success`, `ciunittest.Error` or `ciunittest.Failure`, will be passed as a second parameter to the function.

.. code:: python

    runner.on_end = lambda test, result: print(result, flush=True)

The code is inspired by http://pythonhosted.org/gchecky/unittest-pysrc.html

If you have any question or remark, please contact me at arseni.mourzenko@pelicandd.com. Critics are also welcome, since I have used Python for only a few days, and probably get lots of things wrong.
