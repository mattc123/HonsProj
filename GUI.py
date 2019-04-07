from tkinter import *
from tkinter import scrolledtext
from scanner import main


class Butts:

    def __init__(self, master):


        frame = Frame(master)
        frame.grid()

       # self.tb = Text(frame)
        self.tb = scrolledtext.ScrolledText(frame, width=40, height=10)
		
		
        self.tb.grid(row=0, columnspan=3)


        self.printbutton = Button(frame, text="quit", command=frame.quit)
        self.printbutton.grid(row=1)
		
        self.quitbut = Button(frame, text="scan", command=self.scan)
        self.quitbut.grid(row=1, column =2)

        var = StringVar(master)
        var.set("environment")

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
            try:
                if n is None:  # The variable
                    print('It is None')
            except NameError:
                print("Please Select an enviroment")
            else:
                main(n)

root = Tk()
root.title("Drone Detection")
root.geometry("650x500")



b = Butts(root)

root.mainloop()