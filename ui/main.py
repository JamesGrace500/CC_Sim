from tkinter import *
import sqlite3


class Main(object):
    def __init__(self,master):
        self.master = master


#frames
        mainFrame=Frame(self.master)
        mainFrame.pack()
        #top frames
        topFrame= Frame(mainFrame,width=1350,height=70,bg='#f8f8f8',padx=20,relief=SUNKEN,borderwidth=2)
        topFrame.pack(side=TOP,fill=X)
        #center frame
        centerFrame = Frame(mainFrame,width=1350,relief=RIDGE,bg='#e0f0f0',height=680)
        centerFrame.pack(side=TOP)
        #Center Left Frame
        centerLeftFrame= Frame(centerFrame,width=900,height=700,bg='#e0f0f0',borderwidth=2,relief='sunken')
        centerLeftFrame.pack(side=LEFT)
        #center right frame
        centerRightFrame= Frame(centerFrame,width=450,height=700,bg='#e0f0f0',borderwidth=2,relief='sunken')
        centerRightFrame.pack()

        #search bar
        search_bar =LabelFrame(centerRightFrame,width=440,height=75,text='Simulation Output',bg='#9bc9ff')
        search_bar.pack(fill=BOTH)


        self.btnbook= Button(topFrame,text='Add Book',compound=LEFT,
                                    font='arial 12 bold')
        self.btnbook.pack(side=LEFT,padx=10)
        #add member button
        self.btnmember=Button(topFrame,text='Add Member',font='arial 12 bold',padx=10)
        self.btnmember.configure(compound=LEFT)
        self.btnmember.pack(side=LEFT)
        #give book
        self.btngive=Button(topFrame,text='Give Book',font='arial 12 bold',padx=10,
                            compound=LEFT)
        self.btngive.pack(side=LEFT)

def main():
    root = Tk()
    app = Main(root)
    root.title("CC Sim v1")
    root.geometry("1350x750+350+200")
    root.mainloop()

if __name__ == '__main__':
    main()