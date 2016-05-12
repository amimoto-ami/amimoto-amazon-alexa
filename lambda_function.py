#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
from __future__ import unicode_literals
import yaml
import json
import lamvery

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    print(lamvery.secret.get('test'))
    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId'] +
          ", sessionId=" + session['sessionId'])

def build_session_attributes(session):
    """ initialize session_attributes when passed None """
    if session['attributes']:
        session_attributes = session['attributes']
    else:
        session_attributes = {}
        session_attributes['state'] = 'started'
        session_attributes['flags'] = {
                'name' : False,
                'has_twitter' : False
                }
    return session_attributes


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response(launch_request, session)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # for Development
    print(str(intent_request))
    print(str(session))

    # Dispatch to your skill's intent handlers
    if intent_name == "MyNameIsIntent":
        return set_visitor_name_from_session(intent, session)
    elif intent_name == "WhatIsIntent" or intent_name == "CanIUseIntent":
        return dispatch_question(intent, session)
    elif intent_name == "AMAZON.YesIntent":
        return dispatch_yes_intent(intent, session)
    elif intent_name == "AMAZON.NoIntent":
        return dispatch_no_intent(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response(intent, session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Debug for Development ------------------
def debug_logger(*args):
    """ outputs args to log
    """

    for x in args:
        print(repr(x))

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response(intent, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    debug_logger(intent,session)

    session_attributes = build_session_attributes(session)

    card_title = "Welcome"
    text_data = load_text_from_yaml(card_title)
    print(str(text_data))
    speech_output = text_data['speech']

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = text_data['reprompt']
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the, A MI MO TO Ninja. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def dispatch_question(intent, session):
    """Dispatch questions and return answer.
    """
    session_attributes = build_session_attributes(session)
    if session_attributes['state'] in ['started']:
        session_attributes['state'] = 'on_question'

    if intent['name'] == 'WhatIsIntent':
        card_title = "WhatIs"
    elif intent['name'] == 'CanIUseIntent':
        card_title = "CanIUse"
    else:
        card_title = "Null"

    text_data = load_text_from_yaml(card_title)
    debug_logger(text_data)
    question = intent['slots']['AskedQuestion']['value']
    if question in text_data.keys():
        speech_output = text_data[question] + '. Do you have any other questions?'
    else:
        speech_output = "Pardon?"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def dispatch_yes_intent(intent, session):
    """Dispatch yes intent and return message
    """

    card_title = "Yes"
    session_attributes = build_session_attributes(session)
#    text_data = load_text_from_yaml(card_title)
    debug_logger(session)

    if session_attributes['state'] in ['on_question']:
        speech_output = "Next questions"
    else:
        speech_output = 'Pardon?'

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

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

    speech_output = "Hi, " + \
            visitor_name + ". " \
            "Please ask to me by saying, What is WordPress?, or Can I use free trial?"
    reprompt_text = "I know that, you are " + \
            visitor_name + ". " \
            "Please ask to me by saying, What is WordPress?, or Can I use free trial?"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def set_visitor_full_name_from_session(intent, session):
    """ Sets the visitor name in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = session['attributes']
    should_end_session = False

    visitor_first_name = intent['slots']['VisitorFirstName']['value']
    visitor_last_name = intent['slots']['VisitorLastName']['value']
    session_attributes['VisitorName'] = visitor_first_name.lower() + ' ' + visitor_last_name.lower()
    speech_output = "Hi, " + \
            visitor_name + ". "
    reprompt_text = "I know that, you are " + \
            visitor_name + ". "
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def load_text_from_yaml(title):
    return yaml.load(open('data/text/{card}.yml'.format(card=title)).read())

