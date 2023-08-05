# pytest-selenium-pdiff

[![Current Version](https://img.shields.io/pypi/v/pytest-selenium-pdiff.svg)](https://pypi.python.org/pypi/pytest-selenium-pdiff)
[![Build Status](https://img.shields.io/circleci/project/rentlytics/pytest-selenium-pdiff.svg)](https://circleci.com/gh/rentlytics/pytest-selenium-pdiff)

A pytest package implementing perceptualdiff for Selenium tests.

* Free software: MIT license
* Documentation: https://pytest-selenium-pdiff.readthedocs.org.

## Features
* Embeds screenshots in [pytest-html](https://pypi.python.org/pypi/pytest-html) reports
* Supports ImageMagick or perceptualdiff for image comparison.

## Use with pytest-html and pytest-selenium
By default pytest-selenium will embed a screenshot depicting the current browser state.  This will lead to a duplicated screenshot because of this plugin's behavior.  At this time the best way to exclude the pytest-selenium screenshot is to set the environment variable `SELENIUM_EXCLUDE_DEBUG=screenshot`.

## Working With This Repo
### Setup
1. Set up and activate [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) in the repo by
running: `virtualenv venv` and then `source venv/bin/activate`
1. Run `pip install -r requirements_dev.txt`
1. Install PhantomJS with `brew install phantomjs`
1. Run `tox` to run the tests for the repo

### Making a release
For Rentlytics employees, to release new code for the pytest-selenium-pdiff project to pypi, follow these steps:

1. run `bumpversion` to bump the version
1. make sure there is a file in the home directory `~/.pypirc` with the login credentials for PyPi.  For more about
how to upload to PyPi, see [this link](http://peterdowns.com/posts/first-time-with-pypi.html)
1. run `make release` to push the new code to PyPi
