import time
import sqlite3

class lastspoke:
    def __init__(self):
        self.dbFile = './lastspoke.db'
        self.createDB()
    
    def createDB(self):
        """
        Create database to store user's messages
        """
        self.conn = sqlite3.connect(self.dbFile)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS lastspoke (username TEXT UNIQUE, message TEXT, channel TEXT, date TEXT, time TEXT)")
        self.cursor.close()

    def lastSpoke(self, channel, username, message):
        """
        Insert into the database, username, message, channel and time
        everytime a user speaks - Updates the row, if they have spoken previously
        """
        self.conn = sqlite3.connect(self.dbFile)
        self.cursor = self.conn.cursor()
        theTime = time.gmtime()#does things for GMT
        theDate = "{0}-{1}-{2}".format(theTime.tm_year, theTime.tm_mon, theTime.tm_mday)
        hour = str(theTime.tm_hour+1)
        minute = str(theTime.tm_min)
        if len(hour) == 1: hour = "0"+hour
        if len(minute) == 1: minute = "0"+minute
        theTime = "{0}:{1}".format(hour, minute)
        self.cursor.execute("SELECT * FROM lastspoke WHERE username=?", [(username)])
        if self.cursor.fetchone() == None:
            sql = "INSERT INTO lastspoke VALUES (?, ?, ?, ?, ?)"
            self.cursor.execute(sql, (username, message, channel, theDate, theTime))
        else:
            sql = "UPDATE lastspoke SET message=?, date=?, time=?, channel=? WHERE username=?"
            self.cursor.execute(sql, (message, theDate, theTime, channel, username))
        self.conn.commit() 
        self.cursor.close()

    def getLastSpoke(self, channel, username, connection):
        """
        Retrieve a user's last message and send to the channel
        """
        self.conn = sqlite3.connect(self.dbFile)
        self.cursor = self.conn.cursor()
        theDate = time.gmtime()
        self.cursor.execute("SELECT * FROM lastspoke WHERE username=?", [(username)])
        result = self.cursor.fetchone()
        tDate = result[3]
        connection.privmsg(channel, "{0} - {1} - {2}".format(tDate, result[0], result[1]))
        return 0
        """if int(tDate[0]) < theDate.tm_year or int(tDate[1]) < theDate.tm_mon or int(tDate[2]) < theDate.tm_mday:
        year = str(tDate[0])
        month = str(tDate[1])
        day = str(tDate[2])
        if len(month) == 1: month = "0"+month
        if len(day) == 1: day = "0"+day
        sDate = "{0}/{1}/{2}".format(year, month, day)
        connection.privmsg(channel, u"{0}\u00036[\u000300{1}\u00036]\u00030\u00033 {2} \u00030\u00036<\u000300{3}\u00036>\u000300 {4}".format(sDate, row[0], row[1], row[2], row[3]) )
        return 0
        connection.privmsg(channel, "I don't think I've seen {0}".format(user))
        """
        self.cursor.close()
        
    def on_pubmsg(self, nick, connection, event):
        self.connection = connection
        message = event.arguments()[0]
        source = event.source().split('!')[0]
        self.lastSpoke(event.target(), source, message)
        if message.startswith(".seen"):
            user = message.split(' ')[1]
            self.getLastSpoke(event.target(), user, connection)

