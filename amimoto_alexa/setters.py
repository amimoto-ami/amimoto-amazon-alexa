#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 for amimoto_alexa
"""


def set_visitor_name_from_session(intent, session):
    """ Sets the visitor name in the session and prepares the speech to reply to the
    user.
    """

    card_title = 'MyNameIs'
    session_attributes = build_session_attributes(session)
    should_end_session = False

    if 'VisitorName' in session_attributes.keys():
      visitor_name = session_attributes['VisitorName']
    else:
      visitor_name = intent['slots']['VisitorName']['value'].lower()
      session_attributes['VisitorName'] = visitor_name

    debug_logger(session_attributes)
    attendees = load_attendees()
    if visitor_name in attendees.keys():
        session_attributes['twitter_id'] = attendees[visitor_name]
    else:
        session_attributes['twitter_id'] = None

    speech_output = "Hi, " + \
            visitor_name + ". " \
            + gen_twitter_sentence(session_attributes['twitter_id']) + \
            "Please ask to me by saying, What is WordPress?, or Can I use free trial?"
    reprompt_text = "I know that, you are " + \
            visitor_name + ". " \
            + gen_twitter_sentence(session_attributes['twitter_id']) + \
            "Please ask to me by saying, What is WordPress?, or Can I use free trial?"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

