"""
Manage the CRUD functionality for the database
"""

import sqlite3
from pprint import pprint

class DB:
    def __init__(self, source, twitter_handle):
        conn = sqlite3.connect('Posts.db')
        with conn:
            #Create tables if necessary.....
            conn.execute('''CREATE TABLE if not exists Posts
                        (UID     TEXT PRIMARY KEY     NOT NULL,
                         Title   TEXT    NOT NULL,
                         Link    TEXT    NOT NULL,
                         Source  TEXT NOT NULL,
                         FOREIGN KEY (Source) REFERENCES Source(Source));''')
            conn.execute('''CREATE TABLE if not exists Videos
                                    (UID     TEXT PRIMARY KEY     NOT NULL,
                                     Title   TEXT    NOT NULL,
                                     Link    TEXT    NOT NULL,
                                     Date    TEXT    NOT NULL,
                                     Thumb   TEXT    NOT NULL);''')
            conn.execute('''CREATE TABLE if not exists Source
                        (Source TEXT PRIMARY KEY     NOT NULL,
                         Twitter          TEXT    NOT NULL);''')

            #add Source and twitter handle to Source table
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM Source WHERE Source = ? AND Twitter =?", (source, twitter_handle))
            data = cursor.fetchone()[0]
            # If this source is new, insert into Source table
            if data == 0:
                cursor.execute('insert into Source values (?,?)', (source, twitter_handle))

    @staticmethod
    def add_new_content(source, uid, title, link):
        conn = sqlite3.connect('Posts.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM Posts WHERE Source = ? AND UID =?", (source, uid))
            data = cursor.fetchone()[0]
            #If this post is new, insert in DB and return True
            if data == 0:
                try:
                    cursor.execute('insert into posts values (?,?,?,?)', (uid, title, link, source,))
                    return True
                except sqlite3.IntegrityError:
                    pass
            #Return False for existing content (or content had insufficient detail,
            #for example missing a link that produced an integrity error
            return False

    @staticmethod
    def add_new_video(video_json):
        if 'eng' not in str(video_json.get('language')).lower():
            return False
        #pprint(video_json)
        UID = video_json.get('videos')[0]['url']
        Title = video_json.get('title')
        Link = video_json.get('videos')[0]['url']
        Date = video_json.get('recorded')
        Thumb = video_json.get('thumbnail_url')

        conn = sqlite3.connect('Posts.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM Videos WHERE UID =?", (UID,))
            data = cursor.fetchone()[0]
            #If this video is new, insert in DB and return True
            if data == 0:
                try:
                    cursor.execute('insert into Videos values (?,?,?,?,?)', (UID, Title, Link, Date, Thumb))
                    return True
                except sqlite3.IntegrityError:
                    pass
            #Return False for existing content (or content had insufficient detail,
            #for example missing a link that produced an integrity error
            return False

