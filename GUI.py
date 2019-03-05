from tkinter import *
from scanner import main


class GUI:

    def __init__(self, master):


        frame = Frame(master)
        frame.grid()

        self.tb = Text(frame)
        self.tb.grid(row=0, columnspan=3)


        self.printbutton = Button(frame, text="quit", command=frame.quit)
        self.printbutton.grid(row=1)
        self.quitbut = Button(frame, text="scan", command=self.scan)
        self.quitbut.grid(row=1, column =2)

        var = StringVar(master)
        var.set("Outdoors")

        self.envmenu = OptionMenu(frame, var, "Outdoors", "Indoors", "Built up area", command=self.val)
        self.envmenu.grid(row=2, column=2)



    def val (self, val):

        global n #temporary solution
        if (val == "Outdoors"):
            n = 20
        elif (val == "Indoors"):
            n = 30
        else:
            n = 40

    def scan(self):
        pass
        main(n)


root = Tk()
root.title("Drone Detection")
root.geometry("650x500")



b = GUI(root)

root.mainloop()