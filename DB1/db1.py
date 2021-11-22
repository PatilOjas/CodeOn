from xmlrpc.server import SimpleXMLRPCServer
import sqlite3

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()

def create(props):
    cur.execute(f"""
    INSERT INTO editor_Codes ('userid', 'qid', 'code', 'output') values ({props['userid']}, {props['qid']}, '{props['code']}', '{props['output']}');
    """)
    conn.commit()
    # cur.fetchall()

def update(props):
    cur.execute(f"""
        UPDATE editor_Codes SET code='{props['code']}', output='{props['output']}' where userid={props['userid']} AND qid={props['qid']};
    """)
    conn.commit()

ipAddr = "127.0.0.1"
portNo = 9001

server = SimpleXMLRPCServer((ipAddr, portNo), allow_none=True)
server.register_function(create, 'db1C')
server.register_function(update, 'db1U')

print(f"Server started at {ipAddr}:{portNo}")
server.serve_forever()
