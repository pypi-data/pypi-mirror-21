#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author:: drymer <drymer [ EN ] autistici.org>
# Copyright:: Copyright (c) 2016, drymer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import argparse
import configparser
import hashlib
import logging
import time
import urllib.parse
import urllib.request
import sqlite3
from html.parser import HTMLParser
from os import listdir, path
from re import findall
from sys import argv, exit
from xml.dom import minidom
import requests
import feedparser


# Logging stuff
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(funcName)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Database:
    """Manage the database."""
    def __init__(self, database='gnusrss.db'):
        """
        Connect to the database.

        database -- string containig the filepath of the db
        """
        self.connection = sqlite3.connect(database)
        logger.info('Sqlite database connected')

    def create_tables(self):
        """Create table and columns."""
        current = self.connection.cursor()
        drop = 'DROP TABLE IF EXISTS items'
        create = 'CREATE TABLE items(id INTEGER PRIMARY KEY, feed TEXT, po' + \
                 'st TEXT, posted INTEGER, url TEXT, lastbuild TIMESTAMP, ' + \
                 'guid TEXT)'
        current.execute(drop)
        logger.info('Sqlite Query: %s', drop)
        current.execute(create)
        logger.info('Sqlite Query: %s', create)

    def insert_data(self, param):
        """
        Insert all the article's information to the table.

        Keyword arguments:
        param -- list containing all the values
        """

        insert = 'INSERT INTO items(feed, post, posted, url, lastbuild, gu' + \
                 'id) VALUES(\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")' \
                 % tuple(param)
        self.connection.execute(insert)
        self.connection.commit()
        logger.info('Sqlite Query: %s', insert)

    def select(self, param):
        """
        Return a select.

        Keyword arguments:
        param -- string containing a sql select
        """
        current = self.connection.cursor()
        current.execute(param)
        rows = current.fetchall()
        logger.info('Sqlite Query: %s', param)
        logger.debug('Sqlite Query Result: %s', rows)

        return rows

    def close(self):
        """Close the database."""
        self.connection.close()
        logger.info('Sqlite database closed')


class StupidParser(HTMLParser):
    """Just a HTML parser."""
    def __init__(self):
        try:
            HTMLParser.__init__(self, convert_charrefs=True)
        except:
            # python 3.2 support
            HTMLParser.__init__(self)
        self.data = []

    def handle_data(self, data):
        self.data.append(data)

    def return_value(self):
        return ''.join(self.data)


class GNUsrss:
    def parse_feed(self, feed, post_format):
        """
        Request the feed, parse it and return requested values on a list
        of lists.

        Keyword arguments:
        feed -- string containing the url or the filepath of the feed
        post_format -- string containing RSS keywords surrounded by {}

        Comment:
        Here it's saved way more tags that aren't necessary. They're added just
        to add more metadata just because it's clearer when viewing the sqlite.
        """

        article = []
        xml = feedparser.parse(feed)
        entries_keys = list(xml.entries[0].keys())
        feed_keys = list(xml.feed.keys())

        # Very ugly way to test existence, but seems to be the only way
        if 'published' in entries_keys:
            lastbuild = xml.entries[0].published
        elif 'published' in feed_keys:
            lastbuild = xml.feed.published
        elif 'updated' in entries_keys:
            lastbuild = xml.entries[0].updated
        elif 'updated' in feed_keys:
            lastbuild = xml.feed.updated
        else:
            # Since the feed doesn't have a date, I'll create it
            lastbuild = time.strftime("%a, %d %b %Y %H:%M:%S GMT")

        if 'link' in feed_keys:
            rss_link = xml.feed.link
        else:
            rss_link = 'http://' + xml.entries[0].link.split('/')[2]

        for item in xml['items']:
            values = {}
            for i in entries_keys:
                if i in post_format:
                    values[i] = item[i]
            post = post_format.format(**values)

            # Stupid HTML code adding to complete the post to parse it
            post = '<html>' + post + '</html>'
            parser = StupidParser()
            parser.feed(post)
            post = parser.return_value()

            if 'guid' in entries_keys:
                guid = item['guid']
            else:
                # Since the feed doesn't have a guid, I'll create it
                guid = hashlib.sha1(post.encode()).hexdigest()

            article.append([rss_link, post, item['link'], lastbuild, guid])

        return article

    def post(self, article, gs_node, username, password, insecure):
        """
        Post the articles to GNU Social.

        Keyword arguments:
        article -- list containing a most of what is necessary on the insert
        gs_node -- string containing the url of the GNU Social node
        username -- string containing the user of GNU Social
        password -- string containing the password of GNU Social
        """

        msg = article[1].split()
        api = (gs_node + '/api/statuses/update.xml')

        # Check for twitter images and call post_image if required
        for word in msg:
            if 'pic.twitter.com/' in word:
                image = self.post_image(word, gs_node, username, password,
                                        insecure)
                if image is not None:
                    index = msg.index(word)
                    msg[index] = image
                else:
                    pass

        msg = ' '.join(msg)
        post_data = {'status': msg, 'source': 'gnusrss'}

        if insecure == 'yes':
            req = requests.post(api, auth=(username, password), data=post_data,
                                verify=False)
        else:
            req = requests.post(api, auth=(username, password), data=post_data)

        logger.info('%s %s %s', req.url, req.status_code, post_data)
        logger.debug('%s', req.text)
        response = req.status_code

        return response

    def post_image(self, picture, gs_node, username, password, insecure):
        """
        Upload a picture to GNU Social hosting and return a string with the
        new url.

        Keyword arguments:
        picture -- string containing the twitter url of a picture
        gs_node -- string containing the url of the GNU Social node
        username -- string containing the user of GNU Social
        password -- string containing the password of GNU Social
        """

        pic = ""
        found = False
        api = gs_node + '/api/statusnet/media/upload'

        # If the picture doesn't exist or is not well written, show must go on
        try:
            html = urllib.request.urlopen('https://' + picture).read().decode(
                'utf-8').splitlines()
        except:
            return picture

        # For debugging purposes
        all_parts = []
        for part in html:
            all_parts.append(part)

        logger.debug('Response: %s', all_parts)

        # Search the hardcoded tag name of the picture
        for part in html:
            if picture in part:
                found = True
            if 'data-image-url' in part and found is True:
                pic = part.split('"')[1]
                break

        # If there's a video instead of a picture, just exit
        if not pic:
            return None

        req = requests.get(pic)

        logger.debug('Response: %s', req.text)

        pic = req.content
        img = {'media': ('useless.jpg', pic)}

        if insecure == 'yes':
            req = requests.post(api, auth=(username, password), verify=False,
                                files=img)

        else:
            req = requests.post(api, auth=(username, password), files=img)

        logger.debug('Response: %s', req.text)

        buffer = req.content
        xmldoc = minidom.parseString(buffer)
        item = xmldoc.getElementsByTagName('rsp')
        url = item.item(0).getElementsByTagName('mediaurl')[0].firstChild.data

        return url

    def compare(self, feeds):
        """
        Compare the picked feed to the saved on the database and return
        list of lists if new.

        Keyword argument:
        feeds -- list of lists containing all actual feeds on the RSS file
        """

        db = Database()
        old = db.select('select guid from items;')
        new_feed = []
        posted = []

        # make the list accesible
        for x in old:
            posted.append(x[0])

        for feed in feeds:
            if feed[4] not in posted:
                new_feed.append(feed)

        db.close()

        return new_feed

    def shortener(self, post):
        """
        Return a shortened url.

        Keyword argument:
        post -- string containing a url to be shortened
        """

        api = ('http://qttr.at/yourls-api.php?format=xml&action=shorturl'
               '&signature=b6afeec983&url=' + post)

        req = requests.post(api)

        logger.debug('Response: %s', req.text)
        buffer = req.content
        xmldoc = minidom.parseString(buffer)
        item = xmldoc.getElementsByTagName('result')
        url = item.item(0).getElementsByTagName('shorturl')[0].firstChild.data

        return url

    def shorten_all(self, post):
        """
        Short all the urls from a notice.

        Keyword arguments:
        post - list containing all the data related to the post to GS
        """

        # Regex taken from stackoverflow, thanks guys
        # It doesn't identify pic.twitter.com url, which is good
        urls = findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&~#=+]|[!*\(\),]'
                       '|(?:%[0-9a-fA-F][0-9a-fA-F]))+', post[1])

        separate = post[1].split(' ')
        # Clean shitty carriage return
        tmp = []

        for i in separate:
            i = i.replace('\n', ' ')
            tmp.append(i)

        separate = tmp

        for i in urls:
            shortened = self.shortener(i)
            position = separate.index(i)
            separate[position] = shortened

        post[1] = ' '.join(separate)

        return post


class Config:
    def create(self, config_name):
        """
        Create config file.

        Keyword argument:
        config_name -- string containing the config's name to be created
        """

        print('Hi! Now we\'ll create de config file!')
        feed = input('Please introduce the feed\'s url: ')
        username = input('Please introduce your username (user@server.com): ')
        password = input('Please introduce your password: ')
        shorten = input('Do you need to shorten the urls that you post? Please'
                        ' take in account \nthat you should only use it if you'
                        'r node only has 140 characters. \nAnswer with "yes" o'
                        'r just press enter if you don\'t want to use it: ')
        fallback_feed = input('Please introduce your feed\'s fallback url. If '
                              'you don\'t want or have one,\njust press enter'
                              ': ')
        print('Now we\'re going to fetch the feed. Please wait...')
        feed_file = feedparser.parse(feed)
        keys = list(feed_file.entries[0].keys())
        print('Done! The tags are: ')
        for tag in keys:
            print('\t' + tag)
        post_format = input('The XML has been parsed. Choose wich format you w'
                            'ant:\nPlease put the tags inside the square brack'
                            'ets\nEx: {title} - {link} by @{author}: ')
        insecure = input('Do you want to allow insecure connection to your GNU'
                         ' social server?\nAnswer with "yes" or just press ent'
                         'er if you don\'t want to use it: ')

        config = configparser.ConfigParser()
        config['feeds'] = {}
        config['feeds']['feed'] = feed
        config['feeds']['user'] = username
        config['feeds']['password'] = password
        config['feeds']['shorten'] = shorten
        config['feeds']['fallback_feed'] = fallback_feed
        config['feeds']['format'] = post_format
        config['feeds']['insecure'] = insecure

        with open(config_name + '.ini', 'w') as configfile:
            config.write(configfile)

    def get(self, name):
        """
        Parse config file and return it on a list.

        Keyword arguments:
        name -- string containing the config's name
        """

        config = []
        parser = configparser.SafeConfigParser()
        parser.read(name)

        for name, value in parser.items('feeds'):
            config.append(value)

        return config


class ParseOptions():
    """Parse command line options of this program."""
    def __init__(self):
        parser = argparse.ArgumentParser(description='Post feeds to GNU Social'
                                         '', prog='gnusrss')
        parser.add_argument('-c', '--create-config', metavar='file_name',
                            dest='create_config', help='creates a config file')
        parser.add_argument('-C', '--create-db', dest='create_database',
                            action='store_true', help='creates the database')
        parser.add_argument('-p', '--post', metavar='config_file', dest='post',
                            help='posts feeds')
        parser.add_argument('-P', '--post-all', dest='post_all', action='store'
                            '_true', help='posts all feeds')
        parser.add_argument('-k', '--populate-database', metavar='file_name',
                            dest='populate_database', help='fetch the RSS and'
                            ' save it in the database')
        parser.add_argument('-v', '--version', dest='version', action='store_t'
                            'rue', help='show version in the '
                            'database')
        parser.add_argument('-V', '--verbose', dest='verbose',
                            metavar='level', help='be more verbose, choose bet'
                            'ween "info" or "debug"')

        self.db = Database()
        self.gs = GNUsrss()
        self.cnf = Config()

        self.args = parser.parse_args()
        # Make all options accesible within self
        self.create_database = self.args.create_database
        self.create_config = self.args.create_config
        self.post = self.args.post
        self.post_all = self.args.post_all
        self.populate_database = self.args.populate_database
        self.version = self.args.version
        self.verbose = self.args.verbose
        self.parser = parser

    def declare_config(self):
        """Assign all config parameters to a self object."""

        config = self.cnf.get(self.config_name)
        self.feed = config[0]
        self.user = config[1].split('@')[0]
        self.password = config[2]
        self.shorten = config[3]
        self.fallback_feed = config[4]
        self.format = config[5]
        # Always use SSL
        self.server = 'https://' + config[1].split('@')[1]
        # Test since in versions previous to 0.2.2 didn't exist
        try:
            self.insecure = config[6]
        except:
            self.insecure = ''

    def post_notice(self):
        """Post notice to GNU social."""

        file_name = self.config_name

        # If first feed and fallback feed aren't available, fail gracefully
        try:
            posts = self.gs.parse_feed(self.feed, self.format)
        except Exception as e:
            print(e)
            if self.fallback_feed:
                posts = self.gs.parse_feed(self.fallback_feed, self.format)
            else:
                print('There\'s been a problem with ' + file_name + ' file.')
                return None

        posts = list(reversed(posts))
        new = self.gs.compare(posts)

        if new:
            # Post only the older item
            self.to_post = new[0]
            if self.shorten == 'yes':
                self.to_post = self.gs.shorten_all(self.to_post)

            if not self.populate_database:
                code = self.gs.post(self.to_post, self.server, self.user,
                                    self.password, self.insecure)

                self.save_in_database(code)

    def save_in_database(self, code):
        """
        Save posts in database

        Keyword arguments:
        code -- HTML code of the notice's post to GNU social
        """

        if self.create_config or self.populate_database or int(code) == \
                int(200):
            self.db.insert_data([self.to_post[0], self.to_post[1], 1,
                                 self.to_post[2], self.to_post[3],
                                 self.to_post[4]])
        elif code != 200:
            print('The notice couldn\'t be posted')

    def pointers(self):
        """This are the options of the program."""

        if self.version:
            print("v0.2.3.1")
            exit()

        if self.verbose:
            if self.verbose == 2 or self.verbose == 'info':
                logger.setLevel(logging.INFO)
            elif self.verbose == 1 or self.verbose == 'debug':
                logger.setLevel(logging.DEBUG)

        if self.create_database:
            if path.exists('gnusrss.db'):
                overwrite = input('The database already exists. Are you '
                                  'sure you want to overwrite it? (y/n) ')

                if overwrite == 'y':
                    self.db.create_tables()
            else:
                self.db.create_tables()

            if not self.create_config and not self.populate_database and \
                    not self.post and not self.post_all:
                self.db.close()

        if self.create_config:
            self.config_name = self.create_config + '.ini'
            self.cnf.create(self.create_config)

            populate = input('Do you want to populate the database? (y) Or you'
                             ' prefer to post old items? (n) ')

            if populate == 'y':
                self.declare_config()
                posts = self.gs.parse_feed(self.feed, self.format)

                for post in posts:
                    self.to_post = post
                    self.save_in_database(0)
                self.db.close()

        elif self.post:
            self.config_name = self.post
            self.declare_config()
            self.post_notice()
            self.db.close()

        elif self.post_all:
            for config in listdir('.'):
                if config.endswith('.ini'):
                    self.config_name = config
                    self.declare_config()
                    self.post_notice()
            self.db.close()

        elif self.populate_database:
            self.config_name = self.populate_database
            self.declare_config()
            posts = self.gs.parse_feed(self.feed, self.format)

            for post in posts:
                self.to_post = post
                self.save_in_database(0)

            self.db.close()

        elif len(argv) == 1:
            self.parser.print_help()


if __name__ == "__main__":
    options = ParseOptions()
    options.pointers()
