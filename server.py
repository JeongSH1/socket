import socket, threading
import json
import time
from random import *

class Room:
    def __init__(self):
        self.hangMan = HangMan(self)
        self.participants = []
        self.waiting = []
        self.assignedNum = 1

    def addParticipant(self, c):
        self.participants.append(c)

    def delParticipant(self, c):
        self.participants.remove(c)

        if len(self.participants) == 0:
            self.__init__()

    def addWaiting(self, c):
        self.waiting.append(c)
    
    def delWaiting(self, c):
        self.waiting.remove(c)
    
    def sendObjAll(self, obj):
        obj = json.dumps(obj)
        for client in self.participants:
            client.sendMsg(obj)

        for client in self.waiting:
            client.sendMsg(obj)

    def sendMsgAll(self, msg):
        for client in self.participants:
            client.sendMsg(msg)
        for client in self.waiting:
            client.sendMsg(msg)

class HangMan:
    def __init__(self, room):
        self.problems = []
        self.obj = {
            "hangManStatus": 0,
            "alphabets": [['Aa',True],['Bb',True],['Cc',True],['Dd',True],['Ee',True],['Ff',True],['Gg',True],
                            ['Hh',True],['Ii',True],['Jj',True],['Kk',True],['Ll',True],['Mm',True],['Nn',True],
                            ['Oo',True],['Pp',True],['Qq',True],['Rr',True],['Ss',True],['Tt',True],['Uu',True],
                            ['Vv',True],['Ww',True],['Xx',True],['Yy',True],['Zz',True]],
            "hint": "",
            "answer": [],
            "answerStatus": [],
            "turn": 0,
            "scores": [],
            "msg": ""
        }
        self.room = room
        self.running = False

    def readData(self):
        with open('data.txt', 'r') as f:
            hint = f.readline().strip()
            ans = f.readline().strip()
            while ans:
                self.problems.append([ans, hint])
                b = f.readline()
                hint = f.readline().strip()
                ans = f.readline().strip()
            f.close()


    def start(self):
        if len(self.room.participants) > 0:
            self.readData()
            problem_num = randint(0, len(self.problems)-1)
            self.obj['hint'] = self.problems[problem_num][1]
            self.obj['answer'] = self.problems[problem_num][0]
            self.obj['answerStatus'] = [None for _ in range(len(self.obj['answer']))]
            self.obj['scores'] = [[self.room.participants[i].id, self.room.participants[i].score] for i in range(len(self.room.participants))]
            self.running = True

            self.obj['msg'] = f"Server> Game Start {self.room.participants[0].id} turn"
            self.room.sendObjAll(self.obj)
        
        else:
            print("There are no participants")


    def setObj(self, msg):
        ans = self.obj['answer']
        msg = msg.upper()

        if msg.lower() in ans or msg in ans: #Correct
            if self.obj['alphabets'][ord(msg)-65][1]:
                for i in range(len(ans)):
                    if ans[i].upper() == msg:
                        self.obj['answerStatus'][i] = ans[i]
                        self.obj['msg'] = "Server> Correct! "
                self.room.participants[self.obj['turn']].score += 10


            else:       #Correct but alphabet alreay used
                self.obj['hangManStatus'] += 1
                self.obj['msg'] = "Server> Wrong! "
            
        else: #Wrong
            self.obj['hangManStatus'] += 1 
            self.obj['msg'] = "Server> Wrong! "
        
        self.obj['alphabets'][ord(msg)-65][1] = False #set used alphabet

        self.obj['turn'] = (self.obj['turn'] + 1) % len(self.room.participants) #set turn

        self.obj['scores'] = [[self.room.participants[i].id, self.room.participants[i].score] for i in range(len(self.room.participants))]

        if None not in self.obj['answerStatus'] or self.obj['hangManStatus'] >= 8: #if game over
            self.obj['msg'] += f"Answer is {self.obj['answer']} \nRestart in 5sec\n"
            self.room.sendObjAll(self.obj)
            time.sleep(5)
            self.restart()

        else:
            self.obj['msg'] += f"{self.room.participants[self.obj['turn']].id} turn\n"  
            self.room.sendObjAll(self.obj)

    def attemptAnswer(self, msg):
        if msg.upper() == self.obj['answer'].upper():
            self.room.participants[self.obj['turn']].score += 10 * self.obj['answerStatus'].count(None)
            self.obj['msg'] = f"Server > Correct! Answer is {self.obj['answer']} \nRestart in 5sec\n"
            self.obj['answerStatus'] = list(self.obj['answer'])
            self.room.sendObjAll(self.obj)
            time.sleep(5)
            self.restart()

        else:
            self.obj['hangManStatus'] += 1
            self.obj['msg'] = "Server> Wrong! "
            

            if None not in self.obj['answerStatus'] or self.obj['hangManStatus'] >= 8: #if game over
                self.obj['msg'] += f"Answer is {self.obj['answer']} \nRestart in 5sec\n"
                self.room.sendObjAll(self.obj)
                time.sleep(5)
                self.restart()

            else:
                self.obj['turn'] = (self.obj['turn'] + 1) % len(self.room.participants)
                self.obj['scores'] = [[self.room.participants[i].id, self.room.participants[i].score] for i in range(len(self.room.participants))]
                self.obj['msg'] += f"{self.room.participants[self.obj['turn']].id} turn\n"
                self.room.sendObjAll(self.obj)

    def restart(self):
        self.readData()
        problem_num = randint(0, len(self.problems)-1)
        self.obj['hangManStatus'] = 0
        self.obj['hint'] = self.problems[problem_num][1]
        self.obj['answer'] = self.problems[problem_num][0]
        self.obj['answerStatus'] = [None for _ in range(len(self.obj['answer']))]
        self.obj['alphabets'] = [['Aa',True],['Bb',True],['Cc',True],['Dd',True],['Ee',True],['Ff',True],['Gg',True],
                            ['Hh',True],['Ii',True],['Jj',True],['Kk',True],['Ll',True],['Mm',True],['Nn',True],
                            ['Oo',True],['Pp',True],['Qq',True],['Rr',True],['Ss',True],['Tt',True],['Uu',True],
                            ['Vv',True],['Ww',True],['Xx',True],['Yy',True],['Zz',True]]
        self.running = True

        self.room.participants += self.room.waiting
        self.room.waiting = []

        for client in self.room.participants:
            client.auth = True

        self.obj['turn'] = 0
        self.obj['scores'] = [[self.room.participants[i].id, self.room.participants[i].score] for i in range(len(self.room.participants))]
        self.obj['msg'] = f"Server> Game Start {self.room.participants[self.obj['turn']].id} turn"
        self.room.sendObjAll(self.obj)


class SocketForClient:
    
    def __init__(self, r, soc, auth):
        self.room = r  
        self.id = 'Client' + str(self.room.assignedNum)
        self.room.assignedNum += 1
        self.score = 0
        self.soc = soc
        self.auth = auth #participation authority

    def msgHandler(self, msg):
        print(self.id + " send to server> " + msg)
        p = msg.strip().split(' ')

        if p[0] == '/end': # 사용자가 종료를 원할 때
            self.sendMsg("Server> ACCEPT END")
            self.soc.close()
            self.room.delParticipant(self)
            print(self.id, "disconnected")
            raise Exception

        elif p[0] == '/use': # 권한, 게임중, 차례, len(p) == 2
            if self.auth and self.room.hangMan.running and self.room.participants[self.room.hangMan.obj['turn']].soc == self.soc and len(p) == 2 and len(p[1]) == 1:
                self.room.hangMan.setObj(p[1])

            else:
                self.sendMsg("Server> Non Valid Message")

        elif p[0] == '/answer':
            if self.auth and self.room.hangMan.running and self.room.participants[self.room.hangMan.obj['turn']].soc == self.soc and len(p) == 2:
                if self.room.hangMan.obj['answerStatus'].count(None) < len(self.room.hangMan.obj['answer']) // 2:
                    self.room.hangMan.attemptAnswer(p[1])
                else:
                    self.sendMsg("Server> You can't guess the answer.")
            else:
                self.sendMsg("Server> Non Valid Message")
        
        else:
            if self.auth:
                msg = self.id + "> " + msg
                self.room.sendMsgAll(msg)


    def readMsg(self):
        try:
            self.room.sendMsgAll("Server> " + self.id + " connected" + '\n' + ' ' * 70)
            while True:
                msg = self.soc.recv(1024).decode()
                self.msgHandler(msg)
        except:
            self.room.sendMsgAll(f"Server> {self.id} disconnected")
            if self.room.hangMan.running:
                self.room.sendMsgAll(f"\n{self.room.participants[self.room.hangMan.obj['turn']].id} turn")

    def sendMsg(self, msg):
        self.soc.sendall(msg.encode(encoding='utf-8'))

class GameServer:
    ip = '127.0.0.1'
    port = 10000

    def __init__(self):
        self.server_soc = None
        self.room = Room()
        self.running = True

    def open(self):
        self.server_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_soc.bind((GameServer.ip, GameServer.port))
        self.server_soc.listen()
        print('Server is running')

    def commandLine(self):
        while True:
            cmd = input()
            if cmd == '/start':
                print("game start")
                self.room.hangMan.start()

            if cmd == '/end':
                self.room.sendMsgAll('ShutDown')
                self.running = False
                break
    
    def run(self):
        self.open()

        comm = threading.Thread(target=self.commandLine)  #command thread
        comm.start()

        while True:
            client_soc, addr = self.server_soc.accept()
            print(addr, 'Connected')

            if not self.room.hangMan.running:
                c = SocketForClient(self.room, client_soc, True)
                self.room.addParticipant(c)
            else:
                c = SocketForClient(self.room, client_soc, False)
                self.room.addWaiting(c)
            
            th = threading.Thread(target = c.readMsg)
            th.start()

        self.server_soc.close()

        



gameServer = GameServer()
gameServer.run()

