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

    lang_from_udl_family = {
        'TPL': 'Cucumber'
    }

    sample = """
# This is a comment

Feature: Sample Feature

Background:
    Given some shared setup
    
@scenario1
Scenario: Sample Scenario
    Given some initial setup
    And some more setup
    But not that kind of setup
    When I poke and peek and prod
    Then I should see something amazing happen

    Examples:
        | input   | output  |
        | garbage | garbage |
        | foo     | bar     |

@scenario2
Scenario: All Star Scenario
    * some initial setup
    * not that kind of setup
    * I poke and peek and prod
    * I should see something amazing happen
"""
