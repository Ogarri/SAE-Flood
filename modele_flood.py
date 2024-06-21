import random 
from copy import deepcopy

class Modele:
    def __init__(self, nb_lig=6, nb_col=6, nb_couleurs=4):
        self.__nb_lig = nb_lig
        self.__nb_couleurs = nb_couleurs
        self.__nb_col = nb_col
        self.__score = 0
        self.__couleurs = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(self.__nb_couleurs)]  
        self.__cases = [[Case(i, j, random.randint(0, self.__nb_couleurs-1), False) for j in range(self.__nb_lig)] for i in range(self.__nb_col)]
        self.__coups_a_jouer = self.nombre_coups_max()
        self.__pile_actions = Pile()
        print(self.__couleurs)

    """getters
    """
    @property
    def get_coups_max(self) -> int:
        return self.__coups_a_jouer
    
    @property
    def get_couleurs(self) -> list:
        return self.__couleurs
    
    @property
    def get_score(self) -> int:
        return self.__score
    
    @property
    def get_couleur(self, i, j) -> int:
        return self.__cases[i][j].get_couleur
    
    @property
    def get_nb_lig(self) -> int:
        return self.__nb_lig
    
    @property
    def get_nb_col(self) -> int:
        return self.__nb_col
    
    @property
    def get_nb_couleurs(self) -> int:
        return self.__nb_couleurs
    
    def get_couleur_case(self, i, j) -> int:
        return self.__cases[i][j].get_couleur
    
    def get_action_precedente(self):
        return self.__pile_actions.depile()
    
    """setters
    """

    def set_cases(self, cases):
        self.__cases = cases

    def set_score(self, score):
        self.__score = score
    
    """les fonctions
    """ 

    def empile_action(self):
        self.__pile_actions.empile(deepcopy(self.__cases))

    def nombre_coups_max(self, nb_tests=100) -> int:
        """Retourne le nombre minimum de coups pour terminer la partie en moyenne sur un échantillon de nb_tests parties.
        """
        min_coups = float('inf')  

        for _ in range(nb_tests):
            modele_test = deepcopy(self)
            coups = 0

            while not modele_test.partie_finie():
                couleur_ref = modele_test.get_couleur_case(0, 0)
                connected_cells = modele_test.compte_base(0, 0, couleur_ref, set())
                couleur_choisie = random.randint(0, self.get_nb_couleurs - 1)
                modele_test.pose_couleur(couleur_choisie)
                coups += 1

            min_coups = min(min_coups, coups)

        return min_coups

    def compte_base(self, i, j, couleur_ref, visited) -> int:
        """Compte le nombre de cellules dans la zone connexe à la case (i, j) de même couleur que celle de référence.
        """
        if i < 0 or i >= self.get_nb_lig or j < 0 or j >= self.get_nb_col:
            return 0
        if (i, j) in visited or self.get_couleur_case(i, j) != couleur_ref:
            return 0

        visited.add((i, j))
        count = 1

        for (i2, j2) in self.voisines(i, j):
            count += self.compte_base(i2, j2, couleur_ref, visited)

        return count
    
    def choisit_couleur(self, i, j) -> None:
        """choisit la couleur de la case (i, j) et met a jour le score
        """
        couleur = self.__cases[i][j].get_couleur
        self.pose_couleur(couleur)
        self.__score += 1
                    
    def voisines(self, i, j) -> list:
        return self.__cases[i][j].voisines(self)
    
    def pose_couleur(self, couleur: int) -> None:
        """
        Prend un numéro de couleur en paramètre et diffuse cette couleur à partir du carré en haut à gauche.
        """
        self.diffuse_couleur(0, 0, self.__cases[0][0].get_couleur, couleur)

    def diffuse_couleur(self, i: int, j: int, couleur_orig: int, couleur_nouv: int) -> None:
        """
        Diffuse la couleur spécifiée à partir de la case (i, j) dans la matrice.
        """
        if i < 0 or i >= self.__nb_lig or j < 0 or j >= self.__nb_col:
            return
        if self.__cases[i][j].get_couleur != couleur_orig:
            return
        if self.__cases[i][j].get_couleur == couleur_nouv:
            return
        self.__cases[i][j].changer_couleur_case(couleur_nouv)
        for (i2, j2) in self.voisines(i, j):
            self.diffuse_couleur(i2, j2, couleur_orig, couleur_nouv)
                
    def reinitaliser(self) -> None:
        """reinitialise la matrice et le score"""
        self.__score = 0
        self.__couleurs = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(self.__nb_couleurs)]
        self.__pile_actions = Pile()
        self.__cases = [[Case(i, j, random.randint(0, self.__nb_couleurs-1), False) for j in range(self.__nb_lig)] for i in range(self.__nb_col)]
        self.__coups_a_jouer = self.nombre_coups_max()
        
    def num_col(self) -> str:
        """retourne le numero des colonnes dans l'affichage de la matrice
        """
        text = "   |"
        for i in range(self.__nb_col):
            text += f"{i:2} |"  
        return text
        
    def __str__(self) -> str:
        """retourne l'affichage de la matrice en mode console
        """
        res = ""
        res += self.num_col() + "\n"
        res += "-" * ((self.__nb_col+1) * 4) + "\n"
        for i in range(self.__nb_lig):
            res += f"{i:2} |"
            for j in range(self.__nb_col):
                res += f"{self.__cases[i][j].get_couleur:2} |"
            res += "\n"
            res += "-" * ((self.__nb_col+1) * 4) + "\n"
            
        return res
    
    def partie_finie(self):
        """retourne True si la partie est finie, False sinon
        """
        #si toutes les cases ont la même couleur alors la partie est finie
        couleur = self.__cases[0][0].get_couleur
        for i in range(self.__nb_lig):
            for j in range(self.__nb_col):
                if self.__cases[i][j].get_couleur != couleur:
                    return False
        return True
    
class Case:
    def __init__(self, i :int, j :int, couleur :int, touche :bool):
        self.__i = i
        self.__j = j
        self.__couleur = couleur
        
        #si la case est touchee par celle en haut a gauche
        self.__touche = touche
        
    @property
    def get_i(self) -> int:
        return self.__i
    
    @property
    def get_j(self) -> int:
        return self.__j
    
    @property
    def get_couleur(self) -> int:
        return self.__couleur
    
    @property
    def est_touche(self) -> bool:
        return self.__touche
    
    def voisines(self, modele :Modele) -> list:
        """
        retourne la liste des coordonnées des cases voisines 
        (donc soit une liste de deux couples de coordonnées si la case est dans un coin, 
        de trois couples si la case est sur un bord,
        ou de quatre couples dans les autres cas)
        """
        res = []
        if self.__i > 0:
            res.append((self.__i-1, self.__j))
        if self.__j > 0:
            res.append((self.__i, self.__j-1))
        if self.__i < modele.get_nb_lig-1:
            res.append((self.__i+1, self.__j))
        if self.__j < modele.get_nb_col-1: 
            res.append((self.__i, self.__j+1))
        return res
    
    def changer_couleur_case(self, couleur :int) -> None:
        """change la couleur de la case
        """
        self.__couleur = couleur
    
    def changer_touche(self, touche :bool) -> None:
        """change l'etat de la case
        """
        self.__touche = touche


class Pile:
    def __init__(self):
        self.__pile = []
        
    def empile(self, element):
        self.__pile.append(element)
        
    def depile(self):
        if not self.est_vide():
            return self.__pile.pop()
        return None
    
    def est_vide(self):
        return len(self.__pile) == 0
        
