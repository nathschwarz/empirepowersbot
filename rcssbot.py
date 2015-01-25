#!/usr/bin/env python3
#License: GPL v2

import praw
import logging
import argparse
import re

user_agent = 'reddit css change bot v0.1 by /u/nath_schwarz'

username = ''
password = ''

subreddit = ''
page = 'config/stylesheet'

regex_date = 'DATE: ([A-Z\/]{5,7}) ([0-9]+)'

months = [
        'JAN/FEB',
        'MAR/APR',
        'MAY/JUN',
        'JUL/AUG',
        'SEP/OCT',
        'NOV/DEC',
        'PAUSE'
        ]

#globals
r = praw.Reddit(user_agent = user_agent)
logger = None

def login():
    """Logs in to reddit with given username and password."""
    global r
    try:
        r.login(username, password)
        logger.info('Login successful')
    except Exception as e:
        logger.error(e)

def replace(match):
    if not match:
        logger.error('Match not possible')
        return 'ERROR'
    else:
        #Assigns new month
        month = months[(months.index(match.group(1)) + 1) % 7]
        #Increments year if index of month is 0 (== tuesday)
        date = str(int(match.group(2))+1) if months.index(month) is 0 else match.group(2)
        logger.info(month + ' ' + date)
        return 'DATE: {} {}'.format(month, date)

def pull_stylesheet():
    logger.info('Pulling stylesheet')
    return r.get_wiki_page(subreddit, page).content_md

def push_stylesheet(stylesheet):
    logger.info('Uploading stylesheet')
    r.edit_wiki_page(subreddit, page, stylesheet)

def do():
    css = pull_stylesheet()
    css = re.sub(regex_date, replace, css)
    css = re.sub('&gt;', '>', css)
    push_stylesheet(css)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("--stdout", action="store_true", help="print log output to stdout")
    args = parser.parse_args()

    global logger
    if args.verbose:
        logging.basicConfig(level = logging.INFO)
    else:
        logging.basicConfig(level = logging.ERROR)
    if not args.stdout:
        logging.basicConfig(filename = 'empirepowers.log')
    logger = logging.getLogger('empirepowers')

    login()
    try:
        do()
    except Exception as e:
        logger.error(e)
    r.clear_authentication()

if __name__ == "__main__":
    main()
