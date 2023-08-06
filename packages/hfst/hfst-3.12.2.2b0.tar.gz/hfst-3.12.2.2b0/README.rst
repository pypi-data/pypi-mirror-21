
*******************
Package description
*******************

Package ``hfst`` contains python bindings for `HFST <https://hfst.github.io>`_
(Helsinki Finite-State Technology) C++ library. HFST toolkit is intended for
processing natural language morphologies. The toolkit is demonstrated by
wide-coverage implementations of a number of languages of varying
morphological complexity.

Requirements
############

The bindings have been tested with python 3. Wheels are offered for python
versions 3.4, 3.5 and 3.6 for Windows and Mac OS X. The OS X support is experimental.
For Linux users, we recommend using the `Debian packages
<https://kitwiki.csc.fi/twiki/bin/view/KitWiki/HfstPython#Option_1_Installing_the_debian_p>`_.

We currently offer only 64-bit wheels for Windows. They also require a 64-bit
python to work correctly. Wheels for Mac are compiled as universal binaries
that work on both 32- and 64-bit environments. OS X must be 10.7 or higher.

Compiling from source requires at least swig (tested with versions 2.0.4 and
3.0.5), a C++ compiler (tested with gcc 4.6.3, clang and Visual C++ 10.0
for python 3.4 and 14.0 for python >= 3.5), and python3 with setuptools
(tested with version 28.8.0). All these must be located on directories listed
on system PATH. On Linux and Mac OS X, readline and getline libraries must be
available and the C++ compiler must support flag 'std=c++11'.

A known issue on OS X is that compiling C code fails as flag 'std=c++11' must
be set globally in setup.py but is not accepted when the source is pure C.
To circumvent this, code written in C (the foma back-end) is disabled on Mac
if bindings are created from source.

Installation
############

We recommend using ``pip`` tool for installation. For python version 3, it is
usually named ``pip3`` (plain ``pip`` being used for python version 2).
Starting from python 3.4, pip is included by default and can be called with
``python3 -m pip``.

Basic installation with ``pip3`` on command line:

``pip3 install [--upgrade] hfst``

or, starting from python version 3.4, directly via python:

``python3 -m pip install [--upgrade] hfst``

The commands above are run in a shell/terminal/command prompt, but they can
also be run on python command line or via a graphical user interface 
(e.g. IDLE) with pip.main that takes arguments in a list:

| ``import pip``
| ``pip.main(['install','--upgrade','hfst'])``


Alternative `installation instructions <https://kitwiki.csc.fi/twiki/bin/view/KitWiki/HfstPython>`_
are given on our KitWiki pages.

Documentation
#############

See Doxygen-generated `package documentation <https://hfst.github.io/python>`_
on our Github pages. In python, you can also use ``dir`` and ``help``
commands, e.g.:

``dir(hfst)``

``help(hfst.HfstTransducer)``

License
#######

HFST is licensed under Gnu GPL version 3.0.

Troubleshooting
###############

*Pip starts to compile from source although there is a wheel available:*

Try upgrading pip with ``pip3 install --upgrade pip`` or 
``python3 -m pip install --upgrade pip``. Another reason for this can be that
the source package on PyPI is newer (i.e. has a higher version number) than
the corresponding wheel for the given environment. Report this via our
`issue tracker <https://github.com/hfst/hfst/issues/>`_ so a fresh wheel
will be created.

It is a known issue that pip does not always accept the wheels for OS X
but starts to compile the bindings from scratch. We are working on this issue.

*Error message "command ... failed with error code ...":*

Try rerunning pip in verbose mode with
``pip3 install --verbose [--upgrade] hfst`` to get more information.

*Error message "error: could not delete ... : permission denied":*

You do not have sufficient rights to install packages. On Mac and Linux, try
installing as super user with ``sudo pip3 install [--upgrade] hfst``.
On Windows, reopen Command Prompt/Python command line/IDLE by right-clicking
and choose "Run as administrator", then run pip again.

*Using flag -std=c++11 causes an error in the C++/C compiler:*

This is a known issue on OS X when compiling from source. The flag must be
set globally in setup.py but is not accepted when the source is pure C, as
some of our back-end files are. If there isn't a wheel available for your
environment, see alternative 
`installation instructions <https://kitwiki.csc.fi/twiki/bin/view/KitWiki/HfstPython>`_.

Links
#####

`HFST project main page <https://hfst.github.io>`_: more information about
the project

`Github issue tracker <https://github.com/hfst/hfst/issues/>`_: for comments,
feature requests and bug reports

