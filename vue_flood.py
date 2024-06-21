import modele_flood as mf 
import tkinter as tk

class Vue:
    def __init__(self, modele: mf.Modele, controleur):
        #Initialisation des attributs
        self.__modele = modele
        #IMPORTATION DE FOU FURIEUX 
        #NE PAS TOUCHER SINON VOUS ALLEZ TOUT CASSER
        #QUAND JE DIS VOUS JE PARLE DE TOI BASTIEN
        from ctrl_flood import FloodControleur
        self.__ctrl = controleur
        self.__fenetre = tk.Tk()
        self.__fenetre.title(f"Projet Flood : {self.__modele.get_nb_lig}x{self.__modele.get_nb_col} - {self.__modele.get_nb_couleurs} couleurs")
        self.__fenetre.bind("<Control-n>", lambda event: self.__ctrl.nouvelle_partie())
        self.__fenetre.bind("<Control-u>", lambda event: controleur.undo())
        
        #Construction des éléments de la fenêtre
        #1) Grille
        self.Grille = tk.Frame(self.__fenetre)
        
        for i in range(self.__modele.get_nb_lig):
            for j in range(self.__modele.get_nb_col):
                couleur = self.__modele.get_couleurs[self.__modele.get_couleur_case(i, j)]
                b = tk.Button(self.Grille, width=6, height=3,bg = couleur, command=self.__ctrl.creer_controleur_bouton(i, j))
                b.grid(row = i, column = j)
                
        #2) Boutons et Labels
        self.Boutons = tk.Frame(self.__fenetre)
        self.bouton_jouer_12x12_6couleurs = tk.Button(self.Boutons, text = "12x12", command=lambda: self.__ctrl.nouvelle_partie_nouveau_modele(12, 12, 6))
        self.bouton_jouer_15x15_8couleurs = tk.Button(self.Boutons, text = "15x15", command=lambda: self.__ctrl.nouvelle_partie_nouveau_modele(15, 15, 8))
        self.bouton_joueur_6x6_4couleurs = tk.Button(self.Boutons, text = "6x6", command=lambda: self.__ctrl.nouvelle_partie_nouveau_modele(6, 6, 4))
        self.label_coups_max = tk.Label(self.Boutons, text = f"Coups max: {self.__modele.get_coups_max}", fg="green")
        self.label_victoire = tk.Label(self.Boutons, text = "", fg="green")
        self.label_score = tk.Label(self.Boutons, text = f"Score: {self.__modele.get_score}")
        self.undo = tk.Button(self.Boutons, text = "Undo", command = self.__ctrl.undo)
        self.recommencer = tk.Button(self.Boutons, text = "Nouveau", command = self.__ctrl.nouvelle_partie)
        self.quitter = tk.Button(self.Boutons, text = "Au revoir", command = self.__fenetre.destroy)

        #Positionnement des éléments
        self.bouton_jouer_12x12_6couleurs.grid(row = 1, column = 0)
        self.bouton_jouer_15x15_8couleurs.grid(row = 2, column = 0)
        self.bouton_joueur_6x6_4couleurs.grid(row = 3, column = 0)
        self.label_coups_max.grid(row = 4, column = 0)
        self.label_victoire.grid(row = 5, column = 0)
        self.label_score.grid(row = 6, column = 0)
        self.undo.grid(row = 7, column = 0)
        self.recommencer.grid(row = 8, column = 0)
        self.quitter.grid(row = 9, column = 0)
        
        #Positionnement des Frames
        self.Grille.grid(row = 0, column = 0)
        self.Boutons.grid(row = 0, column = 1)

    def set_modele(self, modele):
        """Change le modèle de la vue."""
        self.__modele = modele

    def fermer(self):
        """Ferme la fenêtre. Utilisé dans le contrôleur pour changer de modèle et refresh la vue."""
        self.__fenetre.destroy()
    
    def pop_up(self, message):
        """Affiche une fenêtre pop-up avec le message donné."""
        popup = tk.Tk()
        popup.wm_title("Information")
        label = tk.Label(popup, text=message)
        label.pack(side="top", fill="x", pady=10)
        bouton = tk.Button(popup, text="Fermer", command=popup.destroy)
        bouton.pack()
        popup.mainloop()
        
    def desactiver_boutons_grille(self):
        """Désactive tous les boutons de la grille."""
        for i in range(self.__modele.get_nb_lig):
            for j in range(self.__modele.get_nb_col):
                button = self.Grille.grid_slaves(row=i, column=j)[0]
                button.configure(state="disabled")

        #désactiver le bouton undo
        self.undo.configure(state="disabled")

    def activer_boutons_grille(self):
        """Active tous les boutons de la grille."""
        for i in range(self.__modele.get_nb_lig):
            for j in range(self.__modele.get_nb_col):
                button = self.Grille.grid_slaves(row=i, column=j)[0]
                button.configure(state="normal")

        #activer le bouton undo
        self.undo.configure(state="normal")
                
    def redessine(self):
        """redessine tous les boutons en cohérence avec le modèle
        """
        for i in range(self.__modele.get_nb_lig):
            for j in range(self.__modele.get_nb_col):
                couleur = self.__modele.get_couleurs[self.__modele.get_couleur_case(i, j)]
                button = self.Grille.grid_slaves(row=i, column=j)[0]
                button.configure(bg=couleur)
            
        self.label_score.config(text=f"Score: {self.__modele.get_score}")

        if self.__modele.get_score == self.__modele.get_coups_max:
            self.label_score.config(fg="red")
        
        if self.__modele.partie_finie():
            if self.__modele.get_score >= self.__modele.get_coups_max:
                self.label_victoire.config(text="Partie finie !\nMais vous avez\ndépassé le score...")
            else:
                self.label_victoire.config(text="Partie finie !\nVous avez gagné !")
            self.desactiver_boutons_grille()
        
    def demarre(self):
        """lance la boucle principale de la fenêtre
        """
        self.__fenetre.mainloop()
        
