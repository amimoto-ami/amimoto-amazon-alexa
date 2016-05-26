#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 for amimoto_alexa
"""

import lamvery
import twitter
from helpers import *
from debugger import *


def post_to_twitter(tw_post):
    tw_ck, tw_cs, tw_ak, tw_as = lamvery.secret.get('tw_keys').split(',')
    tw_api = twitter.Api(consumer_key=tw_ck,
             consumer_secret=tw_cs,
             access_token_key=tw_ak,
             access_token_secret=tw_as)
    try:
        tw_api.PostUpdate(tw_post)
    except:
        pass
    return True
