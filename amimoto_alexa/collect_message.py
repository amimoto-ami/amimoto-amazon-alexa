#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 for amimoto_alexa
"""


import lamvery
import twitter
from helpers import *
from wpapi import *
from debugger import *


def collect_impression(intent, session):
    """Collect impression and finalize session
    """
    session_attributes = build_session_attributes(session)
    card_title = "Impression"

    debug_logger(session)
    speech_output = "Thank you! You can see impressions on twitter and ,A MI MO TO Blog." \
                    "Have a nice day! "

    impression = intent['slots']['UserImpression']['value']

    tw_ck, tw_cs, tw_ak, tw_as = lamvery.secret.get('TW_KEYS').split(',')
    debug_logger(lamvery.secret.get('TW_KEYS'))
    tw_api = twitter.Api(consumer_key=tw_ck,
                         consumer_secret=tw_cs,
                         access_token_key=tw_ak,
                         access_token_secret=tw_as)

# todo: store session summary to firehose
    debug_logger(session['user']['userId'])

    # check right user?
    # if lamvery.secret.get('DC_ID') == session['user']['userId']:
    comment_to_wordpress(session_attributes['VisitorName'], impression)
    if session_attributes['twitter_id']:
        tw_post = impression + " by " + session_attributes['twitter_id']
    else:
        tw_post = impression

    tw_api.PostUpdate(tw_post)



    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
