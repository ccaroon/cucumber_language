# Komodo Cucumber language service.

import logging
from koUDLLanguageBase import KoUDLLanguage


log = logging.getLogger("koCucumberLanguage")
#log.setLevel(logging.DEBUG)


def registerLanguage(registry):
    log.debug("Registering language Cucumber")
    registry.registerLanguage(KoCucumberLanguage())


class KoCucumberLanguage(KoUDLLanguage):
    name = "Cucumber"
    lexresLangName = "Cucumber"
    _reg_desc_ = "%s Language" % name
    _reg_contractid_ = "@activestate.com/koLanguage?language=%s;1" % name
    _reg_categories_ = [("komodo-language", name)]
    _reg_clsid_ = "97929147-d5df-4267-bb6d-37e35f61e604"
    defaultExtension = '.feature'

    lang_from_udl_family = {'SSL': 'Cucumber'}

    sample = """
# This is a comment

Feature: Sample Feature

    Some text describing this awesome feature.

Background:
    Given some shared setup
    
@scenario1
Scenario: Sample Scenario
    Given some initial "<input>"
    And some more setup that include this "hello world"
    But not that kind of setup
    When I poke and peek and prod 10 times
    Then I should see something amazing happen

    Examples:
        | input   | output  |
        | garbage | garbage |
        | foo     | bar     |

@scenario2 @keyword_less
Scenario: All Star Scenario
    * some initial "<input>"
    * some more setup that include this "hello world"
    * not that kind of setup
    * I poke and peek and prod 2.5 times
    * I should see something amazing happen
"""
