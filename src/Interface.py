#coding:utf-8


from Tkinter import *
from PIL import Image, ImageTk
import Tkinter
import tkMessageBox
from tkFileDialog import askopenfilename

class Interface(Frame):


    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=1000, height=1800, **kwargs)
        self.filePath = None
        self.visu = True
        self.pack(fill=BOTH)
        self.argument = None
        # background image
        img = ImageTk.PhotoImage(file="./data/RIPE_NCC_logo.png")
        panel = Label(self, image = img, bd=10)
        panel.image = img
        panel.pack(fill = "both", expand = "yes")
        #~ print im
        #~ tkimage = ImageTk.PhotoImage(im)
        #~ Tkinter.Label(self,image = tkimage).pack()
        #~ background_image = Tkinter.PhotoImage("./RIPE_NCC_logo.png") 
        #~ background_label = Tkinter.Label(self, image=background_image) 
        #~ background_label.place(x=0, y=0, relwidth=1, relheight=1)
        #~ background_label.pack()
        
        # Création de nos widgets
        self.message = Label(self,width=50,
        text="Please enter a number of probes",
        font=("Arial",20), bd=10)
        self.message.pack()
        
        self.var_text1 = StringVar()
        ligne_text1 = Entry(self, textvariable=self.var_text1, width=30,font=("Arial",20))
        ligne_text1.pack()
        
        self.warning1 = Label(self,width=50, text="Number between 2 and 35", fg="red",bd=10)
        self.warning1.pack()
        
        self.message2 = Label(self, width=50,
        text="Or a list separated by coma",
        font=("Arial",20), bd=10)
        self.message2.pack()
        
        self.var_text2 = StringVar()
        ligne_text2 = Entry(self, textvariable=self.var_text2, width=30,font=("Arial",20))
        ligne_text2.pack()
        
        self.warning2 = Label(self,width=50, text="List like id1,id2,id3...", fg="red", bd=10)
        self.warning2.pack()
        
        self.bouton_quitter = Button(self, text="Quit (q)",font=("Arial",10),command=self.quit)
        self.bouton_quitter.pack(side="right",padx = 5, pady = 40)
        
        self.bouton_envoyer = Button(self, text="Launch measure", fg="black",font=("Arial",10),
                command=self.envoyer)
        self.bouton_envoyer.pack(side="right",padx = 5, pady = 40)
        self.message3 = Label(self,
                              #width=25,
                              text="Open an existing file:",
                              fg="black",
                              font=("Arial",10),
                              bd=10)
        self.message3.pack(side="left")
        self.bouton_upload = Button(self, text="Upload (u)", fg="black",font=("Arial",10),
                                    command=self.upload)
        self.bouton_upload.pack(side="left",padx=5,pady=40)
        self.v = StringVar()
        self.v.set("None")
        self.message4 = Label(self,textvariable=self.v, font=("Arial",10),bd=10)
        self.message4.pack(side="left")
        fenetre.bind("<Return>", self.envoyer)
        fenetre.bind("q", self.exit)
        fenetre.bind("u", self.upload)
    
    def envoyer(self, event=None):
		text1 = self.var_text1.get()
		text2 = self.var_text2.get()
		
		if text1 != "":
			if re.match("[2-9]|[0-9][0-9]+", text1) and int(text1)<36 and int(text1)>1:
			    if self.filePath == None:
				print "Send a measure for %d probes"%(int(text1))
				self.argument = int(text1)
				self.quit()
			    else:
				print "Send calculation for %d probes from %s"%(int(text1),self.filePath)
				self.argument = int(text1)
				self.quit()
			else:
				tkMessageBox.showwarning(message="Please enter a number between 2 and 35 probes")
		elif text2 != "":
			if re.match("([0-9]*,)*", text2) and len(text2.split(","))>1:
				print "Send a measure for %s"%text2
				self.argument = text2
				self.quit()
			else:
				tkMessageBox.showwarning(message="Please enter a list of at list 2 probes")
		else:
			tkMessageBox.showwarning(message="Please fill one field")
    
    def upload(self, event=None):
	filePath = askopenfilename()
	self.v.set("%s" %filePath)
	self.filePath = filePath
    
    def exit(self, event=None):
	self.quit()
