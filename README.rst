Introduction
------------

Scribbler is a parallel test runner.

What does it run?
-----------------

Scribbler will pick up any tests where:

* The test method is inside a class
* The test method's name starts with "test_"

It'll also pick setup methods (methods run before every test) where:

* The setup method is inside a class
* The setup method's name is either "setUp", "setup" or "set_up"

It'll pick teardown methods as well (methods run after every test) where:

* The teardown method is inside a class
* The teardown method's name is either "tearDown", "teardown" or "tear_down"

Will I get any results
----------------------

It's hard for me to spoil the surprise of running, but if you run::

    scribbler_console

Scribbler will try to run all the tests in the current directory (and sub-directories) with the default settings.

For more info on the options run the help with::

    scribbler_console -h

Why Scribbler?
--------------

Ernest Scribbler is the inventor of the Funniest Joke in the World (Monthy Python's sketch).

We love the sketch, hence the name.
