#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 for amimoto_alexa
"""


from helpers import *
from debugger import *


def set_visitor_name_from_session(intent, session):
    """ Sets the visitor name in the session and prepares the speech to reply to the
    user.
    """

    session_attributes = build_session_attributes(session)
    should_end_session = False

    if session_attributes['state'] in ['finalizing']:
        speech_output = '<p>One more time please.</p><p>Please tell us your thoughts by saying, <break time="0.3s"/> I feel "I love WordPress!"</p>'
        card_title = "AMIMOTO Ninja unreconized...."
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, speech_output, should_end_session))

    if 'VisitorName' in session_attributes.keys():
        if session_attributes['VisitorName']:
            visitor_name = session_attributes['VisitorName']
        else:
            visitor_name = ""

    else:
        visitor_name = intent['slots']['VisitorName']['value'].lower()
        session_attributes['VisitorName'] = visitor_name

    card_title = 'Hello ' + visitor_name + '! ' + "Let's ask to AMIMOTO Ninja !!"

    debug_logger(session_attributes)
    attendees = load_attendees()
    if visitor_name in attendees.keys():
        session_attributes['twitter_id'] = attendees[visitor_name]
    else:
        session_attributes['twitter_id'] = None

    speech_output = "<p>Hi, " \
        + visitor_name + ".</p>" \
        + gen_twitter_sentence(session_attributes['twitter_id']) \
        + '<p>Please ask to me by saying, <break time="0.2s"/> What is WordPress?, or Can I use free trial?</p>'
    reprompt_text = '<p>Please ask to me by saying, <break time="0.2s"/> What is WordPress?, or Can I use free trial?</p>'
    session_attributes['state'] = ['got_name']
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
