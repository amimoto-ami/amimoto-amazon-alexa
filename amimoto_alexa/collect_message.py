#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 for amimoto_alexa
"""


import lamvery
import boto3
import re
from helpers import *
from wpapi import *
from tweet_message import *
from debugger import *


def collect_impression(intent, session):
    """Collect impression and finalize session
    """
    session_attributes = build_session_attributes(session)
    card_title = "Thank you for trying AMIMOTO Ninja !!"

    debug_logger(session)

    if session_attributes['state'] in ['started']:
        speech_output = '<p>Please tell me your name first, by saying, <break time="0.2s"/> i am John Smith</p>'
        card_title = "Please tell me your name first."
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, speech_output, should_end_session))
    elif session_attributes['state'] in ['on_question', 'got_name']:
        speech_output = '<p>Please ask to me by saying, <break time="0.2s"/> What is WordPress?, or Can I use free trial?</p>'
        card_title = "Usage of AMIMOTO Ninja."
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, speech_output, should_end_session))

    speech_output = '<p>Thank you {0}!'.format(session_attributes['VisitorName']) \
                    + '<p>You can see impressions on twitter and ' \
                    + '<phoneme alphabet="ipa" ph="amimoʊtoʊ">amimoto</phoneme></p> Blog.</p>'.format(session_attributes['VisitorName']) \
                    + "Have a nice day! "

    try:
        impression = intent['slots']['UserImpression']['value']
    except KeyError:
        impression = "Thank you! (Ninja failed convert to text.)"

    # check right user?
    debug_logger(session['user']['userId'])
    amimoto_user = re.compile(lamvery.secret.get('dc_id'))
    if amimoto_user.match(session['user']['userId']):
        # post actions
        comment_to_wordpress(session_attributes['VisitorName'], impression)
        if session_attributes['twitter_id']:
            tw_post = session_attributes['VisitorName'] + " says. [ " + impression + " ] " + session_attributes['twitter_id']
        else:
            tw_post = session_attributes['VisitorName'] + " says. [ " + impression + " ]"

        post_to_twitter(tw_post)

    session['attributes']['UserImpression'] = impression
    put_event_to_firehorse(intent, session)
    should_end_session = True
    return build_response(None, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
