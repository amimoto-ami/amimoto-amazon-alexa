#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 for amimoto_alexa
"""


import lamvery
from helpers import *
from debugger import *


def collect_impression(intent, session):
    """Collect impression and finalize session
    """
    session_attributes = build_session_attributes(session)
    card_title = "Impression"

    debug_logger(session)
    speech_output = "Thank you! You can see impressions on twitter and ,A MI MO TO Blog." \
                    "Have a nice day! "

# todo: tweet if exist id.
# todo: store session summary to firehose
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
