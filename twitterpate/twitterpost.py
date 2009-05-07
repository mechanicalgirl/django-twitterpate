#!/usr/bin/python

import MySQLdb as Database
import base64, urllib, urllib2
import myproject.settings as settings

SINGLEVIEW = 'http://127.0.0.1:8000/id/'

def main():
    db = Database.connect(settings.DATABASE_HOST, settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_NAME)
    cursor = db.cursor(Database.cursors.DictCursor)

    sql = """SELECT * FROM twitterpate_post WHERE approved=1 AND posted=0"""
    cursor.execute(sql)
    data = cursor.fetchall()

    twitter_username = "my_twitter_username"
    twitter_password = "my_twitter_password"

    for record in data:
	message_id = str(record["id"])
        message = record["message"]
        """
	stripping commas out here because they'll wreak havoc with response parsing 
	but the original message remains intact in the database
	"""
        message = message.replace(',', '')

        long_url = SINGLEVIEW + message_id
        request = urllib2.Request("http://tinyurl.com/api-create.php?url="+long_url)
        response = urllib2.urlopen(request) 
	short_url = response.read()

	slen = len(short_url)
	message_length = 135 - slen
	message = message[0:message_length]
	message = message + " ... " + short_url

        request = urllib2.Request('http://twitter.com/statuses/update.json')
        request.headers['Authorization'] = 'Basic %s' % ( base64.b64encode(twitter_username + ':' + twitter_password),)
        request.data = urllib.urlencode({'status': message})
        response = urllib2.urlopen(request) # The Response

        null = 0
        false = 0
        a = eval(response.read()) 
        d = int(a["id"])
        
	if response.code == 200 and type(d) == int:
	    record_id = record["id"]
	    sql = """UPDATE twitterpate_post SET posted=1, post_date=NOW(), twitter_id=%s WHERE id=%s""" %(d, record_id)
	    cursor.execute(sql)

    cursor.close()
    db.close()

if __name__ == "__main__":
    main()

