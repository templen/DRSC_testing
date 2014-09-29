DRSC_testing
============

Test tools for the DRSC website.

The ambitious goal of this project is to be a complete functional test
of the DRSC website and its tools.  There are a lot of sections of the
website that we, as developers, don't have occasion to visit.  This
creates the risk that some page will get deleted or replaced with an
old version, or some dependency will break and a previously stable
tool will stop working without our immidiate knowledge.  As a result,
the primary goal of the project is that it be an automated tool that
can be used frequently to test the integrity of the site.  Beyond that
it is intended as a regression test suite to be used for ongoing
development.

To run functional tests for the DRSC website, make sure you have
Python, Selenium and Firefox installed on your machine, then run
DRSC_functional_tests.py.


Development Notes
-----------------
First of all, if you have access to the TRiP_DB testing code
(/groups/flyrnai/ian_devel/TRiP/DB/TRiP_DB_functional_tests.py) make
use of that for examples, because it does a lot of things that this
code doesn't do yet.

DRSC_functional_tests.py is Python (version 2) code that uses Selenium
to drive a (currently Firefox) web browser and test the DRSC website
from the front end.  The reader is assumed to know how to find
websites about any relevant tools and look them up, so we will be lazy
and not introduce them here.  If you're feeling too rushed to read up
on all the tools, start by running the tests to see what happens.

Development of this code is a big task which should have been started
ten years earlier than it was (although the technology we use didn't
exist then).  It is recommended that it be approached in two ways:
Firstly, try to follow current best practices for test driven
development: first write a test for the new feature and make sure it
fails, then write the feature code that makes the test pass.
Likewise, if a bug is found, write a test for it first, then fix it.
Second, try to establish a schedule of revisiting the script and
filling in test coverage on a regular basis.  In other words, don't
try to do the whole thing at one go.
