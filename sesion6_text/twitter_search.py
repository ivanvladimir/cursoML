#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2016/IIMAS/UNAM
# ----------------------------------------------------------------------

from __future__ import division, print_function  # Python 2 users only
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import config
import json
import os

verbose = lambda *a: None 
keepcharacters = (' ','.','_')

if __name__ == '__main__':
    # Command line options
    p = argparse.ArgumentParser("Twitter search")
    p.add_argument("-q", "--query", dest="query",nargs="+",
                    help="Query/Filter",default='#ironia')
    p.add_argument("-l", "--lang", dest="lang",
                    help="Language",default='es')
    p.add_argument("-i","--items",dest="nitems",type=int,
                   help="Maximum number of tweets to recover", default=1000)
    p.add_argument("-d","--output-dir",dest="output_dir",
                   help="Output/Data Directory", default='.')
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Modo verbose [Off]")
    p.add_argument('--version', action='version', version='create_segments 0.1')
    opts = p.parse_args()

    # Prepara función de verbose  -----------------------------------------
    if opts.verbose:
        def verbose(*args,**kargs):
            print(*args,**kargs)
    else:   
        verbose = lambda *a: None 

    query_="".join(c for c in opts.query if c.isalnum() or c in keepcharacters).rstrip()
    outfile=os.path.join(opts.output_dir,"results_"+opts.lang+"_"+query_+".txt")
    verbose("Output file set to:", outfile)


    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

    with open(outfile, 'a') as f:
        for tweet in tweepy.Cursor(api.search,
                           q=[x.decode('unicode-escape') for x in opts.query],
                           rpp=100,
                           result_type="recent",
                           languages=[opts.lang]).items(opts.nitems):
                jtweet=json.dumps(tweet._json)
                verbose(jtweet)
                f.write(jtweet)
        
