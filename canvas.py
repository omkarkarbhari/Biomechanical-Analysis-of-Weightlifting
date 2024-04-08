

from tkinter import *
import tkinter as tk
import os 
from PIL import Image
from PIL import Image, ImageTk
import datasen
op=[]
files=''
pl=[]
def setop(op):
  global files
  files=op
  with open('temp.txt') as file:
    for i in files:
      print(i)
  print('temp set')
def insertfiles():
    curr=os.getcwd()
    global lst
    for filename in os.listdir(curr+'/frames'):
        print(filename)
        # im=cv2.imread(curr+'\\frames\\'+filename)
        # cv2.imshow('check',im)

        lst.insert(tk.END, curr+'/frames/'+filename)
 
def showimg(event):
    n = lst.curselection()
    filen = lst.get(n)
    img_path = os.path.join(os.getcwd(), 'frames', filen)
    img = Image.open(img_path)
    img = img.resize((700, 700))  # Resize if necessary
    img_tk = ImageTk.PhotoImage(img)
    
    canvas.image = img_tk  # Storing the image to prevent it from being garbage-collected
    canvas.config(width= 700, height=700)
    canvas.create_image(0, 0, image=img_tk, anchor=tk.NW)

    # Assuming datasen.datalist() is a function to extract data from the image
    pl = datasen.datalist(filen, os.getcwd()+'/frames')
    print("pl",pl)
    #pl=[73, 57, 125, 116, 90, 79, 115, 101, 123, 98, 114, 103, 30, 36, 148, 173, 77, 115, 134, 131, 173, 174, 2]
    if len(pl) ==6:
      pl+=[0,0,0,0]
      
    elif len(pl)==4:
      pl=[0,0,0,0,0,0]+pl
    print(pl)
    kr.set(pl[0])
    kl.set(pl[1])
    ar.set(pl[2])
    al.set(pl[3])
    hr.set(pl[4])
    hl.set(pl[5])
    sr.set(pl[6])
    sl.set(pl[7])
    er.set(pl[8])
    el.set(pl[9])

    print('-----------------------------\n',hl,'\n--------------------')
    img = tk.PhotoImage(file=filen)
    #img.resize((800,700))
    w, h = 900,900#img.width(), img.height()
    #print(type(img))
    #img.zoom(3,4)
    canvas.image = img
    canvas.config(width=w, height=h)
    canvas.create_image(0, 0, image=img, anchor=tk.NW)

def selected_item():
  global listbox
	# Traverse the tuple returned by
	# curselection method and print
	# corresponding value(s) in the listbox
  for i in listbox.curselection():
    #print(listbox.get(i))
    op.append(listbox.get(i))
  with open('temp.txt','w') as file:
    for i in op: 
      file.write(os.getcwd()+'\\frames\\'+i)
      file.write('\n')
def getop():
  global op
  return op

root = tk.Tk()
root.geometry("800x700+300+50")
root.state('zoomed')
root.config(background='#28282F')
l1=Label(root,text="Extracted Images",width=20,height=3,font=('Ariel',15)).place(x=0,y=0)
lst = tk.Listbox(root,height=16,width=40)
#lst.grid(row=0,column=0)
#lst.pack(side='left',expand=1)
lst.place(x=0,y=50)
l2=Label(root,text="Select Images",width=20,height=3,font=('Ariel',15)).place(x=0,y=350)
lst.bind("<<ListboxSelect>>", showimg)
listbox = Listbox(root, width=40, height=16, selectmode=MULTIPLE)
cnt=1
lst.select_set(1)
# Inserting the listbox items
for filename in os.listdir(r'./frames'):
  listbox.insert(cnt, filename)
  cnt+=1
# listbox.insert(2, "Algorithm")
# listbox.insert(3, "Data Science")
# listbox.insert(4, "Machine Learning")
# listbox.insert(5, "Blockchain")
btn = Button(root, text='Print Selected', command=selected_item)

# Placing the button and listbox
btn.pack(side='bottom')
listbox.place(x=0,y=400)
insertfiles()
hl=IntVar(root,value=0)
hr=IntVar(root,value=0)
kl=IntVar(root,value=0)
kr=IntVar(root,value=0)
al=IntVar(root,value=0)
ar=IntVar(root,value=0)
sl=IntVar(root,value=0)
sr=IntVar(root,value=0)
el=IntVar(root,value=0)
er=IntVar(root,value=0)
canvas = tk.Canvas(root)

knee=Label(root,text="Knee",width=20,height=3,font=('Ariel',15)).place(x=1250,y=5)
kneel=Label(root,textvariable_=str(kl),font=('Ariel',15)).place(x=1300,y=100)
kneer=Label(root,textvariable_=str(kr),font=('Ariel',15)).place(x=1400,y=100)
ankle=Label(root,text="Ankle",width=20,height=3,font=('Ariel',15)).place(x=1250,y=155)
anklel=Label(root,textvariable_=str(al),font=('Ariel',15)).place(x=1300,y=250)
ankler=Label(root,textvariable_=str(ar),font=('Ariel',15)).place(x=1400,y=250)
hip=Label(root,text="Hip",width=20,height=3,font=('Ariel',15)).place(x=1250,y=305)
hipl=Label(root,textvariable_=str(hl),font=('Ariel',15)).place(x=1300,y=400)
hipr=Label(root,textvariable_=str(hr),font=('Ariel',15)).place(x=1400,y=400)
shoulder=Label(root,text="Shoulder",width=20,height=3,font=('Ariel',15)).place(x=1250,y=455)
shoulderl=Label(root,textvariable_=str(sl),font=('Ariel',15)).place(x=1300,y=550)
shoulderr=Label(root,textvariable_=str(sr),font=('Ariel',15)).place(x=1400,y=550)
elbow=Label(root,text="Elbow",width=20,height=3,font=('Ariel',15)).place(x=1250,y=605)
elbowl=Label(root,textvariable_=str(el),font=('Ariel',15)).place(x=1300,y=700)
elbowr=Label(root,textvariable_=str(er),font=('Ariel',15)).place(x=1400,y=700)
canvas.pack()




root.mainloop()

