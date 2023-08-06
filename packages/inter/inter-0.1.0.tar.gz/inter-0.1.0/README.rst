inter
=====

Toolset for interactive command-line applications

``inter`` is a utility for providing an interactive command line interface.
You can use it to ask question and coerce values into ints, floats, boolean values,
and you have a number of options like specifying integer and floating point constraints,
setting the color of the question text, and specifying default values.

Installation
------------

inter is installable through pip. To install to your system, just run::

    $ sudo pip install inter

or to install from source, run::

    $ python setup.py install

Usage
-----

inter is easy to use in your python scripts. Check the following example::

    from inter import Interact

    cli = Interact()

    # Takes a string from the user and strips the whitespace, and lowercase it.
    first_name = cli.ask_str('enter your first name', strip=True, lower=True)

    # title=True will take input like "hey there" and return "Hey There"
    full_name = cli.ask_str('enter your full name', strip=True, title=True)

    # Prints "whats your age: " and gives an error message regarding min and max
    # if the user fails to enter a value within that range.
    age = cli.ask_int('whats your age', min=1, max=120)

    # Prints "are you in the US [yn]: "
    in_the_us = cli.ask_bool('are you in the US')

    # Prints "are you a developer [Yn]: "
    # If user provides no input, default True is returned. Otherwise it checks for
    # "yes", "y", "true", or "no", "n", "false" and if it receives none of those,
    # it will print an error message in red.
    developer = cli.ask_bool('are you a developer', default=True)


Release Notes
-------------

:0.1.0:
    Alpha release with usable int/float/bool/str tooling.
:0.0.1:
    Project created
