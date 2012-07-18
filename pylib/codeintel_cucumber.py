#!/usr/bin/env python
################################################################################
# Cucumber support for codeintel.
################################################################################
import os
import sys
import logging

from codeintel2.common import *
from codeintel2.citadel import CitadelBuffer
from codeintel2.langintel import LangIntel
from codeintel2.udl import UDLBuffer, UDLCILEDriver, UDLLexer
from codeintel2.util import CompareNPunctLast

from SilverCity.ScintillaConstants import (
    SCE_UDL_SSL_DEFAULT, SCE_UDL_SSL_IDENTIFIER,
    SCE_UDL_SSL_OPERATOR, SCE_UDL_SSL_VARIABLE, SCE_UDL_SSL_WORD,
)

try:
    from xpcom.server import UnwrapObject
    _xpcom_ = True
except ImportError:
    _xpcom_ = False
################################################################################
lang = "Cucumber"
log = logging.getLogger("codeintel.cucumber")
#log.setLevel(logging.DEBUG)

# These keywords are copied from "cucumber-mainlex.udl"
# ** Be sure to keep both of them in sync. **
keywords = [
    'Feature:', 'Background:', 'Scenario:', 'Scenario Outline:', 'Given', 'When',
    'Then', 'And', 'But', 'Examples:', '*'
]
################################################################################
class CucumberLexer(UDLLexer):
        lang = lang
################################################################################
class CucumberLangIntel(LangIntel):
    lang = lang
    
    ############################################################################
    # IMPLICIT codeintel triggering event, i.e. when typing in the editor.
    #
    # @param buf {components.interfaces.koICodeIntelBuffer}
    # @param pos {int} The cursor position in the editor/text.
    # @param implicit {bool} Automatically called, else manually called?
    ############################################################################
    def trg_from_pos(self, buf, pos, implicit=True, DEBUG=False, ac=None):
        if pos < 1:
            return None

        accessor = buf.accessor
        last_pos = pos-1
        char = accessor.char_at_pos(last_pos)
        style = accessor.style_at_pos(last_pos)
        if char == '@':
            return Trigger(self.lang, TRG_FORM_CPLN, "tags", pos, implicit)
        elif char == '<':
            return Trigger(self.lang, TRG_FORM_CPLN, "placeholders", pos-1, implicit)
        elif char.isupper():
            prefix = char
            for word in keywords:
                if word.startswith(prefix):
                    return Trigger(self.lang, TRG_FORM_CPLN, "keywords",
                                   pos-1, implicit, kw_prefix=prefix)

        return None
    ############################################################################
    # EXPLICIT triggering event, i.e. Ctrl+J.
    #
    # @param buf {components.interfaces.koICodeIntelBuffer}
    # @param pos {int} The cursor position in the editor/text.
    # @param implicit {bool} Automatically called, else manually called?
    ############################################################################
    def preceding_trg_from_pos(self, buf, pos, curr_pos,
                               preceding_trg_terminators=None, DEBUG=False):
        if pos < 1:
            return None

        accessor = buf.accessor
        last_pos = pos-1
        char = accessor.char_at_pos(last_pos)
        style = accessor.style_at_pos(last_pos)
        if char == '@':
            return Trigger(self.lang, TRG_FORM_CPLN, "tags", pos, implicit=False)
        elif char == '<':
            return Trigger(self.lang, TRG_FORM_CPLN, "placeholders",
                           pos-1, implicit=False)
        elif char.isupper():
            prefix = char
            for word in keywords:
                if word.startswith(prefix):
                    return Trigger(self.lang, TRG_FORM_CPLN, "keywords",
                                   pos-1, implicit=False, kw_prefix=prefix)

        return None
    ############################################################################
    # Provide the list of completions or the calltip string.
    # Completions are a list of tuple (type, name) items.
    #
    # Note: This example is *not* asynchronous.
    ############################################################################
    def async_eval_at_trg(self, buf, trg, ctlr):
        if _xpcom_:
            trg = UnwrapObject(trg)
            ctlr = UnwrapObject(ctlr)
        pos = trg.pos
        ctlr.start(buf, trg)

        if trg.id == (self.lang, TRG_FORM_CPLN, "placeholders"):
            ctlr.set_cplns(self._get_all_placeholders_in_buffer(buf))
            ctlr.done("success")
            return
        
        if trg.id == (self.lang, TRG_FORM_CPLN, "tags"):
            ctlr.set_cplns(self._get_all_tags_in_buffer(buf))
            ctlr.done("success")
            return

        if trg.id == (self.lang, TRG_FORM_CPLN, "keywords"):
            kw_prefix = trg.extra.get("kw_prefix")
            cplns = [x for x in keywords if x.startswith(kw_prefix)]
            cplns = [("keyword", x) for x in sorted(cplns, cmp=CompareNPunctLast)]
            ctlr.set_cplns(cplns)
            ctlr.done("success")
            return

        ctlr.error("Unknown trigger type: %r" % (trg, ))
        ctlr.done("error")
    ############################################################################
    def _get_all_placeholders_in_buffer(self, buf):
        all_placeholders = set()
        for token in buf.accessor.gen_tokens():
            if token.get('text')[0] == '<':
                all_placeholders.add(token.get('text'))
        return [("variable", x) for x in sorted(all_placeholders, cmp=CompareNPunctLast)]
    ############################################################################
    def _get_all_tags_in_buffer(self, buf):
        all_tags = set()
        for token in buf.accessor.gen_tokens():
            if token.get('text')[0] == '@':
                all_tags.add(token.get('text')[1:])
        return [("identifier", x) for x in sorted(all_tags, cmp=CompareNPunctLast)]
################################################################################
class CucumberBuffer(UDLBuffer):
    lang = lang
    ssl_lang = "Cucumber"

    cb_show_if_empty = True

    # Close the completion dialog when encountering any of these chars.
    cpln_stop_chars = " ()*-=+<>{}[]^&|;:'\",.?~`!@#%\\/"
################################################################################
class CucumberCILEDriver(UDLCILEDriver):
    lang = lang

    def scan_purelang(self, buf):
        import cile_cucumber
        return cile_cucumber.scan_buf(buf)
################################################################################
def register(mgr):
    """Register language support with the Manager."""
    mgr.set_lang_info(
        lang,
        silvercity_lexer=CucumberLexer(),
        buf_class=CucumberBuffer,
        langintel_class=CucumberLangIntel,
        import_handler_class=None,
        cile_driver_class=CucumberCILEDriver,
        # Dev Note: set to false if this language does not support
        # autocomplete/calltips.
        is_cpln_lang=True)
