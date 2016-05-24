#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 for amimoto_alexa
"""


from helpers import *
from debugger import *


def dispatch_question(intent, session):
    """Dispatch questions and return answer.
    """
    session_attributes = build_session_attributes(session)
    if session_attributes['state'] in ['started', 'got_name']:
        session_attributes['state'] = 'on_question'

    if intent['name'] == 'WhatIsIntent':
        card_title = "WhatIs"
    elif intent['name'] == 'CanIUseIntent':
        card_title = "CanIUse"
    else:
        card_title = "Null"

    text_data = load_text_from_yaml(card_title)
    debug_logger(text_data)
    question = intent['slots']['AskedQuestion']['value'].lower()
    # todo: stock question to session_attributes
    if question in text_data.keys():
        session_attributes['accepted_questions'].append(':'.join([intent['name'], question]))
        speech_output = text_data[question] + '. Do you have any other questions?'
    else:
        session_attributes['rejected_questions'].append(':'.join([intent['name'], question]))
        speech_output = "Pardon? please check list of questions." \
            'So, please ask to me by saying, What is WordPress?, or Can I use free trial?'

    reprompt_text = 'Do you have any other questions?'
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def dispatch_yes_intent(intent, session):
    """Dispatch yes intent and return message
    """

    card_title = "Yes"
    session_attributes = build_session_attributes(session)
#    text_data = load_text_from_yaml(card_title)
    debug_logger(session)

    if session_attributes['state'] in ['on_question']:
        speech_output = 'OK. Please ask to me by saying, What is WordPress?, or Can I use free trial?'
    else:
        speech_output = 'Pardon?' \
            'Please ask to me by saying, What is WordPress?, or Can I use free trial?'

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def dispatch_no_intent(intent, session):
    """Dispatch no intent and tweet. Then end session.
    """

    card_title = "No"
    session_attributes = build_session_attributes(session)
#    text_data = load_text_from_yaml(card_title)
    debug_logger(session)

    if session_attributes['state'] in ['on_question']:
        session_attributes['state'] = 'finalizing'
        speech_output = 'Thank you for trying the, A MI MO TO Ninja. ' \
                        'Please tell us your thoughts by saying, my impression is, "I love WordPress!"'
        should_end_session = False
    else:
        speech_output = "Thank you for trying the, A MI MO TO Ninja. " \
                        "Have a nice day! "
        should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
