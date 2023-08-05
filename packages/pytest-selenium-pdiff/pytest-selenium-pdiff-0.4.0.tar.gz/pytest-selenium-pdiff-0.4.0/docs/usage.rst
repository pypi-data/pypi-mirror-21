=====
Usage
=====

To use pytest-selenium-pdiff in a project::

    import pytest-selenium-pdiff

    def test_example(self, driver):
        do_something()
        screenshot_matches(driver, 'module/my screen shot')


Optionally images can be cropped once to a subsection of the original image::

    import pytest-selenium-pdiff

    def test_example(self, driver):
        do_something()
        screenshot_matches(driver, 'module/my screen shot', crop=(0,0,200,200))


Optionally images can be masked with magenta rectangles to hide areas that are unimportant to the screen shot::

    import pytest-selenium-pdiff

    def test_example(self, driver):
        do_something()
        screenshot_matches(driver, 'module/my screen shot', masks=[(10,20,30,40)]

The crop and mask functionality can be used at the same time. Masks are applied after the images is cropped::

    import pytest-selenium-pdiff

    def test_example(self, driver):
        do_something()
        screenshot_matches(driver, 'module/my screen shot', crop=(0,0,200,200), masks=[(10,20,30,40),(20,30,50,70)]

The crop and mask coordinates should be in the following format::

 (left, upper, right, lower)

