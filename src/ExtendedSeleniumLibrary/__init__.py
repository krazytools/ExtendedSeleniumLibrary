from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.base import keyword
from SeleniumLibrary.keywords import WaitingKeywords
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webcolors import *
import re
import time
import os

__version__ = '1.0.0'

class ExtendedSeleniumLib(SeleniumLibrary):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        SeleniumLibrary.__init__(self, 30)
        self.waiting_management = WaitingKeywords(self)


    @keyword
    def clear_textfield_value(self, locator):
        text = self.get_value(locator)
        i = 0
        while i < len(text):
            i += 1
            self.press_key(locator, Keys.BACK_SPACE)
            self.press_key(locator, Keys.DELETE)

    @keyword
    def wait_until_location_is(self, expected, timeout=None, error=None):
        self.waiting_management._wait_until(
          lambda: self.get_location() == expected,
          "Location was not match '%s' in <TIMEOUT>. Actual value was '%s'" % (expected, self.get_location()),
          timeout,
          error
        )

    @keyword
    def wait_until_location_is_not(self, expected, timeout=None, error=None):
        self.waiting_management._wait_until(
            lambda: self.get_location() != expected,
            "Location did not change to value different to '%s' in <TIMEOUT>" % (expected, self.get_location()),
            timeout,
            error
        )

    @keyword
    def wait_until_location_contains(self, expected, timeout=None, error=None):
        self.waiting_management._wait_until(
            lambda: expected in self.get_location(),
            "Location '%s' did not contain '%s' in <TIMEOUT>" % (self.get_location(), expected),
            timeout,
            error
        )

    @keyword
    def location_should_not_be(self, expected):
        actual = self.get_location()
        if expected == actual:
            message = "Location should not be '%s' but it was NOT" % (expected)
            raise AssertionError(message)

    @keyword
    def element_css_property_value_should_be(self, locator, property_name, expected, message=''):
        element = self._element_find(locator, True, True)
        actual = element.value_of_css_property(property_name)
        if expected != actual:
            if not message:
                message = "The css value '%s' of element '%s' should have been '%s' but "\
                          "in fact it was '%s'." % (property_name, locator, expected, actual)
            raise AssertionError(message)

    @keyword
    def element_color_css_property_value_should_be(self, locator, property_name, expected, message=''):
        if self._is_rgb_color(expected):
            expected = self._convert_rgb_to_hex(expected)
        element = self._element_find(locator, True, True)
        actual = element.value_of_css_property(property_name)
        if self._is_rgb_color(actual):
            actual = self._convert_rgb_to_hex(actual)
        if expected != actual:
            if not message:
                message = "The color related css value '%s' of element '%s' should have been '%s' but "\
                          "in fact it was '%s'." % (property_name, locator, expected, actual)
            raise AssertionError(message)

    @keyword
    def wait_until_element_css_property_value_is(self, locator, property_name, expected, timeout=None, error=None):
        self.waiting_management._wait_until(
            lambda: expected == self._element_find(locator, True, True).value_of_css_property(property_name),
            "The css value '%s' of element '%s' did not match '%s' in <TIMEOUT>. Actual value is '%s'"
            % (property_name, locator, expected, self._element_find(locator, True, True).value_of_css_property(property_name)),
            timeout,
            error
        )

    @keyword
    def wait_until_element_css_property_value_is_not(self, locator, property_name, expected, timeout=None, error=None):
        self.waiting_management._wait_until(
            lambda: expected == self._element_find(locator, True, True).value_of_css_property(property_name),
            "The css value '%s' of element '%s' did not different to '%s' in <TIMEOUT>"
            % (property_name, locator, expected),
            timeout,
            error
        )

    @keyword
    def wait_until_element_color_css_property_value_is(self, locator, property_name, expected, timeout=None,
                                                       error=None):
        if self._is_rgb_color(expected):
            expected = self._convert_rgb_to_hex(expected)

        def check_css_property_value():
            element = self._element_find(locator, True, True)
            actual = element.value_of_css_property(property_name)
            if self._is_rgb_color(actual):
                actual = self._convert_rgb_to_hex(actual)
            return actual == expected

        self.waiting_management._wait_until(
            lambda: check_css_property_value,
            "The color related css value '%s' of element '%s' did not match '%s' in <TIMEOUT>"
            % (property_name, locator, expected),
            timeout,
            error
        )

    @keyword
    def wait_until_element_color_css_property_value_is_not(
            self, locator, property_name, expected, timeout=None, error=None):
        if self._is_rgb_color(expected):
            expected = self._convert_rgb_to_hex(expected)

        def check_css_property_value():
            element = self._element_find(locator, True, True)
            actual = element.value_of_css_property(property_name)
            if self._is_rgb_color(actual):
                actual = self._convert_rgb_to_hex(actual)
            return actual == expected

        self.waiting_management._wait_until(
            lambda: check_css_property_value,
            "The color related css value '%s' of element '%s' did not different to '%s' in <TIMEOUT>"
            % (property_name, locator, expected),
            timeout,
            error
        )

    @keyword
    def is_element_present(self, locator, tag=None):
        return self._is_element_present(locator, tag)

    @keyword
    def scroll_to_element(self, locator):
        self.driver.execute_script("arguments[0].scrollIntoView();", self.find_element(locator))

    def _scroll_to_left_of_webElement(self, element):
        self.driver.execute_script("arguments[0].scrollTo(0,0);", element)

    def _convert_rgb_to_hex(self, rgb_string):
        color_tuple = rgb_string.replace("rgb(", "").replace("rgba(", "").replace(")", "").replace(" ", "")
        color_tuple = color_tuple.split(",")
        rgb = (int(color_tuple[0]), int(color_tuple[1]), int(color_tuple[2]))
        hex_str = rgb_to_hex(rgb)
        return hex_str

    def _is_rgb_color(self, color_str):
        r = r"rgb\((\d+),\s*(\d+),\s*(\d+)\)"
        r2 = r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)"
        return re.match(r, color_str) or re.match(r2, color_str)

    @keyword
    def switch_to_frame(self, locator):
        self.wait_for_data_loaded()
        frame = self.find_element(locator)
        self.driver.switch_to_frame(frame)

