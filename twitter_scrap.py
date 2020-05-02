import os
import sys
import time
import requests
import argparse

from bs4 import BeautifulSoup 

import random
import string 


from re import findall
from urllib.request import urlopen

import json


class Twitter(object):

    def __init__(self, username):
        self.username = username

    def RetrieveAccountInformation(self):
        account_information = []
        dataopt = ""
        url = "http://www.twitter.com/" + self.username
        print("\n\nGathers Details of " + self.username + " from Twitter")
        response = None
        try:
            response = requests.get(url)
        except Exception as e:
            print(repr(e))
            sys.exit(1)
    
        if response.status_code != 200:
            print("Non success status code returned "+str(response.status_code))
            sys.exit(1)

        soup = BeautifulSoup(response.text, 'lxml')

        if soup.find("div", {"class": "errorpage-topbar"}):
            print("\n\n Error: Invalid username.")
            sys.exit(1)

        twname = soup.title.text.split("|")[0]
        twbio = soup.find("p", {"class": "ProfileHeaderCard-bio u-dir"}).text
        join_date = soup.find("span", {"class": "ProfileHeaderCard-joinDateText js-tooltip u-dir"})
        twjoin = join_date['title']
        followers = soup.find("li", {"class": "ProfileNav-item ProfileNav-item--followers"}).find('a')
        twfollowers = followers['title']
        followers = soup.find("li", {"class": "ProfileNav-item ProfileNav-item--following"}).find('a')
        twfollowing = followers['title']
        pictureURL = soup.find("a",{"class": "ProfileAvatar-container u-block js-tooltip profile-picture"})
        twdp = pictureURL['data-url']

        filename = self.username+"_twitter.json"
        print("Dumping data in file " + filename)
        data = dict()
        data["Bio: "] = twbio
        data["Join date: "] = twjoin
        data["Followers: "] = twfollowers
        data["Following: "] = twfollowing
        data["Profile URL: "] = twdp

        dataopt = '''
        > Name          :: {}
        > Bio           :: {}
        > Join date     :: {}
        > Followers     :: {}
        > Following     :: {}
        > Profile URL   :: {}

            '''.format(str(twname), str(data['Bio: ']),
            str(data['Join date: ']), str(data['Followers: ']),
            str(data['Following: ']), str(data['Profile URL: ']))

        with open(filename, 'w') as fh:
            fh.write(json.dumps(data))

        return dataopt
           



def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-tw", 
                        "--twitter",
                        type=str,
                        help="return the information associated with specified twitter account",
                        )

    args = parser.parse_args()

    if args.twitter:
        print("Attempting To Gather Account Information")
        try:
            print(Twitter(args.twitter).RetrieveAccountInformation())
        except KeyboardInterrupt as ki:
            print("\tExiting")
            sys.exit(1)


if __name__ == "__main__":
    main() 