#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
helpers for amimoto_alexa
"""

import yaml
import json
import boto3, datetime, time
import lamvery
from debugger import *


def build_session_attributes(session):
    """ initialize session_attributes when passed None """
    if 'attributes' in session.keys():
        if session['attributes']:
            session_attributes = session['attributes']
        else:
            session_attributes = {}
            session_attributes['state'] = 'started'
    else:
        # direct intent ??
        session_attributes = {}
        session_attributes['state'] = 'started'

    return session_attributes


def gen_twitter_sentence(twitter_id):
    if twitter_id:
        str = 'I found your twitter ID, ' + twitter_id + ". "
    else:
        str = ""

    return str


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


def load_attendees():
    return json.load(open('data/attendees.json'))

def put_event_to_firehorse(intent_request, session):
    data = {}
    client = boto3.client('firehose',region_name='us-east-1')
    data['request'] = intent_request
    data['session'] = session
    client.put_record(DeliveryStreamName=lamvery.secret.get('fh_stream'), Record={'Data' : str(data) + "\n"})
    return True
