#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 for amimoto_alexa
"""


import lamvery
import twitter
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
    card_title = "Impression"

    debug_logger(session)

    if session_attributes['state'] in ['started']:
        speech_output = 'Please tell me your name first, by saying, i am John Smith'
        card_title = "Null"
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, speech_output, should_end_session))

    speech_output = "Thank you {0}! You can see impressions on twitter and ,A MI MO TO Blog.".format(session_attributes['VisitorName']) \
                    + "Have a nice day! "

    impression = intent['slots']['UserImpression']['value']

    tw_ck, tw_cs, tw_ak, tw_as = lamvery.secret.get('tw_keys').split(',')
    tw_api = twitter.Api(consumer_key=tw_ck,
                         consumer_secret=tw_cs,
                         access_token_key=tw_ak,
                         access_token_secret=tw_as)

    # check right user?
    debug_logger(session['user']['userId'])
    amimoto_user = re.compile(lamvery.secret.get('dc_id'))
    if amimoto_user.match(session['user']['userId']):
        # post actions
        comment_to_wordpress(session_attributes['VisitorName'], impression)
        if session_attributes['twitter_id']:
            tw_post = impression + " by " + session_attributes['twitter_id']
        else:
            tw_post = impression

        tw_api.PostUpdate(tw_post)

    session['attributes']['UserImpression'] = impression
    put_event_to_firehorse(intent, session)
    should_end_session = True
    return build_response(None, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
