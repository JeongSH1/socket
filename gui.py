# from tkinter import *

# window = Tk()
# window.title("Hang-Man Reviewer")
# window.geometry("640x400+100+100")
# window.resizable(False, False)

# canvas = Canvas(window, width=250, height=350, relief='solid', bd=1)
# line = canvas.create_line(125, 10, 125, 75)
# head = canvas.create_oval(85, 75, 165, 155)
# body = canvas.create_line(125, 155, 125, 270)
# arm1 = canvas.create_line(50, 120, 125, 200)
# arm2 = canvas.create_line(200, 120, 125, 200)
# leg1 = canvas.create_line(125,270, 80, 330)
# leg2 = canvas.create_line(125,270, 170, 330)
# canvas.place(x=30, y=10)


# alphaFrame = LabelFrame(window, text = "Alphabet", width=300, height=100)
# alphaFrame.place(x=300, y=10)
# alphabets = [['Aa',False],['Bb',True],['Cc',True],['Dd',True],['Ee',True],['Ff',True],['Gg',True],['Hh',True],['Ii',True],['Jj',True],['Kk',True],['Ll',True],['Mm',True],['Nn',True],['Oo',True],['Pp',True],['Qq',True],['Rr',True],['Ss',True],['Tt',True],['Uu',True],['Vv',True],['Ww',True],['Xx',True],['Yy',True],['Zz',True]]
# alphabets_label = [None for _ in range(26)]

# for i in range(26):
#     alphabets_label = Label(alphaFrame, text=alphabets[i][0], width=2, height=1, fg='black')
#     if not alphabets[i][1]:
#         alphabets_label['fg'] = 'white'
#     alphabets_label.grid(row=i//12, column=i%12)


# hintFrame = LabelFrame(window, text='Hint', width=300, height=70)
# hintFrame.place(x=300, y=120)

# answerFrame = LabelFrame(window, text='Answer', width=300, height = 70)
# answerFrame.place(x=300, y=230)

# connected = Label(window, text='Connected: None')
# connected.place(x=300, y=320)


# input = Entry(window, width=10)
# input.place(x=350, y=350)
# inputBtn = Button(window, text='enter')
# inputBtn.place(x=450, y=350)

# window.mainloop()
