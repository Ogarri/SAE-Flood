import modele_flood as mf
from vue_flood import Vue 
import tkinter as tk
class FloodControleur:

#Ci dessous, le code du controleur du jeu Flood. Il permet de gérer les actions de l'utilisateur et de les transmettre au modèle et à la vue.
    
    def __init__(self) -> None:
        """début du massacre
        """
        self.__modele = mf.Modele()
        self.__vue = Vue(self.__modele, self)
        
    def creer_controleur_bouton(self, i, j):
        def controleur_btn():
            """Méthode appelée lorsqu'un bouton à la position (i,j) est cliqué
            """
            self.__modele.empile_action()
            self.__modele.choisit_couleur(i, j)
            self.__vue.redessine()
        
        return controleur_btn
    
    def nouvelle_partie(self):
        """en gros ça fait ce que ça dit
        """
        self.__modele.reinitaliser()
        self.__vue.label_coups_max.config(text = f"Coups max: {self.__modele.get_coups_max}", fg="green")
        self.__vue.label_victoire.config(text = "")
        self.__vue.activer_boutons_grille()
        self.__vue.redessine()


    def nouvelle_partie_nouveau_modele(self, nb_lig, nb_col, nb_couleurs):
        """crée un nouveau modèle et redessine la vue
        """
        self.__modele = mf.Modele(nb_lig, nb_col, nb_couleurs)
        self.__vue.fermer()
        self.__vue = Vue(self.__modele, self)
        self.__vue.demarre()
    
    def undo(self):
        """annule la dernière action effectuée
        """
        action_precedente = self.__modele.get_action_precedente()
        if action_precedente != None:
            self.__modele.set_score(self.__modele.get_score - 1)
            self.__modele.set_cases(action_precedente)
            self.__vue.redessine()
        else:
            self.__vue.pop_up("Il n'y a plus d'action à annuler.")
    
    def demarre(self):
        """bref ça lance la vue
        """
        self.__vue.demarre()
        
        
        
    