from tkinter import *

oldx=0
oldy=0
iter=0

class  application:
   
   def __init__(self, window):
      self.window = window
   
   def create(self):
      self.window.title("Application")      #titre de l'interface
      self.window.iconbitmap("ga2.ico")     #logo del'interface
      self.window.geometry("460x350")

   def create_canv(self):
        self.canvas= Canvas(self.window, background="white")
        self.canvas.create_text(50,10, text="Zone de graphe")
        self.canvas.place(x=0,y=0)
        self.ind=0
        self.donne=[]

   def nouveau(self):
      f= Tk()
      self.graphe = application(f)
      self.graphe.create()
      self.graphe.add_menu()
      self.graphe.create_canv()
      self.graphe.affichage()
   
   def vide(event):
      pass

   def ouvrir(self):
      file = askopenfile(title="Ouvrir un fichier",filetypes=[("fichier Python",".py")])

   def enregistrer_sous(self):
      sname = asksaveasfile(title="Enregistrer sous...", filetypes=[("fichier Python",".py")])

   def fermer(self):
      self.window.quit()

   def ajoute_point(self,event):
      self.canvas.focus_set()
      x = event.x 
      y = event.y
      self.canvas.create_oval(x-10, y-10, x+10, y+10)
      self.ind+=1
      self.canvas.create_text(x,y, text=str(self.ind))
      l=[str(self.ind),x,y]
      self.donne.append(l)

   def sommet(self):
      self.canvas.bind("<Button-1>", self.ajoute_point)

   def tracer(self, event):
      global iter
      global oldx,oldy
      if iter==0:
         oldx,oldy = event.x,event.y
         iter+=1
      else:
         x,y = event.x,event.y
         self.canvas.create_line(oldx, oldy, x, y)
         iter=0

   def arete(self):
      self.canvas.bind("<Button-1>", self.tracer)
      
   def cursor(self):
      self.canvas.bind("<Button-1>", self.vide)
      
   def add_menu(self):
        menu = Menu(self.window)
        fichier = Menu (menu, tearoff=0)
        fichier.add_command(label="Nouveau", command=self.nouveau)
        fichier.add_command(label="Ouvrir...", command=self.ouvrir)
        fichier.add_command(label="Enregistrer", command=self.vide)
        fichier.add_command(label="Enregistrer sous...", command=self.enregistrer_sous)
        fichier.add_separator()                                        #ligne de separation
        fichier.add_command(label="Fermer", command=self.fermer)
        creation = Menu (menu, tearoff=0)
        creation.add_command(label="Curseur", command=self.cursor)
        creation.add_command(label="Sommet", command=self.sommet)
        creation.add_command(label="Arete",command=self.arete)
        affichage = Menu (menu, tearoff=0)
        affichage.add_command(label="Graphe", command=self.vide)
        affichage.add_command(label="Chaines", command=self.vide)
        affichage.add_command(label="Matrice", command=self.vide)
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
   
   def affichage(self):
      self.window.mainloop()

f = Tk()
ap = application(f)
ap.create()
ap.add_menu()
ap.affichage()