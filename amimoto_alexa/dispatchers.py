#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 for amimoto_alexa
"""


from helpers import *
from debugger import *
import yaml
import random


def dispatch_question(intent, session):
    """Dispatch questions and return answer.
    """
    session_attributes = build_session_attributes(session)
    should_end_session = False

    debug_logger(session_attributes)

    if session_attributes['state'] in ['started']:
        speech_output = 'Please tell me your name first, by saying, i am John Smith'
        card_title = "Please tell me your name first."
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, speech_output, should_end_session))
    elif session_attributes['state'] in ['finalizing']:
        speech_output = 'One more time please. Please tell us your thoughts by saying, I feel "I love WordPress!"'
        card_title = "AMIMOTO Ninja can't reconized..."
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, speech_output, should_end_session))

    session_attributes['state'] = 'on_question'

    if intent['name'] == 'WhatIsIntent':
        card_title = "WhatIs"
        pre_text = "What is "
    elif intent['name'] == 'CanIUseIntent':
        card_title = "CanIUse"
        pre_text = "Can I use "
    else:
        card_title = "Null"

    text_data = load_text_from_yaml(card_title)
    aliases = yaml.load(open('data/aliases.yml').read())
    rev_aliases = {}
    for x in aliases.items():
        if x[1]:
            for y in x[1]:
                rev_aliases[y] = x[0]

    # debug_logger(text_data)
    question = str(intent['slots']['AskedQuestion']['value']).lower()
    # todo: stock question to session_attributes
    if question in text_data.keys():
        card_title = "About " + question
        session_attributes['accepted_questions'].append(':'.join([intent['name'], question]))
        speech_output = '<break time="0.5s"/>' + ssmlnize_sentence(text_data[question]) + '<break time="2s"/> Do you have any other questions?'
    elif question in rev_aliases.keys():
        question = rev_aliases[question]
        card_title = "About " + question
        session_attributes['accepted_questions'].append(':'.join([intent['name'], question]))
        speech_output = '<break time="0.5s"/>' + ssmlnize_sentence(text_data[question]) + '<break time="2s"/> Do you have any other questions?'
    else:
        card_title = "AMIMOTO Ninja can't reconized..."
        session_attributes['rejected_questions'].append(':'.join([intent['name'], question]))
        speech_output = "<p>Hmm... I couldn't recognize, you said '{0}'.</p>".format(question)

        if len(session_attributes['rejected_questions']) % 2 == 0:
            question = random.choice(text_data.keys())
            card_title = "AMIMOTO Ninja can't reconized... But introduce " + question
            speech_output = speech_output \
                + '<p><break time="0.5s"/>I might as well introduce, {0}{1}?.</p>'.format(pre_text, question) \
                + '<break time="0.5s"/>' \
                + ssmlnize_sentence(text_data[question]) \
                + '<break time="2s"/><p>Do you have any other questions?</p>'
        else:
            speech_output = speech_output \
                + '<p>So, please ask to me by saying, <break time="0.2s"/> What is WordPress?, or Can I use free trial?</p>'

    reprompt_text = '<p>Do you have any other questions?</p>'
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def dispatch_yes_intent(intent, session):
    """Dispatch yes intent and return message
    """

    session_attributes = build_session_attributes(session)
    should_end_session = False
#    text_data = load_text_from_yaml(card_title)
    debug_logger(session)

    if session_attributes['state'] in ['on_question', 'got_name']:
        card_title = "Please ask to AMIMOTO Ninja."
        speech_output = '<p>OK. Please ask to me by saying, <break time="0.2s"/> What is WordPress?, or Can I use free trial?</p>'
        reprompt_text = '<p>Please ask to me by saying, <break time="0.2s"/> What is WordPress?, or Can I use free trial?</p>'
    elif session_attributes['state'] in ['finalizing']:
        card_title = "Please ask to AMIMOTO Ninja."
        speech_output = '<p>One more time please.</p> <p>Please tell us your thoughts by saying, <break time="0.3s"/> I feel "I love WordPress!"</p>'
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, speech_output, should_end_session))
    else:
        card_title = "AMIMOTO Ninja can't reconized..."
        speech_output = '<p>Sorry, what did you say?</p>'
        reprompt_text = None

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def dispatch_no_intent(intent, session):
    """Dispatch no intent and tweet. Then end session.
    """

    card_title = "No"
    session_attributes = build_session_attributes(session)
#    text_data = load_text_from_yaml(card_title)
    debug_logger(session)

    if session_attributes['state'] in ['on_question']:
        card_title = "Please tell your thoughts"
        session_attributes['state'] = 'finalizing'
        speech_output = '<p>Thank you {0} for trying <phoneme alphabet="ipa" ph="amimoʊtoʊ">amimoto</phoneme> Ninja.</p> '.format(session_attributes['VisitorName']) \
                        + '<p>Please tell us your thoughts by saying, <break time="0.3s"/> I feel "I love WordPress!"</p>'
        should_end_session = False
    elif session_attributes['state'] in ['got_name']:
        card_title = "Thank you for trying AMIMOTO Ninja !!"
        session_attributes['state'] = 'finalizing'
        speech_output = '<p>Thank you {0} for trying <phoneme alphabet="ipa" ph="amimoʊtoʊ">amimoto</phoneme> Ninja.</p>'.format(session_attributes['VisitorName']) \
                        + "Have a nice day! "
        should_end_session = True
    elif session_attributes['state'] in ['finalizing']:
        card_title = "AMIMOTO Ninja can't reconized..."
        should_end_session = False
        speech_output = '<p>One more time please.</p> <p>Please tell us your thoughts by saying, <break time="0.3s"/> I feel "I love WordPress!"</p>'
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, speech_output, should_end_session))
    else:
        card_title = "Thank you for trying AMIMOTO Ninja !!"
        session_attributes['state'] = 'finalizing'
        speech_output = '<p>Thank you for trying <phoneme alphabet="ipa" ph="amimoʊtoʊ">amimoto</phoneme> Ninja.</p>' \
                        "Have a nice day! "
        should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
