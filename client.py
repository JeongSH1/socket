import socket, threading
from tkinter import *
import json
import tkinter.font

class Gui:
    def __init__(self, obj, client):
        self.window = Tk()
        self.window.title("Hang-Man Reviewer")
        self.window.geometry("960x400+100+100")
        self.window.resizable(True, True)
        self.input = None
        self.canvas = None
        self.alphaFrame = None
        self.hintFrame = None
        self.hintCont = None
        self.answerFrame = None
        self.scoreFrame = None
        self.chattingFrame = None
        self.input = None
        self.obj = obj
        self.client = client
        self.chatCont = None
        self.allChat = ""

        self.setInput()

    def setWindow(self):

        self.setCanvas(self.obj['hangManStatus'])
        self.setAlphaFrame(self.obj['alphabets'])
        self.setHintFrame(self.obj['hint'])
        self.setAnswerFrame(self.obj['answer'], self.obj['answerStatus'])
        self.setScoreFrame(self.obj['scores'])
        self.setChattingFrame()

        

    def setInput(self):
        self.input = Entry(self.window, width=10)
        self.input.place(x=700, y=350)
        inputBtn = Button(self.window, text='enter', command = self.client.sendMsg)
        inputBtn.place(x=800, y=350)
        self.input.bind('<Return>', self.client.sendMsg)

    def setCanvas(self, hangManStatus):
        canvas = Canvas(self.window, width=250, height=350, relief='solid', bd=1)

        if hangManStatus >= 1:
            line = canvas.create_line(125, 10, 125, 75)
        if hangManStatus >= 2:
            head = canvas.create_oval(85, 75, 165, 155)
        if hangManStatus >= 3:
            body = canvas.create_line(125, 155, 125, 270)
        if hangManStatus >= 4:
            arm1 = canvas.create_line(50, 120, 125, 200)
        if hangManStatus >= 5:
            arm2 = canvas.create_line(200, 120, 125, 200)
        if hangManStatus >= 6:
            leg1 = canvas.create_line(125,270, 80, 330)
        if hangManStatus >= 7:
            leg2 = canvas.create_line(125,270, 170, 330)
        if hangManStatus >= 8:
            mouth1 = canvas.create_line(115, 130, 135, 145)
            mouth2 = canvas.create_line(135, 130, 115, 145)

        canvas.place(x=30, y=10)

    def setAlphaFrame(self, alphabets):
        alphaFrame = LabelFrame(self.window, text = "Alphabet", width=300, height=100)
        alphaFrame.place(x=300, y=10)

        for i in range(26):
            alphabets_label = Label(alphaFrame, text=alphabets[i][0], width=2, height=1, fg='black')
            if not alphabets[i][1]:
                alphabets_label['text'] = ''
            alphabets_label.grid(row=i//12, column=i%12)


    def setHintFrame(self, hint):
        self.hintFrame = LabelFrame(self.window, text='Hint', width=300, height=90)
        self.hintFrame.place(x=300, y=120)
        font=tkinter.font.Font(family="한초롬돋음", size=15, slant="italic")
        self.hintCont = Label(self.window, text = hint, justify='left', font = font, wraplength=280)
        self.hintCont.place(x=310, y= 140)

    def setAnswerFrame(self, answer, answerStatus):
        answerFrame = LabelFrame(self.window, text='Answer', width=300, height = 70)
        answerFrame.place(x=300, y=230)

        font=tkinter.font.Font(family="한초롬돋음", size=20, slant="italic")

        for i in range(len(answer)):
            answer_label = Label(answerFrame, text=answer[i], width=2, height=1, fg='black',font=font)
            answer_label.grid(row = 1, column = i%len(answer))

            if answerStatus[i] == None:
                answer_label['fg'] = 'systemWindowBackgroundColor'

    def setScoreFrame(self, scores):
        self.scoreFrame = LabelFrame(self.window, text='ScoreBoard', width=300, height=60)
        self.scoreFrame.place(x=300, y=330)
        
        for i in range(len(scores)):
            score_label = Label(self.scoreFrame, text= scores[i][0] + ": " + str(scores[i][1]), width=7, height=1, fg='black')
            score_label.grid(row = 1, column = i%len(scores))


    def setChattingFrame(self):
        self.chattingFrame = LabelFrame(self.window, text = 'Chat')
        self.chattingFrame.place(x=650, y=10)
        self.chatCont = Label(self.chattingFrame,  text=self.allChat, anchor = 's', justify='left', width=30, height=15)
        self.chatCont.pack(side='left')
        


class GameClient:
    ip = '127.0.0.1'
    port = 10000

    def __init__(self):
    
        self.conn_soc = None
        self.obj = {
            "hangManStatus": 8,
            "alphabets": [['Aa',True],['Bb',True],['Cc',True],['Dd',True],['Ee',True],['Ff',True],['Gg',True],
                            ['Hh',True],['Ii',True],['Jj',True],['Kk',True],['Ll',True],['Mm',True],['Nn',True],
                            ['Oo',True],['Pp',True],['Qq',True],['Rr',True],['Ss',True],['Tt',True],['Uu',True],
                            ['Vv',True],['Ww',True],['Xx',True],['Yy',True],['Zz',True]],
            "hint": "Waiting..",
            "answer": [],
            "answerStatus": [],
            "turn": 0,
            "scores": [],
            "msg": ""
        }

        self.gui = Gui(self.obj, self)
    
    def conn(self):
        self.conn_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn_soc.connect((GameClient.ip, GameClient.port))
        
    def sendMsg(self, e = None):
        msg = self.gui.input.get()
        if msg == '/end':
            self.close_x()
        else:
            self.gui.input.delete(0, END)
            self.gui.input.config(text='')
            msg = msg.encode(encoding='utf-8')
            self.conn_soc.sendall(msg)

    def recvMsg(self):
        while True:

            msg = self.conn_soc.recv(1024).decode()
            print(msg)

            if len(msg) >= 100:
                obj = json.loads(msg)
                self.gui.obj = obj

                self.gui.allChat += obj['msg'] + '\n'

                self.gui.setWindow()

            

            else:
                if msg == "Server> ACCEPT END":
                    self.close()
                    break
                if msg == "ShutDown":
                    self.close_x()

                msg = msg + '\n'
                self.gui.allChat += msg
                self.gui.setChattingFrame()


    def run(self):
        self.conn()
        self.gui.setWindow()
        th2 = threading.Thread(target=self.recvMsg)
        th2.start()
        self.gui.window.protocol('WM_DELETE_WINDOW', self.close_x)
        self.gui.window.mainloop()


    def close(self):
        self.conn_soc.close()
        print("Termination")

    def close_x(self):
        msg = "/end"
        msg = msg.encode(encoding='utf-8')
        self.conn_soc.sendall(msg)
        self.gui.window.destroy()




gc = GameClient()
gc.run()