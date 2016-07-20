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

class Collector(StreamListener):
    """Custom StreamListener for streaming data."""

    def __init__(self, output_dir, query="#ironia", lang="es"):
        query_="".join(c for c in query if c.isalnum() or c in keepcharacters).rstrip()
        self.oufile=os.path.join(output_dir,lang+"_"+query_)

    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:
                f.write(data)
                verbose(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True


if __name__ == '__main__':
    # Command line options
    p = argparse.ArgumentParser("Twitter collector")
    p.add_argument("-q", "--query", dest="query",nargs="+",
                    help="Query/Filter",default='#ironia')
    p.add_argument("-l", "--lang", dest="lang",
                    help="Language",default='es')
    p.add_argument("-d","--data-dir",dest="data_dir",
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

    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

    twitter_stream = Stream(auth, Collector(opts.data_dir, opts.query, opts.lang))
    twitter_stream.filter(track=[opts.query],languages=[opts.lang])
