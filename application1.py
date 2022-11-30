from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import json
import os

oldx=0
oldy=0
iter=0
l=[]

class  application:
   
   def __init__(self):
      self.window = Tk()
      self.savefile={1:""}
      self.file=None
   
   def personalise(self):
      self.window.title("Application")      #titre de l'interface
      self.window.iconbitmap("ga2.ico")     #logo de l'interface
      self.window.geometry("750x450")


   def nouveau(self):
      self.fram = Toplevel(self.window)
      self.fram.transient(self.window)
      self.fram.focus_set()
      self.fram.iconbitmap("ga2.ico")     
      self.fram.geometry("500x250")
      self.canvas= Canvas(self.fram, background="white")
      self.canvas.pack(side=TOP, fill=BOTH, expand=1)
      self.indice_sommet=0
      self.indice_arete=0
      self.list_sommet=[]
      self.list_arete=[]

   def get_sommet(self):
      l=[]
      A = self.list_sommet
      for i in A:
         l.append(int(i[0]))
      return l
   
   def get_arete(self):
      l=[]
      B = self.list_arete
      j=0
      for i in B:
         j+=1
         l.append(int(j))
      return l

   def voisin(self):
      A = self.list_sommet
      B =self.list_arete
      matrice={}
      for i in A:
         adjacence= []
         for j in A:
            for k in B:
               if i[0]==k[1] or j[0]==k[2]:
                  adja=1
               else:
                  adja=0
            adjacence.append(adja)
         matrice[int(i[0])]= tuple(self.voisin())
      return matrice


   def creer_matrice_ad(self):
      A = self.list_sommet
      matrice={}
      for i in A:
         adjacence= []
         
         matrice[int(i[0])]= tuple(self.voisin())
      return matrice
   
   def matrice_ad(self):
      popup = Toplevel(self.fram)
      popup.title("Matrice d'adjacence")
      popup.iconbitmap("ga2.ico")     
      popup.geometry("300x175")
      popup.transient(self.fram)
      matrice = self.voisin()
      list_sommet = self.get_sommet()
      for i in range(len(list_sommet)):
         list_sommet[i] = str(list_sommet[i])
      mat= ttk.Treeview(master=popup)
      mat['columns'] = tuple(list_sommet)
      mat.column("#0",width=30,minwidth=20)
      for i in range(len(list_sommet)):
         mat.column(list_sommet[i],width=30,minwidth=20)
      mat.heading("#0",text="  ")
      for i in range(len(list_sommet)):
         mat.heading(list_sommet[i],text=str(list_sommet[i]))
      list_sommet = self.get_sommet()
      for i in list_sommet:
         mat.insert(parent="",index="end",iid = i,text=str(i)+" ",values=matrice[i])
      mat.pack(expand=1, fill=BOTH)


   def creer_matrice_in(self):
      A = self.list_sommet
      B = self.list_arete
      matrice={}
      for i in A:
         incidence= []
         for j in B:
            if i[0]==j[1] or i[0]==j[2]:
               incid=1
            else:
               incid=0
            incidence.append(incid)
         matrice[int(i[0])]= tuple(incidence)
      return matrice
   
   def matrice_in(self):
      popup = Toplevel(self.fram)
      popup.title("Matrice d'incidence")
      popup.iconbitmap("ga2.ico")     
      popup.geometry("300x175")
      popup.transient(self.fram)
      matrice = self.creer_matrice_in()
      list_arete = self.get_arete()
      list_sommet = self.get_sommet()
      for i in range(len(list_sommet)):
         list_sommet[i] = str(list_sommet[i])
      mat= ttk.Treeview(master=popup)
      mat['columns'] = tuple(list_sommet)
      mat.column("#0",width=30,minwidth=20)
      for i in range(len(list_sommet)):
         mat.column(list_sommet[i],width=30,minwidth=20)
      mat.heading("#0",text="  ")
      for i in range(len(list_arete)):
         mat.heading(list_arete[i],text="e"+str(list_arete[i]))
      list_sommet = self.get_sommet()
      for i in list_sommet:
         mat.insert(parent="",index="end",iid = i,text=str(i)+" ",values=matrice[i])
      mat.pack(expand=1, fill=BOTH)
   

   def vide(event):
      pass

   def ouvrir(self):
      self.file = filedialog.askopenfilename(defaultextension=".json",
                                      filetypes=[("All Files","*.*"),
                                        ("Text Documents","*.txt"),
                                        ("Json","*.json")])

      if self.file == "":

         # no file to open
         self.file = None
      else:

         # Try to open the file
         # set the window title
         funcs = {
            'arc': self.canvas.create_arc,
            # 'bitmap' and 'image' are not supported
            # 'bitmap': self.c.create_bitmap,
            # 'image': self.c.create_image,
            'line': self.canvas.create_line,
            'oval': self.canvas.create_oval,
            'polygon': self.canvas.create_polygon,
            'rectangle': self.canvas.create_rectangle,
            'text': self.canvas.create_text,
            # 'window' is not supported
         }
         with open(self.file) as f:
            for line in f:
               item = json.loads(line)
               if item['type'] in funcs:
                  funcs[item['type']](item['coords'], **item['options'])

                         # __file.close()


   def enregistrer(self):
      if self.file is None:
            # Save as new file
            self.file = filedialog.asksaveasfilename(initialfile='Untitled.txt',
                                            defaultextension="*.json",
                                            filetypes=[("All Files","*.*"),
                                                ("Text Documents","*.json")])

            if self.file == "":
                self.file = None
            else:

                with open(self.file, 'w') as f:
                    for item in self.canvas.find_all():
                        print(json.dumps({
                            'type': self.canvas.type(item),
                            'coords': self.canvas.coords(item),
                            'options': {key: val[-1] for key, val in self.canvas.itemconfig(item).items()}
                        }), file=f)




   def enregistrer_sous(self):
      self.enregistrer()

   def fermer(self):
      self.window.quit()

   def ajoute_point(self,event):
      self.canvas.focus_set()
      x = event.x 
      y = event.y
      self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="black")
      self.indice_sommet+=1
      self.canvas.create_text(x,y, text=str(self.indice_sommet), fill="white")
      l=[str(self.indice_sommet),x,y]
      self.list_sommet.append(l)
      
   def sommet(self):
      self.canvas.bind("<Button-1>", self.ajoute_point)

   def tracer(self, event):
      global iter, l
      global oldx,oldy
      if iter==0:
         oldx,oldy = event.x,event.y
         for i in range(len(self.list_sommet)):
            osx=self.list_sommet[i][1]
            osy=self.list_sommet[i][2]
            if (oldx > osx-10) and (oldx < osx+10) and (oldy > osy-10) and (oldy < osy+10):
               oldx, oldy=self.list_sommet[i][1], self.list_sommet[i][2]
               l=self.list_sommet[i]
               iter+=1
      else:
         x,y = event.x,event.y
         for i in range(len(self.list_sommet)):
            sx=self.list_sommet[i][1]
            sy=self.list_sommet[i][2]
            if (x > sx-10) and (x < sx+10) and (y > sy-10) and (y < sy+10):
               x,y=self.list_sommet[i][1], self.list_sommet[i][2]
               self.canvas.create_line(oldx, oldy, x, y)
               center_x, center_y = ((oldx) + (x)) / 2, ((oldy + 15) + (y + 15)) / 2
               self.indice_arete+=1
               self.canvas.create_text(center_x, center_y, text="e"+str(self.indice_arete))
               
               list=["e"+str(self.indice_arete),l[0][0], self.list_sommet[i][0] ]
               self.list_arete.append(list)
               iter=0
               oldx=0
               oldy=0
               l=[]

   def arete(self):
      self.canvas.bind("<Button-1>", self.tracer)

   def add_menu(self):
        menu = Menu(self.window)
        fichier = Menu (menu, tearoff=0)
        fichier.add_command(label="Nouveau", command=self.nouveau)
        fichier.add_command(label="Ouvrir...", command=self.ouvrir)
        fichier.add_command(label="Enregistrer", command=self.enregistrer)
        fichier.add_command(label="Enregistrer sous...", command=self.enregistrer_sous)
        fichier.add_separator()                                        #ligne de separation
        fichier.add_command(label="Fermer", command=self.fermer)
        creation = Menu (menu, tearoff=0)
        creation.add_command(label="Sommet", command=self.sommet)
        creation.add_command(label="Arete",command=self.arete)
        affichage = Menu (menu, tearoff=0)
        affichage.add_command(label="Graphe", command=self.vide)
        affichage.add_command(label="Chaines", command=self.vide)

        matrice = Menu(affichage, tearoff=0)
        matrice.add_command(label="Matrice d'incidence", command=self.matrice_in)
        matrice.add_command(label="Matrice d'adjacence", command=self.matrice_ad)
        affichage.add_cascade(label="Matrice", menu=matrice)
        execution = Menu (menu, tearoff=0)
        execution.add_command(label="Plus court chemin", command=self.vide)
        execution.add_command(label="Coloration", command=self.vide)
        edition = Menu(menu, tearoff=0)
        edition.add_command(label="Graphe")

        menu.add_cascade(label="Fichier", menu=fichier)
        menu.add_cascade(label="Création", menu=creation) 
        menu.add_cascade(label="Affichage", menu=affichage)
        menu.add_cascade(label="Exécution", menu=execution)
        menu.add_cascade(label="Edition", menu=edition)
        self.window.config(menu = menu)

   def affiche(self):
      self.window.mainloop()
   

