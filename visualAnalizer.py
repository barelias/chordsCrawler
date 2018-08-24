from tkinter import *

class Aplication:
    def __init__ (self, master=None):
        
        # Definindo o container geral
        self.container1 = Frame(master)
        self.container1.pack()
        self.container1["padx"] = 100
        # Definindo o container do emulador de terminal
        self.container2 = Frame(self.container1)
        self.container2.pack( side = RIGHT )
        # Definindo o container da janela de selecao
        self.container3 = Frame( self.container1)
        self.container3.pack( side = LEFT )

        self.terminal = Frame( self.container2 )
        self.terminal.pack()
        self.tmsg = Label(self.terminal, text="TERMINAL")
        self.tmsg.pack()
        self.name = Frame( self.container3 )
        self.name.pack()
        self.msg = Label(self.name, text="CHORDS ANALIZER")
        self.msg.pack()
        self.sair = Button(self.container3)
        self.sair["text"] = "SAIR"
        self.sair["width"] = 5
        self.sair["command"] = self.container1.quit
        self.sair.pack( side = TOP )
        pass
root = Tk()
Aplication(root)
root.mainloop()