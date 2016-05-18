#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AMIMOTO Alexa
"""

from __future__ import print_function
from __future__ import unicode_literals
import yaml
import json
import lamvery

# amimoto_alexa
from amimoto_alexa.helpers import *
from amimoto_alexa.debugger import *
from amimoto_alexa.dispatchers import *
from amimoto_alexa.setters import *
from amimoto_alexa.collect_message import *


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

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
    elif intent_name == "ImpressionIntent":
        return collect_impression(intent, session)
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


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response(intent, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    debug_logger(intent, session)

    session_attributes = build_session_attributes(session)
    if session['new']:
        put_event_to_firehorse(intent, session)

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
