import json
import message

string = '{"to": "sufre", "from": "server", "id": 1375284519, "params": {"status": "wait", "players": {"sufre": {"cards": [], "posts": []}}}, "method": "gameStatus"}'
print string
print ''
message.messagePool = string
msg = message.getMessageFromPool()
print msg
print ''
print message.messagePool
print ''
params = json.loads(msg)
print params