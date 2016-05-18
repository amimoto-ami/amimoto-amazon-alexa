#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 for amimoto_alexa
 POST comment for WordPress REST API

 @param AUTHOR_NAME:string
 @param COMMENT:string
 @usage comment_to_wordpress( AUTHOR_NAME, COMMENT )
"""

import urllib
import urllib2
import yaml
yaml_path = 'data/WPConf.yml'

def create_query( author_name, comment ):
	params = {
		'content': comment,
		'author_name': author_name
	}
	return params;

def post_comment( url, params ):
	api_url = url + '/wp-json/wp/v2/comments/';
	params = urllib.urlencode( params )
	req = urllib2.Request( api_url )
	req.add_data( params )
	res = urllib2.urlopen( req )
	body = res.read()

def comment_to_wordpress( author_name, comment ):
	conf = yaml.load( open( yaml_path, 'r' ) )
	query = create_query( author_name, comment  )
	query['post'] = conf['wordpress']['post']
	url = conf['wordpress']['url']
	post_comment( url, query )
