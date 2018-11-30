#!/usr/bin/env python

import time
from getpass import getpass
from textwrap import TextWrapper

import tweepy


class StreamWatcherListener(tweepy.StreamListener):

    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')

    def on_status(self, status):
        try:
            print(self.status_wrapper.fill(status.text))
            print('\n %s  %s  via %s\n' % (status.author.screen_name, status.created_at, status.source))
        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status_code):
        print('An error has occured! Status code = %s' % status_code)
        return True  # keep stream alive

    def on_timeout(self):
        print('Snoozing Zzzzzz')


def main():
    # Prompt for login credentials and setup stream object
    consumer_key = "8Td6x4leLN18211ukncCz2K0H "
    consumer_secret = "z7eMDcHXCgfrAMHUZb6J2K3AaX02Xt1PQ5vkpDV6tUHlqrG7GM "
    access_token = "719909534-Ui9024F0S1lvdsm4xmqI3c6ZJf21i0IBycIYju3w "
    access_token_secret = "qAlSmWE4CyNt2J9rUK2phJdY3gDC6hYuJcTMhJ4UgpyUs "

    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, StreamWatcherListener(), timeout=None)

    # Prompt for mode of streaming
    valid_modes = ['sample', 'filter']
    while True:
        mode = "filter"
        if mode in valid_modes:
            break
        print('Invalid mode! Try again.')

    if mode == 'sample':
        stream.sample()

    elif mode == 'filter':
        follow_list = ("H&M")
        track_list = ("H&M")
        if follow_list:
            follow_list = [u for u in follow_list.split(',')]
            userid_list = []
            username_list = []

            for user in follow_list:
                if user.isdigit():
                    userid_list.append(user)
                else:
                    username_list.append(user)

            for username in username_list:
                user = tweepy.API().get_user(username)
                userid_list.append(user.id)

            follow_list = userid_list
        else:
            follow_list = None
        if track_list:
            track_list = [k for k in track_list.split(',')]
        else:
            track_list = None
        print(follow_list)
        stream.filter(follow_list, track_list)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Goodbye!')
