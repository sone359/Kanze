# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 09:03:50 2020

@author: Simon Biffe
"""

import os
import tkinter as tk
import tkinter.filedialog as filedialog
import time
import copy
import random

class InfosDePartie:
    """
    Classe gérant l'accès et les modifications des données de jeu. Il contient
    des méthodes permettant l'accès aux attributs, la manipulation de
    sauvegarde et le jeu d'une action d'un joueur.
    """
    def __init__(self, nouvellePartie:bool=True, nombreDeTroupesMax:int=49, casesNeutresNonAdjacentes:bool=True, casesAdversesNonAdjacentes:bool=False, caseDepartJ1:tuple=(13, 1), caseDepartJ2:tuple=(1, 1)):
        """
        Constructeur créant pour une nouvelle partie une liste (_infos)
        destiné à contenir toutes les informations internes sur le jeu et
        initialisant une variable (tour) servant de compteur de tour.

        Parameters
        ----------
        nouvellePartie : bool, optional
            Si ce paramètre est vrai, l'attribut _infos est créé comme vierge.
            Sinon, une sauvegarde est importée.
            The default is True.
        nombreDeTroupesMax : int, optional
            Nombre de troupes maximales de chaque joueur, il peut seulement
            être dépassé grâce à l'influence.
            The default is 49.
        casesNeutresNonAdjacentes : bool, optional
            Si ce paramètre est vrai, un joueur peut déplacer des troupes sur
            une case neutre non-adjacente à la case de départ tant que les
            deux cases sont reliées par des cases du joueur.
            The default is True.
        casesAdversesNonAdjacentes : bool, optional
            Si ce paramètre est vrai, un joueur peut déplacer des troupes sur
            une case adverse non-adjacente à la case de départ tant que les
            deux cases sont reliées par des cases du joueur.
            The default is False.
        caseDepartJ1 : tuple, optional
            Case de départ du joueur 1, où sont positionnées au début de la
            partie 7 de ses troupes et son Représentant.
        caseDepartJ2 : tuple, optional
            Case de départ du joueur 2, où sont positionnées au début de la
            partie 7 de ses troupes et son Représentant.

        Returns
        -------
        None.

        """
        if nouvellePartie == True:
                          # Indication de fin de partie (0 si elle est en cours, 1 si le joueur 1 a gagné, 2 si c'est le joueur 2, 3 si la partie est nulle)
            self._infos = [{"indicationPartie":0, "nombreDeTroupesMax":nombreDeTroupesMax, "casesNeutresNonAdjacentes":casesNeutresNonAdjacentes, "casesAdversesNonAdjacentes":casesAdversesNonAdjacentes},
                          # 1er tour (indice 1 de la liste)
                           {('nombreTroupes', 'Joueur 1'): 7,
                            ('nombreTroupes', 'Joueur 2'): 7,
                            ('nombreCases', 'Joueur 1') : 1,
                            ('nombreCases', 'Joueur 2') : 1,
                            "action": None,
                            (1, 1): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [150, 0, 200, 50], 'Representant': True, 'CasesAdjacentes': [(2, 1), (2, 2)]},
                            (2, 1): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [125, 50, 175, 100], 'Representant': False, 'CasesAdjacentes': [(1, 1), (2, 2), (3, 1), (3, 2)]},
                            (2, 2): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [175, 50, 225, 100], 'Representant': False, 'CasesAdjacentes': [(1, 1), (2, 1), (3, 2), (3, 3)]},
                            (3, 1): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [100, 100, 150, 150], 'Representant': False, 'CasesAdjacentes': [(2, 1), (3, 2), (4, 1), (4, 2)]},
                            (3, 2): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [150, 100, 200, 150], 'Representant': False, 'CasesAdjacentes': [(2, 1), (2, 2), (3, 1), (3, 3), (4, 2), (4, 3)]},
                            (3, 3): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [200, 100, 250, 150], 'Representant': False, 'CasesAdjacentes': [(2, 2), (3, 2), (4, 3), (4, 4)]},
                            (4, 1): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [75, 150, 125, 200], 'Representant': False, 'CasesAdjacentes': [(3, 1), (4, 2), (5, 1), (5, 2)]},
                            (4, 2): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [125, 150, 175, 200], 'Representant': False, 'CasesAdjacentes': [(3, 1), (3, 2), (4, 1), (4, 3), (5, 2), (5, 3)]},
                            (4, 3): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [175, 150, 225, 200], 'Representant': False, 'CasesAdjacentes': [(3, 2), (3, 3), (4, 2), (4, 4), (5, 3), (5, 4)]},
                            (4, 4): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [225, 150, 275, 200], 'Representant': False, 'CasesAdjacentes': [(3, 3), (4, 3), (5, 4), (5, 5)]},
                            (5, 1): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [50, 200, 100, 250], 'Representant': False, 'CasesAdjacentes': [(4, 1), (5, 2), (6, 1), (6, 2)]},
                            (5, 2): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [100, 200, 150, 250], 'Representant': False, 'CasesAdjacentes': [(4, 1), (4, 2), (5, 1), (5, 3), (6, 2), (6, 3)]},
                            (5, 3): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [150, 200, 200, 250], 'Representant': False, 'CasesAdjacentes': [(4, 2), (4, 3), (5, 2), (5, 4), (6, 3), (6, 4)]},
                            (5, 4): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [200, 200, 250, 250], 'Representant': False, 'CasesAdjacentes': [(4, 3), (4, 4), (5, 3), (5, 5), (6, 4), (6, 5)]},
                            (5, 5): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [250, 200, 300, 250], 'Representant': False, 'CasesAdjacentes': [(4, 4), (5, 4), (6, 5), (6, 6)]},
                            (6, 1): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [25, 250, 75, 300], 'Representant': False, 'CasesAdjacentes': [(5, 1), (6, 2), (7, 1), (7, 2)]},
                            (6, 2): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [75, 250, 125, 300], 'Representant': False, 'CasesAdjacentes': [(5, 1), (5, 2), (6, 1), (6, 3), (7, 2), (7, 3)]},
                            (6, 3): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [125, 250, 175, 300], 'Representant': False, 'CasesAdjacentes': [(5, 2), (5, 3), (6, 2), (6, 4), (7, 3), (7, 4)]},
                            (6, 4): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [175, 250, 225, 300], 'Representant': False, 'CasesAdjacentes': [(5, 3), (5, 4), (6, 3), (6, 5), (7, 4), (7, 5)]},
                            (6, 5): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [225, 250, 275, 300], 'Representant': False, 'CasesAdjacentes': [(5, 4), (5, 5), (6, 4), (6, 6), (7, 5), (7, 6)]},
                            (6, 6): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [275, 250, 325, 300], 'Representant': False, 'CasesAdjacentes': [(5, 5), (6, 5), (7, 6), (7, 7)]},
                            (7, 1): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [0, 300, 50, 350], 'Representant': False, 'CasesAdjacentes': [(6, 1), (7, 2), (8, 1)]},
                            (7, 2): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [50, 300, 100, 350], 'Representant': False, 'CasesAdjacentes': [(6, 1), (6, 2), (7, 1), (7, 3), (8, 1), (8, 2)]},
                            (7, 3): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [100, 300, 150, 350], 'Representant': False, 'CasesAdjacentes': [(6, 2), (6, 3), (7, 2), (7, 4), (8, 2), (8, 3)]},
                            (7, 4): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [150, 300, 200, 350], 'Representant': False, 'CasesAdjacentes': [(6, 3), (6, 4), (7, 3), (7, 5), (8, 3), (8, 4)]},
                            (7, 5): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [200, 300, 250, 350], 'Representant': False, 'CasesAdjacentes': [(6, 4), (6, 5), (7, 4), (7, 6), (8, 4), (8, 5)]},
                            (7, 6): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [250, 300, 300, 350], 'Representant': False, 'CasesAdjacentes': [(6, 5), (6, 6), (7, 5), (7, 7), (8, 5), (8, 6)]},
                            (7, 7): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [300, 300, 350, 350], 'Representant': False, 'CasesAdjacentes': [(6, 6), (7, 6), (8, 6)]},
                            (8, 1): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [25, 350, 75, 400], 'Representant': False, 'CasesAdjacentes': [(7, 1), (7, 2), (8, 2), (9, 1)]},
                            (8, 2): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [75, 350, 125, 400], 'Representant': False, 'CasesAdjacentes': [(7, 2), (7, 3), (8, 1), (8, 3), (9, 1), (9, 2)]},
                            (8, 3): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [125, 350, 175, 400], 'Representant': False, 'CasesAdjacentes': [(7, 3), (7, 4), (8, 2), (8, 4), (9, 2), (9, 3)]},
                            (8, 4): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [175, 350, 225, 400], 'Representant': False, 'CasesAdjacentes': [(7, 4), (7, 5), (8, 3), (8, 5), (9, 3), (9, 4)]},
                            (8, 5): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [225, 350, 275, 400], 'Representant': False, 'CasesAdjacentes': [(7, 5), (7, 6), (8, 4), (8, 6), (9, 4), (9, 5)]},
                            (8, 6): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [275, 350, 325, 400], 'Representant': False, 'CasesAdjacentes': [(7, 6), (7, 7), (8, 5), (9, 5)]},
                            (9, 1): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [50, 400, 100, 450], 'Representant': False, 'CasesAdjacentes': [(8, 1), (8, 2), (9, 2), (10, 1)]},
                            (9, 2): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [100, 400, 150, 450], 'Representant': False, 'CasesAdjacentes': [(8, 2), (8, 3), (9, 1), (9, 3), (10, 1), (10, 2)]},
                            (9, 3): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [150, 400, 200, 450], 'Representant': False, 'CasesAdjacentes': [(8, 3), (8, 4), (9, 2), (9, 4), (10, 2), (10, 3)]},
                            (9, 4): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [200, 400, 250, 450], 'Representant': False, 'CasesAdjacentes': [(8, 4), (8, 5), (9, 3), (9, 5), (10, 3), (10, 4)]},
                            (9, 5): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [250, 400, 300, 450], 'Representant': False, 'CasesAdjacentes': [(8, 5), (8, 6), (9, 4), (10, 4)]},
                            (10, 1): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [75, 450, 125, 500], 'Representant': False, 'CasesAdjacentes': [(9, 1), (9, 2), (10, 2), (11, 1)]},
                            (10, 2): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [125, 450, 175, 500], 'Representant': False, 'CasesAdjacentes': [(9, 2), (9, 3), (10, 1), (10, 3), (11, 1), (11, 2)]},
                            (10, 3): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [175, 450, 225, 500], 'Representant': False, 'CasesAdjacentes': [(9, 3), (9, 4), (10, 2), (10, 4), (11, 2), (11, 3)]},
                            (10, 4): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [225, 450, 275, 500], 'Representant': False, 'CasesAdjacentes': [(9, 4), (9, 5), (10, 3), (11, 3)]},
                            (11, 1): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [100, 500, 150, 550], 'Representant': False, 'CasesAdjacentes': [(10, 1), (10, 2), (11, 2), (12, 1)]},
                            (11, 2): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [150, 500, 200, 550], 'Representant': False, 'CasesAdjacentes': [(10, 2), (10, 3), (11, 1), (11, 3), (12, 1), (12, 2)]},
                            (11, 3): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [200, 500, 250, 550], 'Representant': False, 'CasesAdjacentes': [(10, 3), (10, 4), (11, 2), (12, 2)]},
                            (12, 1): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [125, 550, 175, 600], 'Representant': False, 'CasesAdjacentes': [(11, 1), (11, 2), (12, 2), (13, 1)]},
                            (12, 2): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [175, 550, 225, 600], 'Representant': False, 'CasesAdjacentes': [(11, 2), (11, 3), (12, 1), (13, 1)]},
                            (13, 1): {'Proprietaire': 'Neutre', 'Troupes': 0, 'Coordonnees': [150, 600, 200, 650], 'Representant': True, 'CasesAdjacentes': [(12, 1), (12, 2)]}}]
            self[1][caseDepartJ1]['Proprietaire'] = 'Joueur 1'
            self[1][caseDepartJ2]['Proprietaire'] = 'Joueur 2'
            self[1][caseDepartJ1]['Troupes'] = 7
            self[1][caseDepartJ2]['Troupes'] = 7
            self._infos.append(copy.deepcopy(self[1]))
            self.tour = 1

    def __getitem__(self, index:int):
        """
        Méthode permettant d'accéder à un index de l'attribut _infos en
        interrogeant l'objet de classe InfosDePartie sous la forme
        objet[index].

        Parameters
        ----------
        index : int
            Index de self auquel on veut accéder.

        Returns
        -------
        dict or int
            Valeur correspondant à l'index demandé.

        """
        return self._infos[index]

    def __setitem__(self, index:int, valeur):
        """
        Méthode permettant d'attribuer une valeur à un index de l'attribut
        _infos en interrogeant l'objet de classe InfosDePartie sous la forme
        objet[index] = valeur.

        Parameters
        ----------
        index : int
            Index de self auquel on veut attribuer une valeur.

        valeur : all types
            Valeur à attribuer.

        Returns
        -------
        None.

        """
        self._infos[index] = valeur

    def __delitem__(self, index:int):
        """
        Méthode permettant de supprimer la valeur correspondant à un index de
        l'attribut _infos en interrogeant l'objet de classe InfosDePartie sous
        la forme del objet[index].

        Parameters
        ----------
        index : int
            Index de self dont on veut supprimer la valeur.

        Returns
        -------
        None.

        """
        del self._infos[index]

    def __contains__(self, donneeCherche):
        """
        Méthode permettant de vérifier si une donnée est présente dans
        l'attribut _infos en interrogeant l'objet de classe InfosDePartie sous
        la forme valeur in objet.

        Parameters
        ----------
        donneeCherche : all types
            Donnée recherchée.

        Returns
        -------
        bool
            Renvoie True si la valeur est présente et False si ce n'est pas le
            cas.

        """
        for donnee in self._infos:
            if donnee == donneeCherche:
                return True
        return False

    def __len__(self):
        """
        Méthode renvoyant la longueur de l'attribut _infos en interrogeant
        l'objet de classe InfosDePartie sous la forme len(objet).

        Returns
        -------
        int
            Longueur de _infos.

        """
        return len(self._infos)

    def sauvegarder(self, fenetre=None, choixSauvegarde="choix"):
        """
        Méthode permettant de sauvegarder les données de jeu, soit celles
        contenues dans l'attribut _infos, sous un format personnalisé nommé
        kan et dont le but est de permettre une lecture simple du fichier tout
        en optimisant sa place en mémoire.

        Parameters
        ----------
        fenetre : tk.Tk
            Fenêtre tkinter parent.
        choixSauvegarde : string, optional
            Chemin du fichier de sauvegarde. Laisser la valeur par défaut
            permet à l'utilisateur de choisir l'endroit où il souhaite
            sauvegarder.
            The default is "choix".

        Returns
        -------
        None.

        """
        #Si aucun fichier n'est indiqué, ouverture d'une fenêtre permettant de choisir le nom et l'emplacement de la sauvegarde
        if choixSauvegarde != "choix":
            fichierSauvegarde = choixSauvegarde
        else:
            fichierSauvegarde = filedialog.asksaveasfilename(title="Nom et emplacement de la sauvegarde", initialdir=os.path.dirname(__file__)+"/Sauvegardes", initialfile=time.strftime("%d-%m-%Y_%H%M%S")+".kan", filetypes=[("Kanze", "*.kan"), ("All", "*")], defaultextension=".kan", parent=fenetre)
        #Calcul des scores de chacun des tours
        scores = self.calculScore()
        #Conversion des données de jeu au format kan
        sauvegarde = "/".join([cle + ";" + str(self[0][cle]) for cle in self[0].keys()]) + "\n" + str(len(self)-1)
        for i in range (1, len(self)):
            sauvegarde = sauvegarde + "\n" + str(i) + "/" + str(self[i][('nombreTroupes', 'Joueur 1')]) + "/" + str(self[i][('nombreTroupes', 'Joueur 2')]) + "/" + str(self[i][('nombreCases', 'Joueur 1')]) + "/" + str(self[i][('nombreCases', 'Joueur 2')]) + "/" + str(scores[i])
            if self[i]["action"] == None:
                sauvegarde = sauvegarde + "/" + "0"
            elif type(self[i]["action"]) != list:
                sauvegarde = sauvegarde + "/" + self[i]["action"]
            elif self[i]["action"][0] == "recruterCase":
                sauvegarde = sauvegarde + "/" + self[i]["action"][0]
                for caseRecrutement in self[i]["action"][1:]:
                    sauvegarde = sauvegarde + ";" + str(list(caseRecrutement)[0]) + "," + str(list(caseRecrutement)[1])
            else:
                sauvegarde = sauvegarde + "/" + self[i]["action"][0] + ";" + str(list(self[i]["action"][1])[0]) + "," + str(list(self[i]["action"][1])[1]) + ";" + str(list(self[i]["action"][2])[0]) + "," + str(list(self[i]["action"][2])[1]) + ";" + str(self[i]["action"][3]) + ";" + str(self[i]["action"][4])
            for case in self[i]:
                if type(self[i][case]) == dict:
                    sauvegarde = sauvegarde + "/" + str(list(case)[0]) + "," + str(list(case)[1]) + ";" + self[i][case]["Proprietaire"] + ";" + str(self[i][case]["Troupes"]) + ";" + str(self[i][case]["Representant"])
        #Ecriture des données converties dans le fichier choisi
        with open(fichierSauvegarde, "w") as fichierSauvegarde:
            fichierSauvegarde.write(sauvegarde)

    def calculScore(self):
        differencesTours = [None, None]
        scoresTours = [None]
        for i in range (2, len(self)-1):
            differencesTours.append((self[i][('nombreCases', 'Joueur 1')] - self[i-1][('nombreCases', 'Joueur 1')], self[i][('nombreCases', 'Joueur 2')] - self[i-1][('nombreCases', 'Joueur 2')], self[i][('nombreTroupes', 'Joueur 1')] - self[i-1][('nombreTroupes', 'Joueur 1')], self[i][('nombreTroupes', 'Joueur 2')] - self[i-1][('nombreTroupes', 'Joueur 2')]))
        for i in range (1, len(self)-1):
            joueur = 'Joueur '+('1' if i%2 == 1 else '2')
            score = {"evolCasesJoueur":0.0, "evolCasesAdversaire":0.0, "evolTroupesJoueur":0.0, "evolTroupesAdversaire":0.0}
            for j in range (1, 6 if len(differencesTours)-i > 5 else len(differencesTours)-i):
                score["evolCasesJoueur"] += differencesTours[i+j][0 if joueur == 'Joueur 1' else 1]/j
                score["evolCasesAdversaire"] += differencesTours[i+j][1 if joueur == 'Joueur 1' else 0]/j
                score["evolTroupesJoueur"] += differencesTours[i+j][2 if joueur == 'Joueur 1' else 3]/j
                score["evolTroupesAdversaire"] += differencesTours[i+j][3 if joueur == 'Joueur 1' else 2]/j
            scoresTours.append((score["evolCasesJoueur"]*100 + score["evolCasesAdversaire"]*100*(-1/4) + score["evolTroupesJoueur"]*100*(1/4) + score["evolTroupesAdversaire"]*100*(-1/8))//4)
        scoresTours.append(0.0)
        return scoresTours

    def importerSauvegarde(self, fenetre):
        """
        Méthode permettant d'importer une sauvegarde au format kan. Elle est
        convertie et les données importées viennent remplacer les données de
        jeu stockées dans _infos.

        Parameters
        ----------
        fenetre : tk.Tk
            Fenêtre tkinter parent.

        Returns
        -------
        str
            Erreur éventuelle ou instruction d'actualisation de l'interface.

        """
        #Ouverture d'une fenêtre permettant de choisir le fichier à importer
        fichierSauvegarde = filedialog.askopenfilename(title="Choix de la sauvegarde", initialdir=os.path.dirname(__file__)+"/Sauvegardes", filetypes=[("Kanze", "*.kan"), ("All", "*")], multiple=False, parent=fenetre)
        with open(fichierSauvegarde, "r") as fichierSauvegarde:
            sauvegarde = fichierSauvegarde.read()
        #Vérification sommaire que le fichier importé est au bon format
        if len(sauvegarde) < 200:
            return "Ce fichier n'est pas reconnu"
        #Conversion du fichier importé de manière à pouvoir utiliser les
        #données
        sauvegarde = sauvegarde.split("\n")
        sauvegarde[0] = sauvegarde[0].split("/")
        for i in range (len(sauvegarde[0])):
            sauvegarde[0][i] = sauvegarde[0][i].split(";")
        for i in range (2, len(sauvegarde)):
            sauvegarde[i] = sauvegarde[i].split("/")
            sauvegarde[i][6] = sauvegarde[i][6].split(";")
            # Conversion de l'action du tour
            if len(sauvegarde[i][6]) == 1:
                if sauvegarde[i][6][0] == "0":
                    sauvegarde[i][6] = None
                else:
                    sauvegarde[i][6] = sauvegarde[i][6][0]
            elif sauvegarde[i][6][0] == "recruterCase":
                for k in range (1, len(sauvegarde[i][6])):
                    sauvegarde[i][6][k] = (int(sauvegarde[i][6][k].split(",")[0]), int(sauvegarde[i][6][k].split(",")[1]))
            else:
                sauvegarde[i][6][1] = (int(sauvegarde[i][6][1].split(",")[0]), int(sauvegarde[i][6][1].split(",")[1]))
                sauvegarde[i][6][2] = (int(sauvegarde[i][6][2].split(",")[0]), int(sauvegarde[i][6][2].split(",")[1]))
                sauvegarde[i][6][3] = int(sauvegarde[i][6][3])
                sauvegarde[i][6][4] = sauvegarde[i][6][4]=="True"
            for j in range (7, len(sauvegarde[i])):
                sauvegarde[i][j] = sauvegarde[i][j].split(";")
                sauvegarde[i][j][0] = sauvegarde[i][j][0].split(",")
        #Réinitialisation de _infos et ajout de l'information de fin de partie et des options
        self._infos = [{cle:valeur for cle, valeur in sauvegarde[0]}]
        for cle, valeur in sauvegarde[0]:
            try :
                self[0][cle] = int(valeur)
            except ValueError:
                self[0][cle] = valeur=="True"
        #Ajout dans _infos des données importées, qui remplacent les infos déjà présentes
        for tour in sauvegarde[2:]:
            casesFormatees = {}
            for case in tour[7:]:
                casesFormatees[(int(case[0][0]), int(case[0][1]))] = {"Proprietaire":case[1], "Troupes":int(case[2]), "Representant":case[3]=="True"}
            self._infos.append({('nombreTroupes', 'Joueur 1'): int(tour[1]),
                                ('nombreTroupes', 'Joueur 2'): int(tour[2]),
                                ('nombreCases', 'Joueur 1'): int(tour[3]),
                                ('nombreCases', 'Joueur 2'): int(tour[4]),
                                "action": tour[6],
                                (1, 1): {'Proprietaire': casesFormatees[(1, 1)]['Proprietaire'], 'Troupes': casesFormatees[(1, 1)]['Troupes'], 'Coordonnees': [150, 0, 200, 50], 'Representant': casesFormatees[(1, 1)]['Representant'], 'CasesAdjacentes': [(2, 1), (2, 2)]},
                                (2, 1): {'Proprietaire': casesFormatees[(2, 1)]['Proprietaire'], 'Troupes': casesFormatees[(2, 1)]['Troupes'], 'Coordonnees': [125, 50, 175, 100], 'Representant': casesFormatees[(2, 1)]['Representant'], 'CasesAdjacentes': [(1, 1), (2, 2), (3, 1), (3, 2)]},
                                (2, 2): {'Proprietaire': casesFormatees[(2, 2)]['Proprietaire'], 'Troupes': casesFormatees[(2, 2)]['Troupes'], 'Coordonnees': [175, 50, 225, 100], 'Representant': casesFormatees[(2, 2)]['Representant'], 'CasesAdjacentes': [(1, 1), (2, 1), (3, 2), (3, 3)]},
                                (3, 1): {'Proprietaire': casesFormatees[(3, 1)]['Proprietaire'], 'Troupes': casesFormatees[(3, 1)]['Troupes'], 'Coordonnees': [100, 100, 150, 150], 'Representant': casesFormatees[(3, 1)]['Representant'], 'CasesAdjacentes': [(2, 1), (3, 2), (4, 1), (4, 2)]},
                                (3, 2): {'Proprietaire': casesFormatees[(3, 2)]['Proprietaire'], 'Troupes': casesFormatees[(3, 2)]['Troupes'], 'Coordonnees': [150, 100, 200, 150], 'Representant': casesFormatees[(3, 2)]['Representant'], 'CasesAdjacentes': [(2, 1), (2, 2), (3, 1), (3, 3), (4, 2), (4, 3)]},
                                (3, 3): {'Proprietaire': casesFormatees[(3, 3)]['Proprietaire'], 'Troupes': casesFormatees[(3, 3)]['Troupes'], 'Coordonnees': [200, 100, 250, 150], 'Representant': casesFormatees[(3, 3)]['Representant'], 'CasesAdjacentes': [(2, 2), (3, 2), (4, 3), (4, 4)]},
                                (4, 1): {'Proprietaire': casesFormatees[(4, 1)]['Proprietaire'], 'Troupes': casesFormatees[(4, 1)]['Troupes'], 'Coordonnees': [75, 150, 125, 200], 'Representant': casesFormatees[(4, 1)]['Representant'], 'CasesAdjacentes': [(3, 1), (4, 2), (5, 1), (5, 2)]},
                                (4, 2): {'Proprietaire': casesFormatees[(4, 2)]['Proprietaire'], 'Troupes': casesFormatees[(4, 2)]['Troupes'], 'Coordonnees': [125, 150, 175, 200], 'Representant': casesFormatees[(4, 2)]['Representant'], 'CasesAdjacentes': [(3, 1), (3, 2), (4, 1), (4, 3), (5, 2), (5, 3)]},
                                (4, 3): {'Proprietaire': casesFormatees[(4, 3)]['Proprietaire'], 'Troupes': casesFormatees[(4, 3)]['Troupes'], 'Coordonnees': [175, 150, 225, 200], 'Representant': casesFormatees[(4, 3)]['Representant'], 'CasesAdjacentes': [(3, 2), (3, 3), (4, 2), (4, 4), (5, 3), (5, 4)]},
                                (4, 4): {'Proprietaire': casesFormatees[(4, 4)]['Proprietaire'], 'Troupes': casesFormatees[(4, 4)]['Troupes'], 'Coordonnees': [225, 150, 275, 200], 'Representant': casesFormatees[(4, 4)]['Representant'], 'CasesAdjacentes': [(3, 3), (4, 3), (5, 4), (5, 5)]},
                                (5, 1): {'Proprietaire': casesFormatees[(5, 1)]['Proprietaire'], 'Troupes': casesFormatees[(5, 1)]['Troupes'], 'Coordonnees': [50, 200, 100, 250], 'Representant': casesFormatees[(5, 1)]['Representant'], 'CasesAdjacentes': [(4, 1), (5, 2), (6, 1), (6, 2)]},
                                (5, 2): {'Proprietaire': casesFormatees[(5, 2)]['Proprietaire'], 'Troupes': casesFormatees[(5, 2)]['Troupes'], 'Coordonnees': [100, 200, 150, 250], 'Representant': casesFormatees[(5, 2)]['Representant'], 'CasesAdjacentes': [(4, 1), (4, 2), (5, 1), (5, 3), (6, 2), (6, 3)]},
                                (5, 3): {'Proprietaire': casesFormatees[(5, 3)]['Proprietaire'], 'Troupes': casesFormatees[(5, 3)]['Troupes'], 'Coordonnees': [150, 200, 200, 250], 'Representant': casesFormatees[(5, 3)]['Representant'], 'CasesAdjacentes': [(4, 2), (4, 3), (5, 2), (5, 4), (6, 3), (6, 4)]},
                                (5, 4): {'Proprietaire': casesFormatees[(5, 4)]['Proprietaire'], 'Troupes': casesFormatees[(5, 4)]['Troupes'], 'Coordonnees': [200, 200, 250, 250], 'Representant': casesFormatees[(5, 4)]['Representant'], 'CasesAdjacentes': [(4, 3), (4, 4), (5, 3), (5, 5), (6, 4), (6, 5)]},
                                (5, 5): {'Proprietaire': casesFormatees[(5, 5)]['Proprietaire'], 'Troupes': casesFormatees[(5, 5)]['Troupes'], 'Coordonnees': [250, 200, 300, 250], 'Representant': casesFormatees[(5, 5)]['Representant'], 'CasesAdjacentes': [(4, 4), (5, 4), (6, 5), (6, 6)]},
                                (6, 1): {'Proprietaire': casesFormatees[(6, 1)]['Proprietaire'], 'Troupes': casesFormatees[(6, 1)]['Troupes'], 'Coordonnees': [25, 250, 75, 300], 'Representant': casesFormatees[(6, 1)]['Representant'], 'CasesAdjacentes': [(5, 1), (6, 2), (7, 1), (7, 2)]},
                                (6, 2): {'Proprietaire': casesFormatees[(6, 2)]['Proprietaire'], 'Troupes': casesFormatees[(6, 2)]['Troupes'], 'Coordonnees': [75, 250, 125, 300], 'Representant': casesFormatees[(6, 2)]['Representant'], 'CasesAdjacentes': [(5, 1), (5, 2), (6, 1), (6, 3), (7, 2), (7, 3)]},
                                (6, 3): {'Proprietaire': casesFormatees[(6, 3)]['Proprietaire'], 'Troupes': casesFormatees[(6, 3)]['Troupes'], 'Coordonnees': [125, 250, 175, 300], 'Representant': casesFormatees[(6, 3)]['Representant'], 'CasesAdjacentes': [(5, 2), (5, 3), (6, 2), (6, 4), (7, 3), (7, 4)]},
                                (6, 4): {'Proprietaire': casesFormatees[(6, 4)]['Proprietaire'], 'Troupes': casesFormatees[(6, 4)]['Troupes'], 'Coordonnees': [175, 250, 225, 300], 'Representant': casesFormatees[(6, 4)]['Representant'], 'CasesAdjacentes': [(5, 3), (5, 4), (6, 3), (6, 5), (7, 4), (7, 5)]},
                                (6, 5): {'Proprietaire': casesFormatees[(6, 5)]['Proprietaire'], 'Troupes': casesFormatees[(6, 5)]['Troupes'], 'Coordonnees': [225, 250, 275, 300], 'Representant': casesFormatees[(6, 5)]['Representant'], 'CasesAdjacentes': [(5, 4), (5, 5), (6, 4), (6, 6), (7, 5), (7, 6)]},
                                (6, 6): {'Proprietaire': casesFormatees[(6, 6)]['Proprietaire'], 'Troupes': casesFormatees[(6, 6)]['Troupes'], 'Coordonnees': [275, 250, 325, 300], 'Representant': casesFormatees[(6, 6)]['Representant'], 'CasesAdjacentes': [(5, 5), (6, 5), (7, 6), (7, 7)]},
                                (7, 1): {'Proprietaire': casesFormatees[(7, 1)]['Proprietaire'], 'Troupes': casesFormatees[(7, 1)]['Troupes'], 'Coordonnees': [0, 300, 50, 350], 'Representant': casesFormatees[(7, 1)]['Representant'], 'CasesAdjacentes': [(6, 1), (7, 2), (8, 1)]},
                                (7, 2): {'Proprietaire': casesFormatees[(7, 2)]['Proprietaire'], 'Troupes': casesFormatees[(7, 2)]['Troupes'], 'Coordonnees': [50, 300, 100, 350], 'Representant': casesFormatees[(7, 2)]['Representant'], 'CasesAdjacentes': [(6, 1), (6, 2), (7, 1), (7, 3), (8, 1), (8, 2)]},
                                (7, 3): {'Proprietaire': casesFormatees[(7, 3)]['Proprietaire'], 'Troupes': casesFormatees[(7, 3)]['Troupes'], 'Coordonnees': [100, 300, 150, 350], 'Representant': casesFormatees[(7, 3)]['Representant'], 'CasesAdjacentes': [(6, 2), (6, 3), (7, 2), (7, 4), (8, 2), (8, 3)]},
                                (7, 4): {'Proprietaire': casesFormatees[(7, 4)]['Proprietaire'], 'Troupes': casesFormatees[(7, 4)]['Troupes'], 'Coordonnees': [150, 300, 200, 350], 'Representant': casesFormatees[(7, 4)]['Representant'], 'CasesAdjacentes': [(6, 3), (6, 4), (7, 3), (7, 5), (8, 3), (8, 4)]},
                                (7, 5): {'Proprietaire': casesFormatees[(7, 5)]['Proprietaire'], 'Troupes': casesFormatees[(7, 5)]['Troupes'], 'Coordonnees': [200, 300, 250, 350], 'Representant': casesFormatees[(7, 5)]['Representant'], 'CasesAdjacentes': [(6, 4), (6, 5), (7, 4), (7, 6), (8, 4), (8, 5)]},
                                (7, 6): {'Proprietaire': casesFormatees[(7, 6)]['Proprietaire'], 'Troupes': casesFormatees[(7, 6)]['Troupes'], 'Coordonnees': [250, 300, 300, 350], 'Representant': casesFormatees[(7, 6)]['Representant'], 'CasesAdjacentes': [(6, 5), (6, 6), (7, 5), (7, 7), (8, 5), (8, 6)]},
                                (7, 7): {'Proprietaire': casesFormatees[(7, 7)]['Proprietaire'], 'Troupes': casesFormatees[(7, 7)]['Troupes'], 'Coordonnees': [300, 300, 350, 350], 'Representant': casesFormatees[(7, 7)]['Representant'], 'CasesAdjacentes': [(6, 6), (7, 6), (8, 6)]},
                                (8, 1): {'Proprietaire': casesFormatees[(8, 1)]['Proprietaire'], 'Troupes': casesFormatees[(8, 1)]['Troupes'], 'Coordonnees': [25, 350, 75, 400], 'Representant': casesFormatees[(8, 1)]['Representant'], 'CasesAdjacentes': [(7, 1), (7, 2), (8, 2), (9, 1)]},
                                (8, 2): {'Proprietaire': casesFormatees[(8, 2)]['Proprietaire'], 'Troupes': casesFormatees[(8, 2)]['Troupes'], 'Coordonnees': [75, 350, 125, 400], 'Representant': casesFormatees[(8, 2)]['Representant'], 'CasesAdjacentes': [(7, 2), (7, 3), (8, 1), (8, 3), (9, 1), (9, 2)]},
                                (8, 3): {'Proprietaire': casesFormatees[(8, 3)]['Proprietaire'], 'Troupes': casesFormatees[(8, 3)]['Troupes'], 'Coordonnees': [125, 350, 175, 400], 'Representant': casesFormatees[(8, 3)]['Representant'], 'CasesAdjacentes': [(7, 3), (7, 4), (8, 2), (8, 4), (9, 2), (9, 3)]},
                                (8, 4): {'Proprietaire': casesFormatees[(8, 4)]['Proprietaire'], 'Troupes': casesFormatees[(8, 4)]['Troupes'], 'Coordonnees': [175, 350, 225, 400], 'Representant': casesFormatees[(8, 4)]['Representant'], 'CasesAdjacentes': [(7, 4), (7, 5), (8, 3), (8, 5), (9, 3), (9, 4)]},
                                (8, 5): {'Proprietaire': casesFormatees[(8, 5)]['Proprietaire'], 'Troupes': casesFormatees[(8, 5)]['Troupes'], 'Coordonnees': [225, 350, 275, 400], 'Representant': casesFormatees[(8, 5)]['Representant'], 'CasesAdjacentes': [(7, 5), (7, 6), (8, 4), (8, 6), (9, 4), (9, 5)]},
                                (8, 6): {'Proprietaire': casesFormatees[(8, 6)]['Proprietaire'], 'Troupes': casesFormatees[(8, 6)]['Troupes'], 'Coordonnees': [275, 350, 325, 400], 'Representant': casesFormatees[(8, 6)]['Representant'], 'CasesAdjacentes': [(7, 6), (7, 7), (8, 5), (9, 5)]},
                                (9, 1): {'Proprietaire': casesFormatees[(9, 1)]['Proprietaire'], 'Troupes': casesFormatees[(9, 1)]['Troupes'], 'Coordonnees': [50, 400, 100, 450], 'Representant': casesFormatees[(9, 1)]['Representant'], 'CasesAdjacentes': [(8, 1), (8, 2), (9, 2), (10, 1)]},
                                (9, 2): {'Proprietaire': casesFormatees[(9, 2)]['Proprietaire'], 'Troupes': casesFormatees[(9, 2)]['Troupes'], 'Coordonnees': [100, 400, 150, 450], 'Representant': casesFormatees[(9, 2)]['Representant'], 'CasesAdjacentes': [(8, 2), (8, 3), (9, 1), (9, 3), (10, 1), (10, 2)]},
                                (9, 3): {'Proprietaire': casesFormatees[(9, 3)]['Proprietaire'], 'Troupes': casesFormatees[(9, 3)]['Troupes'], 'Coordonnees': [150, 400, 200, 450], 'Representant': casesFormatees[(9, 3)]['Representant'], 'CasesAdjacentes': [(8, 3), (8, 4), (9, 2), (9, 4), (10, 2), (10, 3)]},
                                (9, 4): {'Proprietaire': casesFormatees[(9, 4)]['Proprietaire'], 'Troupes': casesFormatees[(9, 4)]['Troupes'], 'Coordonnees': [200, 400, 250, 450], 'Representant': casesFormatees[(9, 4)]['Representant'], 'CasesAdjacentes': [(8, 4), (8, 5), (9, 3), (9, 5), (10, 3), (10, 4)]},
                                (9, 5): {'Proprietaire': casesFormatees[(9, 5)]['Proprietaire'], 'Troupes': casesFormatees[(9, 5)]['Troupes'], 'Coordonnees': [250, 400, 300, 450], 'Representant': casesFormatees[(9, 5)]['Representant'], 'CasesAdjacentes': [(8, 5), (8, 6), (9, 4), (10, 4)]},
                                (10, 1): {'Proprietaire': casesFormatees[(10, 1)]['Proprietaire'], 'Troupes': casesFormatees[(10, 1)]['Troupes'], 'Coordonnees': [75, 450, 125, 500], 'Representant': casesFormatees[(10, 1)]['Representant'], 'CasesAdjacentes': [(9, 1), (9, 2), (10, 2), (11, 1)]},
                                (10, 2): {'Proprietaire': casesFormatees[(10, 2)]['Proprietaire'], 'Troupes': casesFormatees[(10, 2)]['Troupes'], 'Coordonnees': [125, 450, 175, 500], 'Representant': casesFormatees[(10, 2)]['Representant'], 'CasesAdjacentes': [(9, 2), (9, 3), (10, 1), (10, 3), (11, 1), (11, 2)]},
                                (10, 3): {'Proprietaire': casesFormatees[(10, 3)]['Proprietaire'], 'Troupes': casesFormatees[(10, 3)]['Troupes'], 'Coordonnees': [175, 450, 225, 500], 'Representant': casesFormatees[(10, 3)]['Representant'], 'CasesAdjacentes': [(9, 3), (9, 4), (10, 2), (10, 4), (11, 2), (11, 3)]},
                                (10, 4): {'Proprietaire': casesFormatees[(10, 4)]['Proprietaire'], 'Troupes': casesFormatees[(10, 4)]['Troupes'], 'Coordonnees': [225, 450, 275, 500], 'Representant': casesFormatees[(10, 4)]['Representant'], 'CasesAdjacentes': [(9, 4), (9, 5), (10, 3), (11, 3)]},
                                (11, 1): {'Proprietaire': casesFormatees[(11, 1)]['Proprietaire'], 'Troupes': casesFormatees[(11, 1)]['Troupes'], 'Coordonnees': [100, 500, 150, 550], 'Representant': casesFormatees[(11, 1)]['Representant'], 'CasesAdjacentes': [(10, 1), (10, 2), (11, 2), (12, 1)]},
                                (11, 2): {'Proprietaire': casesFormatees[(11, 2)]['Proprietaire'], 'Troupes': casesFormatees[(11, 2)]['Troupes'], 'Coordonnees': [150, 500, 200, 550], 'Representant': casesFormatees[(11, 2)]['Representant'], 'CasesAdjacentes': [(10, 2), (10, 3), (11, 1), (11, 3), (12, 1), (12, 2)]},
                                (11, 3): {'Proprietaire': casesFormatees[(11, 3)]['Proprietaire'], 'Troupes': casesFormatees[(11, 3)]['Troupes'], 'Coordonnees': [200, 500, 250, 550], 'Representant': casesFormatees[(11, 3)]['Representant'], 'CasesAdjacentes': [(10, 3), (10, 4), (11, 2), (12, 2)]},
                                (12, 1): {'Proprietaire': casesFormatees[(12, 1)]['Proprietaire'], 'Troupes': casesFormatees[(12, 1)]['Troupes'], 'Coordonnees': [125, 550, 175, 600], 'Representant': casesFormatees[(12, 1)]['Representant'], 'CasesAdjacentes': [(11, 1), (11, 2), (12, 2), (13, 1)]},
                                (12, 2): {'Proprietaire': casesFormatees[(12, 2)]['Proprietaire'], 'Troupes': casesFormatees[(12, 2)]['Troupes'], 'Coordonnees': [175, 550, 225, 600], 'Representant': casesFormatees[(12, 2)]['Representant'], 'CasesAdjacentes': [(11, 2), (11, 3), (12, 1), (13, 1)]},
                                (13, 1): {'Proprietaire': casesFormatees[(13, 1)]['Proprietaire'], 'Troupes': casesFormatees[(13, 1)]['Troupes'], 'Coordonnees': [150, 600, 200, 650], 'Representant': casesFormatees[(13, 1)]['Representant'], 'CasesAdjacentes': [(12, 1), (12, 2)]}})
        #Le tour actif est fixé au dernier tour de la sauvegarde importée
        self.tour = len(self)-2
        return "Actualisation"

    def changementTour(self, nouveauTour):
        """
        Vérifie que le tour demandé par le joueur est valide et si c'est
        le cas, modifie l'attribut tour pour qu'il corresponde au tour demandé.

        Parameters
        ----------
        nouveauTour : int
            Numéro du tour demandé par l'utilisateur.

        Returns
        -------
        str
            Erreur éventuelle ou instruction d'actualisation de l'interface.

        """
        if type(nouveauTour) != int:
            return "Le tour demandé doit être un nombre entier"
        elif nouveauTour < 1 or nouveauTour > len(self)-2:
            return "Ce tour n'existe pas"
        else:
            self.tour = nouveauTour
            return "Actualisation"

    def ajoutTour(self):
        """
        Ajoute une copie des informations du tour actuel dans la liste des
        tours afin de permettre la navigation entre les tours.

        Returns
        -------
        None.

        """
        self._infos.append(copy.deepcopy(self[self.tour]))

    def nouvelleVersion(self):
        """
        Supprime tous les tours déjà joués après celui en cours et copie le
        tour actuel dans le but de réinitialiser les coups joués si
        l'utilisateur revient en arrière et décide de changer le coup joué.

        Amélioration possible : demander à l'utilisateur s'il est sur de
        vouloir supprimer les tours suivants. Ou proposer dans ce cas de
        sauvegarder la partie voir créer un système de gestion de branche
        possibles de la partie.

        Returns
        -------
        None.

        """
        del self[self.tour+1:]
        self.ajoutTour()

    def deplacement(self, caseDepart:tuple, caseArrivee:tuple, nombreTroupes:int, representant:bool):
        """
        Gère l'action "Déplacer" en vérifiant que le déplacement est valide et
        en mettant à jour les informations du tour en fonction si c'est le cas.

        Parameters
        ----------
        caseDepart : tuple
            Coordonnées de la case d'où part le déplacement.
        caseArrivee : tuple
            Coordonnées de la case où arrive le déplacement.
        nombreTroupes : int
            Nombre de troupes à déplacer depuis la case de départ.
        representant : bool
            Indication de la présence du Représentant dans les troupes
            déplacées.

        Returns
        -------
        str
            Erreur éventuelle.

        """
        #Réinitialisation des tours suivants si besoin
        self.nouvelleVersion()
        #Vérification du joueur actif à partir du numéro du tour
        if self.tour%2 == 0:
            joueur = "Joueur 2"
            adversaire = "Joueur 1"
        else:
            joueur = "Joueur 1"
            adversaire = "Joueur 2"
        #Test de la validité du déplacement et si il est invalide, fin de la fonction et renvoi d'une notification d'erreur
        validite, validiteRepresentant = self.verificationDeplacement(joueur, nombreTroupes, caseDepart, caseArrivee, representant)
        if validiteRepresentant == False:
            return "Vous ne pouvez pas déplacer de Représentant à partir de cette case."
        elif validite == False:
            return "Ce déplacement n'est pas réglementaire."
        if self[self.tour][caseArrivee]["Proprietaire"] == adversaire:
            #Les troupes et éventuellement le représentant sont retirés de la case de départ
            self[self.tour+1][caseDepart]["Troupes"] -= nombreTroupes
            if representant == True:
                self[self.tour+1][caseDepart]["Representant"] = False
            #Selon le nombre de troupes et la présence ou non d'un représentant sur chaque case, le propriétaire, le nombre de troupes et la présence d'un représentant sur la case d'arrivée sont mis à jour
            if self[self.tour][caseArrivee]["Representant"] == True:
                if nombreTroupes >= self[self.tour][caseArrivee]["Troupes"]+1:
                    self[self.tour+1][caseArrivee]["Troupes"] = nombreTroupes - self[self.tour+1][caseArrivee]["Troupes"]+1
                    self[self.tour+1][caseArrivee]["Proprietaire"] = joueur
                    if representant == False:
                        self[self.tour+1][caseArrivee]["Representant"] = False
                else:
                    if representant == True and nombreTroupes+1 == self[self.tour][caseArrivee]["Troupes"]+1:
                        self[self.tour+1][caseArrivee]["Troupes"] = 0
                        self[self.tour+1][caseArrivee]["Representant"] = False
                    elif representant == True:
                        self[self.tour+1][caseArrivee]["Troupes"] -= nombreTroupes+1
                    else:
                        self[self.tour+1][caseArrivee]["Troupes"] -= nombreTroupes
            else:
                if nombreTroupes >= self[self.tour][caseArrivee]["Troupes"]:
                    self[self.tour+1][caseArrivee]["Troupes"] = nombreTroupes - self[self.tour+1][caseArrivee]["Troupes"]
                    self[self.tour+1][caseArrivee]["Proprietaire"] = joueur
                    if representant == True:
                        self[self.tour+1][caseArrivee]["Representant"] = True
                elif nombreTroupes < self[self.tour][caseArrivee]["Troupes"] and representant == True:
                    self[self.tour+1][caseArrivee]["Troupes"] = self[self.tour+1][caseArrivee]["Troupes"] - (nombreTroupes + 1)
                else:
                    self[self.tour+1][caseArrivee]["Troupes"] = self[self.tour+1][caseArrivee]["Troupes"] - nombreTroupes
            #L'action jouée est inscrite dans les informations du tour actuel
            self[self.tour]["action"] = ["deplacer", caseDepart, caseArrivee, nombreTroupes, representant]
        elif self[self.tour][caseArrivee]["Proprietaire"] == joueur:
            #Si la case visée appartient au joueur actif, il est vérifié que la somme des troupes déplacées et de celles de la case d'arrivée ne dépasse pas 7 et si c'est le cas, fin de la fonction et renvoi d'une notification d'erreur
            if self[self.tour][caseArrivee]["Troupes"] + nombreTroupes > 7:
                return "Nombre de troupes déplacées incorrect, veuillez recommencer"
            #Les troupes déplacées sont retirées de la case de départ et ajoutées à la case d'arrivée, de même que le Représentant si il est déplacé
            self[self.tour+1][caseDepart]["Troupes"] -= nombreTroupes
            if representant == True:
                self[self.tour+1][caseDepart]["Representant"] = False
                self[self.tour+1][caseArrivee]["Representant"] = True
            self[self.tour+1][caseArrivee]["Troupes"] += nombreTroupes
            #L'action jouée est inscrite dans les informations du tour actuel
            self[self.tour]["action"] = ["deplacer", caseDepart, caseArrivee, nombreTroupes, representant]
        elif self[self.tour][caseArrivee]["Proprietaire"] == "Neutre":
            #Si la case visée est neutre, le propriétaire de la case d'arrivée devient le joueur actif et les troupes déplacées sont retirées de la case de départ et ajoutées à la case d'arrivée, de même que le Représentant si il est déplacé
            self[self.tour+1][caseDepart]["Troupes"] -= nombreTroupes
            if representant == True:
                self[self.tour+1][caseDepart]["Representant"] = False
                self[self.tour+1][caseArrivee]["Representant"] = True
            self[self.tour+1][caseArrivee]["Proprietaire"] = joueur
            self[self.tour+1][caseArrivee]["Troupes"] = nombreTroupes
            #L'action jouée est inscrite dans les informations du tour actuel
            self[self.tour]["action"] = ["deplacer", caseDepart, caseArrivee, nombreTroupes, representant]

    def verificationDeplacement(self, joueur:str, nombreTroupes:int, caseDepart:tuple, caseArrivee:tuple, representant:bool):
        """
        Fonction vérifiant la validité d'un déplacement.

        Parameters
        ----------
        joueur : str
            Indication du joueur actuel.
        nombreTroupes : int
            Nombre de troupes à déplacer.
        caseDepart : tuple
            Coordonnées de la case d'où part le déplacement.
        caseArrivee : tuple
            Coordonnées de la case où arrive le déplacement.
        representant : bool
            Indication de la présence du Représentant dans les troupes
            déplacées.

        Returns
        -------
        validite : bool
            Indication de la validité du déplacement.
        validiteRepresentant : bool
            Indication de la validité du déplacement du représentant si
            nécessaire.

        """
        validiteRepresentant = True
        #Vérification que le nombre de troupes déplacées et la case depuis laquelle elles le sont sont valides
        if nombreTroupes >= 0 and nombreTroupes <= 7 and self[self.tour][caseDepart]["Troupes"] >= nombreTroupes and self[self.tour][caseDepart]["Proprietaire"] == joueur:
            #Vérification que le Représentant peut être déplacé
            if representant == True and self[self.tour][caseDepart]["Representant"] != True:
                validite = False
                validiteRepresentant = False
            #Vérification de la validité de la case d'arrivée, c'est à dire si elle est reliée à la case de départ quand elle appartient au joueur actif et si elle est adjacente quand elle appartient au joueur adverse ou qu'elle est neutre (cela peut changer selon les options activées)
            elif caseArrivee in self[self.tour][caseDepart]["CasesAdjacentes"]:
                #Si la case est adjacente, le déplacement est toujours valide
                validite = True
            else:
                #Si la case n'est pas adjacente, il est vérifié qu'elle appartient au joueur actif, ou autre selon les options sélectionnées, et qu'elle est reliée à la case de départ
                #Pour cela, une boucle vérifie les cases adjacente pour chaque case adjacente à la case de départ et recommence l'action pour chaque case appartenant au joueur actif
                #Et ce jusqu'à ce qu'un chemin reliant les 2 cases soit trouvé ou que toutes les cases rencontrées aient été testées
                validite = False
                if self[self.tour][caseArrivee]["Proprietaire"] == joueur or (self[0]["casesNeutresNonAdjacentes"] and self[self.tour][caseArrivee]["Proprietaire"] == "Neutre") or (self[0]["casesAdversesNonAdjacentes"] and self[self.tour][caseArrivee]["Proprietaire"] != "Neutre"):
                    casesVisitees = [caseDepart]
                    casesVerifiees = []
                    while validite == False and len(casesVisitees) > 0:
                        nouvelleCase = False
                        i = 0
                        while nouvelleCase == False and i < len(self[self.tour][casesVisitees[-1]]["CasesAdjacentes"]):
                            if self[self.tour][casesVisitees[-1]]["CasesAdjacentes"][i] == caseArrivee:
                                nouvelleCase = True
                                validite = True
                            elif self[self.tour][self[self.tour][casesVisitees[-1]]["CasesAdjacentes"][i]]["Proprietaire"] == joueur and self[self.tour][casesVisitees[-1]]["CasesAdjacentes"][i] not in casesVisitees and self[self.tour][casesVisitees[-1]]["CasesAdjacentes"][i] not in casesVerifiees:
                                nouvelleCase = True
                                casesVisitees.append(self[self.tour][casesVisitees[-1]]["CasesAdjacentes"][i])
                            else:
                                i += 1
                        if nouvelleCase == False:
                            casesVerifiees.append(casesVisitees.pop())
        else:
            validite = False
        return validite, validiteRepresentant

    def recrutement(self):
        """
        Fonction gérant le recrutement, ce qui comprend la vérification du nombre de
        troupe du joueur actif et si nécessaire le choix des cases où recruter, les
        changements dans le répertoire des cases "infosJeu".

        Returns
        -------
        int or str
            Si le recrutement est possible mais pas sur chaque case du joueur,
            le nombre de troupes à recruter est renvoyé de manière à être
            traité d'une autre manière.
            Si le recrutement est impssible, une notication d'erreur sous
            forme de chaîne de caractère est renvoyée.
        """
        #Réinitialisation des tours suivants
        self.nouvelleVersion()
        #Vérification du joueur actif à partir du numéro du tour
        if self.tour%2 == 0:
            joueur = "Joueur 2"
        else:
            joueur = "Joueur 1"
        #Compte du nombre de troupes à rajouter
        troupesARajouter = 0
        for case in self[self.tour].keys():
            if type(self[self.tour][case]) == dict and type(case) == tuple:
                if self[self.tour][case]["Proprietaire"] == joueur and self[self.tour][case]["Troupes"] < 7:
                    troupesARajouter += 1
        if troupesARajouter == 0:
            return "Vos cases sont pleines, vous ne pouvez pas recruter."
        #Si le nombre de troupes après le recrutement ne dépasse pas le nombre de troupes maximal fixé pour la partie, ajout d'une nouvelle troupe sur chaque case du joueur actif qui compte moins de 7 troupes
        elif self[self.tour]["nombreTroupes", joueur] + troupesARajouter <= self[0]["nombreDeTroupesMax"]:
            for case in self[self.tour+1].keys():
                if type(self[self.tour+1][case]) == dict:
                    if self[self.tour+1][case]["Proprietaire"] == joueur and self[self.tour+1][case]["Troupes"] < 7:
                        self[self.tour+1][case]["Troupes"] += 1
        #Si le nombre de troupes du joueur est trop élevée pour recruter sur chacune de ses cases mais est inférieur au nombre de troupes maximal fixé pour la partie, renvoi du nombre de troupes à rajouter, sui sera pris en compte de façon extérieure
        elif self[self.tour]["nombreTroupes", joueur] < self[0]["nombreDeTroupesMax"]:
            #Une liste comportant le type de l'action jouée et destinée à contenir les cases où il y a eu un recrutement est ajoutée dans les informations du tour actuel
            self[self.tour]["action"] = ["recruterCase"]
            return self[0]["nombreDeTroupesMax"] - self[self.tour]["nombreTroupes", joueur]
        #Si le nombre de troupes du joueur est trop élevée pour recruter sur chacune de ses cases et supérieur ou égal au nombre de troupes maximal fixé pour la partie, renvoi d'une erreur
        else:
            return "Vous possédez trop de troupes pour pouvoir recruter.\nVeuillez choisir une autre option."
        #L'action jouée est inscrite dans les informations du tour actuel
        self[self.tour]["action"] = "recruter"

    def recrutementALaCase(self, joueur:str, case:tuple):
        """
        Ajout si possible d'une troupe sur une case donnée.

        Parameters
        ----------
        joueur : str
            Indication du joueur actif.
        case : tuple
            Coordonnées de la case où il faut recruter.

        Returns
        -------
        str
            Notification éventuelle d'erreur.

        """
        if self[self.tour][case]["Proprietaire"] != joueur or self[self.tour][case]["Troupes"] >= 7:
            return "Impossible de recruter sur cette case."
        elif case in self[self.tour]["action"]:
            return "Un recrutement a déjà eu lieu sur cette case durant ce tour."
        else:
            self[self.tour+1][case]["Troupes"] += 1
            self[self.tour]["action"].append(case)

    def passerTour(self):
        """
        Passe un tour.

        Returns
        -------
        None.

        """
        self.nouvelleVersion()
        self[self.tour]["action"] = "passer"

    def influence(self):
        """
        Fonction gérant l'influence, soit le changement de propriétaire d'une
        case lorsqu'elle est entourée en majorité par des cases adverses.

        Returns
        -------
        None.

        """
        changement = True
        #Tant que la totalité des cases ne sont pas stables, elles subissent toutes une vérification de l'influence
        while changement == True:
            changement = False
            #Pour toutes les cases, si le propriétaire d'une des cases ajacente est le joueur adverse, "proprietaireDifferent" augmente de 1
            for case in self[self.tour].keys():
                if type(self[self.tour][case]) == dict and type(case) == tuple:
                    if self[self.tour][case]["Proprietaire"] != "Neutre" and self[self.tour][case]["Representant"] == False:
                        proprietaireDifferent = 0
                        for caseAdjacente in self[self.tour][case]["CasesAdjacentes"]:
                            if self[self.tour][caseAdjacente]["Proprietaire"] != self[self.tour][case]["Proprietaire"] and self[self.tour][caseAdjacente]["Proprietaire"] != "Neutre":
                                proprietaireDifferent += 1
                                adversaire = self[self.tour][caseAdjacente]["Proprietaire"]
                        #Si le nombre de cases adjacentes appartenant au joueur adverse est supérieur au nombre de cases adjacentes, le propriétaire de la case devient le joueur adverse
                        if proprietaireDifferent > len(self[self.tour][case]["CasesAdjacentes"])/2:
                            self[self.tour][case]["Proprietaire"] = adversaire
                            changement = True

class FenetreGlobale:
    """
    Classe gérant le premier paramétrage et le lancement des parties en créant
    une fenêtre faisant office de menu de jeu. On y trouve la possiblité de
    lancer une partie en modifiant des options, de continuer ou revoir une
    partie importée, de voir les règles du Kanze et de quitter le programme.
    """
    def __init__(self):
        """
        Constructeur créant la fenêtre dans son état de base et paramétrant
        les attributs.

        Returns
        -------
        None.

        """
        self.demarrage()

    def demarrage(self):
        """
        Créé une fenêtre et initialise les widgets qui la composent et les
        attibuts permettant son fonctionnement et la prise en compte des
        choix d'options de l'utilisateur.
        Cette fonction est appelée au démarrage du programme mais aussi à la
        fermeture de toutes les fenêtre de jeu.

        Returns
        -------
        None.

        """
        #Création de la fenêtre
        self.fenetre = tk.Tk()
        self.fenetre.title("Kanzé")

        #Initialisation des attributs qui ne représentent pas un élément fixe de la fenêtre
        self._joueur1 = tk.BooleanVar()
        self._joueur2 = tk.BooleanVar()
        self._troupesMax = tk.StringVar()
        self._troupesMax.set("49")
        self._casesNeutresNonAdjacentes = tk.BooleanVar()
        self._casesNeutresNonAdjacentes.set(True)
        self._casesAdversesNonAdjacentes = tk.BooleanVar()

        #Initialisation des attributs qui représentent un élément visible fixe de la fenêtre
        self.boutonNouvellePartie = tk.Button(self.fenetre, text="Nouvelle partie", command=self.nouvellePartie)
        self.boutonNouvellePartie.grid(row=1, column=0)
        self.boutonImporterPartie = tk.Button(self.fenetre, text="Importer une partie", command=self.importerPartie)
        self.boutonImporterPartie.grid(row=2, column=0)
        self.boutonRegles = tk.Button(self.fenetre, text="Règles du jeu", command=self.regles)
        self.boutonRegles.grid(row=3, column=0)
        self.boutonQuitter = tk.Button(self.fenetre, text="Quitter", command=self.fenetre.quit)
        self.boutonQuitter.grid(row=4, column=0)

        #Début de la boucle durant laquelle on peut interagir avec la fenêtre
        self.fenetre.mainloop()
        #Destruction de la fenêtre lorsque la boucle s'est finie
        self.fenetre.destroy()

    def retour(self):
        """
        Permet de repasser la fenêtre de son état de choix d'option à son état
        de base.

        Returns
        -------
        None.

        """
        #Les éléments présents dans la fenêtre sont cachés
        self.texteJoueur1.grid_remove()
        self.checkboxJoueur1.grid_remove()
        self.texteJoueur2.grid_remove()
        self.checkboxJoueur2.grid_remove()
        self.texteTroupesMax.grid_remove()
        self.boutonRetirerTroupe.grid_remove()
        self.entreeTroupes.grid_remove()
        self.boutonAugmenterTroupe.grid_remove()
        self.texteCasesNeutresNonAdjacentes.grid_remove()
        self.checkboxCasesNeutresNonAdjacentes.grid_remove()
        self.texteCasesAdversesNonAdjacentes.grid_remove()
        self.checkboxCasesAdversesNonAdjacentes.grid_remove()
        self.boutonRetour.grid_remove()
        self.boutonLancerPartie.grid_remove()
        self.boutonReinitialiser.grid_remove()

        #Les éléments cachés redeviennent visibles
        self.boutonNouvellePartie.grid()
        self.boutonImporterPartie.grid()
        self.boutonRegles.grid()
        self.boutonQuitter.grid()

    def reinitialiser(self):
        """
        Réinitialise les attributs gérant les options.

        Returns
        -------
        None.

        """
        #Reinitialisation de la valeur de base des attributs des options
        self._joueur1.set(False)
        self._joueur2.set(False)
        self._troupesMax.set("49")
        self._casesNeutresNonAdjacentes.set(True)
        self._casesAdversesNonAdjacentes.set(False)

    def nouvellePartie(self):
        """
        Fais passer la fenêtre de son état de base à son état de choix
        d'options en cachant les widgets présent à l'écran et en initialisant
        ceux permettant à l'utlisateur de modifier le paramétrage de la partie.

        Returns
        -------
        None.

        """
        #Les boutons présents sont cachés
        self.boutonNouvellePartie.grid_remove()
        self.boutonImporterPartie.grid_remove()
        self.boutonRegles.grid_remove()
        self.boutonQuitter.grid_remove()

        #Initialisation des attributs qui représentent un élément visible fixe de la fenêtre
        self.texteJoueur1 = tk.Label(self.fenetre, text="Remplacement du joueur 1 par une IA :", fg="black")
        self.texteJoueur1.grid(row=0, column=0, columnspan=7)
        self.checkboxJoueur1 = tk.Checkbutton(self.fenetre, text="", variable=self._joueur1, onvalue=True, offvalue=False, fg="black")
        self.checkboxJoueur1.grid(row=0, column=8, columnspan=3)
        self.texteJoueur2 = tk.Label(self.fenetre, text="Remplacement du joueur 2 par une IA :", fg="black")
        self.texteJoueur2.grid(row=1, column=0, columnspan=7)
        self.checkboxJoueur2 = tk.Checkbutton(self.fenetre, text="", variable=self._joueur2, onvalue=True, offvalue=False, fg="black")
        self.checkboxJoueur2.grid(row=1, column=8, columnspan=3)
        self.texteTroupesMax = tk.Label(self.fenetre, text="Nombre maximal de troupes possédées simulanément par chaque joueur :\n(Peut être dépassé uniquement grâce à l'influence)", fg="black")
        self.texteTroupesMax.grid(row=2, column=0, columnspan=7)
        self.boutonRetirerTroupe = tk.Button(self.fenetre, text="-", command=lambda: self._troupesMax.set(str(int(self._troupesMax.get())-1)) if int(self._troupesMax.get()) > 0 else None)
        self.boutonRetirerTroupe.grid(row=2, column=8)
        self.entreeTroupes = tk.Entry(self.fenetre, textvariable=self._troupesMax, justify="center")
        self.entreeTroupes.grid(row=2, column=9)
        self.boutonAugmenterTroupe = tk.Button(self.fenetre, text="+", command=lambda: self._troupesMax.set(str(int(self._troupesMax.get())+1)))
        self.boutonAugmenterTroupe.grid(row=2, column=10)
        self.texteCasesNeutresNonAdjacentes = tk.Label(self.fenetre, text="Possiblité pour un joueur de déplacer ses troupes sur n'importe quelle case neutre adjacente à une de ses cases :\n(Plutôt que sur une case neutre adjacente à la case de départ des troupes)", fg="black")
        self.texteCasesNeutresNonAdjacentes.grid(row=3, column=0, columnspan=7)
        self.checkboxCasesNeutresNonAdjacentes = tk.Checkbutton(self.fenetre, text="", variable=self._casesNeutresNonAdjacentes, onvalue=True, offvalue=False, fg="black")
        self.checkboxCasesNeutresNonAdjacentes.grid(row=3, column=8, columnspan=3)
        self.texteCasesAdversesNonAdjacentes = tk.Label(self.fenetre, text="Possiblité pour un joueur de déplacer ses troupes sur n'importe quelle case adverse adjacente à une de ses cases :\n(Plutôt que sur une case adverse adjacente à la case de départ des troupes)", fg="black")
        self.texteCasesAdversesNonAdjacentes.grid(row=4, column=0, columnspan=7)
        self.checkboxCasesAdversesNonAdjacentes = tk.Checkbutton(self.fenetre, text="", variable=self._casesAdversesNonAdjacentes, onvalue=True, offvalue=False, fg="black")
        self.checkboxCasesAdversesNonAdjacentes.grid(row=4, column=9, columnspan=3)
        self.boutonRetour = tk.Button(self.fenetre, text="Retour", command=self.retour)
        self.boutonRetour.grid(row=5, column=0, columnspan=3)
        self.boutonLancerPartie = tk.Button(self.fenetre, text="Jouer", command=self.demarrerPartie)
        self.boutonLancerPartie.grid(row=5, column=4, columnspan=3)
        self.boutonReinitialiser = tk.Button(self.fenetre, text="Réinitialiser les options", command=self.reinitialiser)
        self.boutonReinitialiser.grid(row=5, column=8, columnspan=3)

    def demarrerPartie(self):
        """
        Ferme la fenêtre et démarre une partie avec les paramètres choisis par
        l'utilisateur en créant un objet de type InfosDePartie et un objet de
        type FenetreDeJeu adaptés.
        Cette fonction est appelée quand une nouvelle partie est lancée,
        lorsque la fenêtre est dans son état de choix d'options.

        A noter que la fenêtre est fermée avec la méthode destroy et non quit
        comme dans la plupart des autres méthodes car quit ne ferme pas la
        fenêtre lorsque une instance tkinter reste ouverte.

        Returns
        -------
        None.

        """
        self.fenetre.destroy()
        self._infos = InfosDePartie(nombreDeTroupesMax=int(self._troupesMax.get()), casesNeutresNonAdjacentes=self._casesNeutresNonAdjacentes.get(), casesAdversesNonAdjacentes=self._casesAdversesNonAdjacentes.get())
        FenetreDeJeu(infos=self._infos, etatJoueur1="joueur" if self._joueur1.get() == False else "IA", IAJoueur1=IA("Joueur 1", self._infos), etatJoueur2="joueur" if self._joueur2.get() == False else "IA", IAJoueur2=IA("Joueur 2", self._infos))
        self.demarrage()

    def importerPartie(self):
        """
        Laisse l'utilisateur choisir une partie à importer puis ferme la
        fenêtre et démarre une partie avec les paramètres de la sauvegarde
        sélectionnée en créant un objet de type InfosDePartie où les
        informations de la sauvegarde sont stockés et un objet de
        type FenetreDeJeu adapté.
        Cette fonction est appelée quand une partie importée est lancée,
        lorsque la fenêtre est dans son état de base.

        A noter que la fenêtre est fermée avec la méthode destroy et non quit
        comme dans la plupart des autres méthodes car quit ne ferme pas la
        fenêtre lorsque une instance tkinter reste ouverte.

        Returns
        -------
        None.

        """
        self._infos = InfosDePartie(nouvellePartie=False)
        self._infos.importerSauvegarde(fenetre=self.fenetre)
        self.fenetre.destroy()
        FenetreDeJeu(infos=self._infos, etatJoueur1="joueur", IAJoueur1=IA("Joueur 1", self._infos), etatJoueur2="joueur", IAJoueur2=IA("Joueur 2", self._infos))
        self.demarrage()

    def regles(self):
        """
        Ouvre une fenêtre dans laquelle sont inscrites les règles du Kanze.

        Returns
        -------
        None.

        """
        with open(os.path.dirname(__file__)+"/Regles.txt", "r", encoding="utf-8") as fichierRegles:
            texteRegles = fichierRegles.read()
        fenetreRegles = tk.Toplevel(self.fenetre)
        fenetreRegles.title("Règles du jeu")
        texte = tk.Text(fenetreRegles, width=95, wrap="none")
        texte.grid(row=0, column=0)
        texte.insert("1.0", texteRegles)
        texte.configure(state="disabled")
        defilement = tk.Scrollbar(fenetreRegles, command=texte.yview)
        defilement.grid(row=0, column=1, sticky="ns")
        texte.configure(yscrollcommand=defilement.set)
        tk.Button(fenetreRegles, text="Quitter", command=fenetreRegles.quit).grid(row=1, column=0)
        fenetreRegles.mainloop()
        fenetreRegles.destroy()

    def quitter(self):
        """
        Quitte la boucle qui fait fonctionner les widgets, ce qui conduit à la
        fermeture de la fenêtre et à l'arrêt du programme.

        Returns
        -------
        None.

        """
        self.fenetre.quit()

class FenetreDeJeu:
    """
    Classe gérant la fenêtre de jeu et l'interaction entre l'utilisateur et
    les données.
    """
    def __init__(self, infos:InfosDePartie, etatJoueur1="joueur", IAJoueur1=None, etatJoueur2="joueur", IAJoueur2=None):
        """
        Constructeur créant une fenêtre servant d'interface de jeu et
        initialisant de nombreux attributs qui permettent la construction et
        l'interaction avec cette fenêtre.

        Parameters
        ----------
        infos : InfosDePartie
            Est un objet contenant toutes les données sur la partie et gérant
            leur utilisation et modification.
        etatJoueur1 : str, optional
            Indique si le joueur 1 est une IA ("IA") ou un utilisateur
            ("joueur").
            The default is "joueur".
        IAJoueur1 : IA, optional
            Objet de classe IA permettant au joueur 2 de jouer automatiquement.
            The default is None.
        etatJoueur2 : str, optional
            Indique si le joueur 2 est une IA ("IA") ou un utilisateur
            ("joueur").
            The default is "joueur".
        IAJoueur2 : IA, optional
            Objet de classe IA permettant au joueur 2 de jouer automatiquement.
            The default is None.

        Returns
        -------
        None.

        """
        #Création de la fenêtre
        self.fenetre = tk.Tk()
        self.fenetre.title("Kanzé")

        #Initialisation des attributs qui ne représentent pas un élément fixe de la fenêtre
        self.infos = infos
        self._etatJoueur1 = etatJoueur1
        self._etatJoueur2 = etatJoueur2
        self._IAJoueur1 = IAJoueur1
        self._IAJoueur2 = IAJoueur2
        self._recrutement = tk.StringVar()
        self._recrutement.set("0")
        self._tourDeplacement = 0
        self._casesDeplacement =[(), ()]
        self._indicationDeplacement = tk.StringVar()
        self._indicationDeplacement.set("de la case () à la case ()")
        self._indicationTour = tk.StringVar()
        self._indicationTour.set("Tour 1")
        self._joueur = "Joueur 1"
        self._troupesAEnvoyer = tk.StringVar()
        self._troupesAEnvoyer.set("1")
        self._representant = tk.BooleanVar()
        self._tourChange = tk.StringVar()

        #Initialisation des attributs qui représentent un élément fixe de la fenêtre
        self.zonePlateau = tk.Canvas(self.fenetre, width=350, height=650, bg='white')
        self.zonePlateau.grid(row=0, column=0, rowspan=15)
        self.zonePlateau.bind("<Button-1>", self.clic)
        tk.Label(self.fenetre, textvariable=self._indicationTour, fg="black").grid(row=0, column=1)
        self.boutonRegles = tk.Button(self.fenetre, text="Règles du jeu", command=self.regles)
        self.boutonRegles.grid(row=0, column=5)
        self.texteJoueur = tk.Label(self.fenetre, text="Choisissez une action Joueur 1 :", fg="black")
        self.texteJoueur.grid(row=1, column=1, columnspan=5)
        tk.Label(self.fenetre, text="Déplacer ", fg="black").grid(row=2, column=1)
        self.boutonRetirerTroupe = tk.Button(self.fenetre, text="-", command=lambda: self._troupesAEnvoyer.set(str(int(self._troupesAEnvoyer.get())-1)) if int(self._troupesAEnvoyer.get()) > 0 else None)
        self.boutonRetirerTroupe.grid(row=2, column=2)
        self.entreeTroupes = tk.Entry(self.fenetre, textvariable=self._troupesAEnvoyer, justify="center")
        self.entreeTroupes.grid(row=2, column=3)
        self.boutonAugmenterTroupe = tk.Button(self.fenetre, text="+", command=lambda: self._troupesAEnvoyer.set(str(int(self._troupesAEnvoyer.get())+1)) if int(self._troupesAEnvoyer.get()) < 7 else None)
        self.boutonAugmenterTroupe.grid(row=2, column=4)
        tk.Label(self.fenetre, text=" troupes", fg="black").grid(row=2, column=5)
        tk.Label(self.fenetre, textvariable=self._indicationDeplacement, fg="black").grid(row=3, column=1, columnspan=5)
        self.checkboxRepresentant = tk.Checkbutton(self.fenetre, text="Envoyer le Représentant", variable=self._representant, onvalue=True, offvalue=False, state="disabled", fg="black")
        self.checkboxRepresentant.grid(row=4, column=1, columnspan=5)
        self.boutonDeplacer = tk.Button(self.fenetre, text="Déplacer", state="disabled", command=lambda: self.action(lambda: self.infos.deplacement(self._casesDeplacement[0], self._casesDeplacement[1], int(self._troupesAEnvoyer.get()), self._representant.get())))
        self.boutonDeplacer.grid(row=5, column=3)
        self.boutonRecruter = tk.Button(self.fenetre, text="Recruter", command=lambda: self.action(self.infos.recrutement))
        self.boutonRecruter.grid(row=6, column=3)
        self.boutonPasser = tk.Button(self.fenetre, text="Passer le tour", command=lambda:(self.infos.passerTour(), self.finDuTour()))
        self.boutonPasser.grid(row=7, column=2, columnspan=3)
        self.texteRecrutement = tk.Label(self.fenetre, text="Vous possédez trop de troupes pour recruter sur toutes vos cases, sélectionnez-en", fg="black")
        self.texteRecrutement.grid(row=8, column=1, columnspan=4)
        self.texteRecrutement.grid_remove()
        self.casesRecrutementRestantes = tk.Label(self.fenetre, textvariable=self._recrutement, fg="black")
        self.casesRecrutementRestantes.grid(row=8, column=5)
        self.casesRecrutementRestantes.grid_remove()
        self.texteErreur = tk.Label(self.fenetre, text="Erreur", fg="red")
        self.texteErreur.grid(row=9, column=1, columnspan=5)
        self.texteErreur.grid_remove()
        self.boutonTourPrecedent = tk.Button(self.fenetre, text="Tour précédent", state="disabled", command=lambda: self.action(lambda: self.infos.changementTour(self.infos.tour-1)))
        self.boutonTourPrecedent.grid(row=10, column=1, columnspan=2)
        self.boutonTourSuivant = tk.Button(self.fenetre, text="Tour suivant", state="disabled", command=lambda: self.action(lambda: self.infos.changementTour(self.infos.tour+1)))
        self.boutonTourSuivant.grid(row=10, column=4, columnspan=2)
        tk.Label(self.fenetre, text="Aller directement au tour :", fg="black").grid(row=11, column=1,columnspan=3)
        self.entreeChangementTour = tk.Entry(self.fenetre, textvariable=self._tourChange, justify="center")
        self.entreeChangementTour.grid(row=11, column=4)
        self.boutonChangementTour = tk.Button(self.fenetre, text="Valider", command=lambda: self.action(lambda: self.infos.changementTour(int(self._tourChange.get()))))
        self.boutonChangementTour.grid(row=11, column=5)
        self.boutonSauvegarder = tk.Button(self.fenetre, text="Sauvegarder", command=lambda: self.infos.sauvegarder(self.fenetre))
        self.boutonSauvegarder.grid(row=13, column=1, columnspan=2)
        self.boutonImporterSauvegarde = tk.Button(self.fenetre, text="Importer une sauvegarde", command=lambda: self.action(lambda: self.infos.importerSauvegarde(self.fenetre)))
        self.boutonImporterSauvegarde.grid(row=13, column=4, columnspan=2)
        self.boutonQuitter = tk.Button(self.fenetre, text="Quitter", command=self.fenetre.quit)
        self.boutonQuitter.grid(row=14, column=3)

        #Crétion des cases du plateau
        self.formationCase()
        #Début de la boucle durant laquelle on peut interagir avec la fenêtre
        self.fenetre.mainloop()
        #Destruction de la fenêtre lorsque la boucle s'est finie
        self.fenetre.destroy()

    def formationCase(self):
        """
        Parcours les infos du tour et pour chaque case trouvée, la trace selon
        ses coordonnées dans le canvas, puis la colore en fonction de son
        propriétaire, ajoute un trait noir pour chaque troupe sur la case et,
        si il est présent, un trait rouge pour le Représentant.

        Returns
        -------
        None.

        """
        for case in self.infos[self.infos.tour].keys():
            if type(self.infos[self.infos.tour][case]) == dict:
                if self.infos[self.infos.tour][case]["Proprietaire"] == "Joueur 1":
                    self.zonePlateau.create_oval(self.infos[self.infos.tour][case]["Coordonnees"][0], self.infos[self.infos.tour][case]["Coordonnees"][1], self.infos[self.infos.tour][case]["Coordonnees"][2], self.infos[self.infos.tour][case]["Coordonnees"][3], fill="#20f029", width=1)
                    for i in range (0, self.infos[self.infos.tour][case]["Troupes"]):
                        self.zonePlateau.create_rectangle(self.infos[self.infos.tour][case]["Coordonnees"][0]+3+i*7, self.infos[self.infos.tour][case]["Coordonnees"][1]+21, self.infos[self.infos.tour][case]["Coordonnees"][2]-3-(6-i)*7, self.infos[self.infos.tour][case]["Coordonnees"][3]-21, fill="black", width=0)
                    if self.infos[self.infos.tour][case]["Representant"] == True:
                        self.zonePlateau.create_rectangle(self.infos[self.infos.tour][case]["Coordonnees"][0]+23, self.infos[self.infos.tour][case]["Coordonnees"][1]+6, self.infos[self.infos.tour][case]["Coordonnees"][2]-23, self.infos[self.infos.tour][case]["Coordonnees"][3]-36, fill="red", width=0)
                elif self.infos[self.infos.tour][case]["Proprietaire"] == "Joueur 2":
                    self.zonePlateau.create_oval(self.infos[self.infos.tour][case]["Coordonnees"][0], self.infos[self.infos.tour][case]["Coordonnees"][1], self.infos[self.infos.tour][case]["Coordonnees"][2], self.infos[self.infos.tour][case]["Coordonnees"][3], fill="#2bcfff", width=1)
                    for i in range (0, self.infos[self.infos.tour][case]["Troupes"]):
                        self.zonePlateau.create_rectangle(self.infos[self.infos.tour][case]["Coordonnees"][0]+3+i*7, self.infos[self.infos.tour][case]["Coordonnees"][1]+21, self.infos[self.infos.tour][case]["Coordonnees"][2]-3-(6-i)*7, self.infos[self.infos.tour][case]["Coordonnees"][3]-21, fill="black", width=0)
                    if self.infos[self.infos.tour][case]["Representant"] == True:
                        self.zonePlateau.create_rectangle(self.infos[self.infos.tour][case]["Coordonnees"][0]+23, self.infos[self.infos.tour][case]["Coordonnees"][1]+36, self.infos[self.infos.tour][case]["Coordonnees"][2]-23, self.infos[self.infos.tour][case]["Coordonnees"][3]-6, fill="red", width=0)
                else:
                    self.zonePlateau.create_oval(self.infos[self.infos.tour][case]["Coordonnees"][0], self.infos[self.infos.tour][case]["Coordonnees"][1], self.infos[self.infos.tour][case]["Coordonnees"][2], self.infos[self.infos.tour][case]["Coordonnees"][3], fill="#fff", width=1)

    def regles(self):
        """
        Ouvre une fenêtre dans laquelle sont inscrites les règles du Kanze.

        Returns
        -------
        None.

        """
        with open(os.path.dirname(__file__)+"/Regles.txt", "r", encoding="utf-8") as fichierRegles:
            texteRegles = fichierRegles.read()
        fenetreRegles = tk.Toplevel(self.fenetre)
        fenetreRegles.title("Règles du jeu")
        texte = tk.Text(fenetreRegles, width=95, wrap="none")
        texte.grid(row=0, column=0)
        texte.insert("1.0", texteRegles)
        texte.configure(state="disabled")
        defilement = tk.Scrollbar(fenetreRegles, command=texte.yview)
        defilement.grid(row=0, column=1, sticky="ns")
        texte.configure(yscrollcommand=defilement.set)
        tk.Button(fenetreRegles, text="Quitter", command=fenetreRegles.quit).grid(row=1, column=0)
        fenetreRegles.mainloop()
        fenetreRegles.destroy()

    def action(self, fonction):
        """
        Sert d'intermédiaire entre les méthodes de l'objet de type
        InfosDePartie et la fenêtre. Cette méthode gère notamment le passage
        de la fenêtre à son état de recrutement à la case, l'actualisation de
        la fenêtre en fonction des infos de jeu si nécessaire, l'affichage des
        éventuelles notifications d'erreurs et l'appel à la méthode finDuTour
        si aucune notification n'est reçue.

        Parameters
        ----------
        fonction : function
            Fonction à exécuter.

        Returns
        -------
        None.

        """
        #Récupération de l'éventuelle notification renvoyée par la fonction à exécuter
        notification = fonction()
        #Si la notification est le nombre de troupes à recruter, passage de la fenêtre dans son état de recrutement à la case
        if fonction == self.infos.recrutement and type(notification) == int:
            self._recrutement.set(notification)
            self.texteRecrutement.grid()
            self.casesRecrutementRestantes.grid()
            #Désactivation de toutes les autres actions possibles à l'exeption de la consultation des règles et du bouton Quitter
            self.boutonDeplacer.config(state="disabled")
            self.boutonRecruter.config(state="disabled")
            self.boutonPasser.config(state="disabled")
            self.boutonTourPrecedent.config(state="disabled")
            self.boutonTourSuivant.config(state="disabled")
            self.boutonChangementTour.config(state="disabled")
            self.boutonSauvegarder.config(state="disabled")
        #Si la notification est la chaîne de caractère "Actualisation", la fenêtre est actualisée selon les infos du tour actuel
        elif notification == "Actualisation":
            #Mise à jour des indications visuelles
            self.formationCase()
            self._indicationTour.set("Tour {}".format(str(self.infos.tour)))
            #Vérification du joueur actif à partir du numéro du tour
            if self.infos.tour%2 == 0:
                self._joueur = "Joueur 2"
            else:
                self._joueur = "Joueur 1"
            #Réinitialisation des attributs changeant en fonction des infos du tour actuel
            self.texteJoueur.config(text="Choisissez une action {} :".format(self._joueur))
            self._troupesAEnvoyer.set("1")
            self._tourDeplacement = 0
            self._casesDeplacement =[(), ()]
            self._representant.set(False)
            self.checkboxRepresentant.config(state="disabled")
            self._indicationDeplacement.set("de la case () à la case ()")
            self.boutonDeplacer.config(state="disabled")
            self.boutonRecruter.config(state="normal")
            self.boutonPasser.config(state="normal")
            self.texteRecrutement.grid_remove()
            self.casesRecrutementRestantes.grid_remove()
            self._casesRecrutement = []
            self.texteErreur.grid_remove()
            if self.infos.tour == 1:
                self.boutonTourPrecedent.config(state="disabled")
            else:
                self.boutonTourPrecedent.config(state="normal")
            if self.infos.tour >= len(self.infos)-2:
                self.boutonTourSuivant.config(state="disabled")
            else:
                self.boutonTourSuivant.config(state="normal")
            self.boutonChangementTour.config(state="normal")
            self.boutonSauvegarder.config(state="normal")
            self.boutonImporterSauvegarde.config(state="normal")
        #Si la notification est une erreur, elle est affichée dans la fenêtre
        elif notification != None:
            self.texteErreur.config(text=notification)
            self.texteErreur.grid()
        #Si aucune notification n'est reçue, il est considéré qu'une action a été jouée et on passe à la fin du tour
        else:
            self.finDuTour()

    def finDuTour(self):
        """
        Gère la mise à jour des infos de jeu à la fin d'un tour, ce qui
        comprend l'influence, le compte des troupes et évidemment le passage
        au tour suivant, met à jour les indications visuelles en fonction des
        infos de jeu, vérifie que les conditions de fin de partie ne sont pas
        remplies et gère le lancement du tour d'une IA si nécessaire.

        Returns
        -------
        None.

        """
        #Le tour est incrémenté de manière à faire les modifications de fin de tour sur le tour suivant et de pouvoir ainsi revenir en arrière jusqu'au tour 1. Sans cette mesure, le tour vierge du début de partie n'est pas enregistré.
        self.infos.tour += 1
        representantJ1 = False
        representantJ2 = False
        for case in self.infos[self.infos.tour].keys():
            if type(self.infos[self.infos.tour][case]) == dict and type(case) == tuple:
                #Vérification de la présence d'un Représentant pour chaque joueur
                if self.infos[self.infos.tour][case]["Proprietaire"] == "Joueur 1" and self.infos[self.infos.tour][case]["Representant"] == True:
                    representantJ1 = True
                elif self.infos[self.infos.tour][case]["Proprietaire"] == "Joueur 2" and self.infos[self.infos.tour][case]["Representant"] == True:
                    representantJ2 = True
                #Toutes les cases sans troupes ni Représentant deviennent neutres
                if self.infos[self.infos.tour][case]["Troupes"] == 0 and self.infos[self.infos.tour][case]["Representant"] == False:
                    self.infos[self.infos.tour][case]["Proprietaire"] = "Neutre"
        #Vérification de l'influence
        self.infos.influence()
        #Ajout aux infos de jeu du prochain tour, pour l'instant identique à l'actuel
        self.infos.ajoutTour()
        #Compte des troupes et des cases de chaque joueur
        self.infos[self.infos.tour]["nombreTroupes", "Joueur 1"] = 0
        self.infos[self.infos.tour]["nombreCases", "Joueur 1"] = 0
        self.infos[self.infos.tour]["nombreTroupes", "Joueur 2"] = 0
        self.infos[self.infos.tour]["nombreCases", "Joueur 2"] = 0
        for case in self.infos[self.infos.tour].keys():
            if type(self.infos[self.infos.tour][case]) == dict and type(case) == tuple:
                if self.infos[self.infos.tour][case]["Proprietaire"] == "Joueur 1":
                    self.infos[self.infos.tour]["nombreTroupes", "Joueur 1"] += self.infos[self.infos.tour][case]["Troupes"]
                    self.infos[self.infos.tour]["nombreCases", "Joueur 1"] += 1
                elif self.infos[self.infos.tour][case]["Proprietaire"] == "Joueur 2":
                    self.infos[self.infos.tour]["nombreTroupes", "Joueur 2"] += self.infos[self.infos.tour][case]["Troupes"]
                    self.infos[self.infos.tour]["nombreCases", "Joueur 2"] += 1
        #Mise à jour des indications visuelles
        self.formationCase()
        self._indicationTour.set("Tour {}".format(str(self.infos.tour)))
        #Vérification du joueur actif à partir du numéro du tour
        if self.infos.tour%2 == 0:
            self._joueur = "Joueur 2"
        else:
            self._joueur = "Joueur 1"
        #Réinitialisation des attributs changeant en fonction des infos du tour
        self.texteJoueur.config(text="Choisissez une action {} :".format(self._joueur))
        self._troupesAEnvoyer.set("1")
        self._tourDeplacement = 0
        self._casesDeplacement =[(), ()]
        self._representant.set(False)
        self.checkboxRepresentant.config(state="disabled")
        self._indicationDeplacement.set("de la case () à la case ()")
        self.boutonDeplacer.config(state="disabled")
        self.boutonRecruter.config(state="normal")
        self.boutonPasser.config(state="normal")
        self.texteRecrutement.grid_remove()
        self.casesRecrutementRestantes.grid_remove()
        self._casesRecrutement = []
        self.texteErreur.grid_remove()
        if self.infos.tour == 1:
            self.boutonTourPrecedent.config(state="disabled")
        else:
            self.boutonTourPrecedent.config(state="normal")
        self.boutonChangementTour.config(state="normal")
        self.boutonSauvegarder.config(state="normal")
        self.boutonImporterSauvegarde.config(state="normal")
        #Vérification des conditions de fin de partie
        if representantJ1 == False and representantJ2 == False:
            self.texteJoueur.config(text="Partie terminée, match nul !\n")
            self.infos[0]["indicationPartie"] = 3
            self.infos.sauvegarder(self.fenetre, os.path.dirname(__file__)+"/Sauvegardes"+"/Auto/"+time.strftime("%d-%m-%Y_%H%M%S")+".kan")
        elif representantJ1 == False:
            self.texteJoueur.config(text="Partie terminée, victoire du Joueur 2 !\n")
            self.infos[0]["indicationPartie"] = 2
            self.infos.sauvegarder(self.fenetre, os.path.dirname(__file__)+"/Sauvegardes"+"/Auto/"+time.strftime("%d-%m-%Y_%H%M%S")+".kan")
        elif representantJ2 == False:
            self.texteJoueur.config(text="Partie terminée, victoire du Joueur 1 !\n")
            self.infos[0]["indicationPartie"] = 1
            self.infos.sauvegarder(self.fenetre, os.path.dirname(__file__)+"/Sauvegardes"+"/Auto/"+time.strftime("%d-%m-%Y_%H%M%S")+".kan")
        #Si la partie n'est pas terminée et que c'est au tour d'une IA de jouer, celle-ci joue et une procédure de fin de tour est à nouveau appelée
        else:
            if self._joueur == "Joueur 1" and self._etatJoueur1 == "IA":
                self._IAJoueur1.choixAction()
                self.finDuTour()
            elif self._joueur == "Joueur 2" and self._etatJoueur2 == "IA":
                self._IAJoueur2.choixAction()
                self.finDuTour()

    def clic(self, event):
        """
        Est appelée lorsque l'utilisateur clique sur le plateau.
        Cette méthode identifie la case sur laquelle l'utilisateur a cliqué et
        effectue l'action qui en découle, soit la sélection d'une case sur
        laquelle recruter s'il faut recruter des troupes ou la sélection et
        l'affichage d'une case de départ ou d'arrivée d'un déplacement dans
        les autres cas.

        Parameters
        ----------
        event : Event
            Objet dérivant les circonstance du clic, ici il sert à connaître
            son abscisse et son ordonnée.

        Returns
        -------
        None.

        """
        #Identification de la case où l'utilisateur a cliqué si s'en est une
        case = self.correspondanceCase(event.x, event.y)
        #Recrutement sur la case si il y a des troupes à recruter
        if self._recrutement.get() != "0" and case != None:
            erreur = self.infos.recrutementALaCase(self._joueur, case)
            if erreur != None:
                self.texteErreur.config(text=erreur)
                self.texteErreur.grid()
            else:
                self._recrutement.set(str(int(self._recrutement.get())-1))
                if self._recrutement.get() == "0":
                    self.finDuTour()
        #Sinon, sélection de la case en temps que case de départ ou d'arrivée d'un déplacement et mise à jour des éléments affichés en fonction
        elif case != None:
            self._casesDeplacement[self._tourDeplacement] = case
            self._indicationDeplacement.set("de la case {} à la case {}".format(str(self._casesDeplacement[0]), str(self._casesDeplacement[1])))
            if self._tourDeplacement == 0:
                if self.infos[self.infos.tour][case]["Representant"] == True:
                    self.checkboxRepresentant.config(state="normal")
                self._tourDeplacement = 1
            else:
                self._tourDeplacement = 0
                self.boutonDeplacer.config(state="normal")

    def correspondanceCase(self, x:int, y:int):
        """
        Renvoie la case sur laquelle a cliqué l'utilisateur.

        Parameters
        ----------
        x : int
            Abscisse sur le repère d'un canvas du pointeur de la souris de
            l'utilisateur au moment où il a cliqué.
        y : int
            Ordonnée sur le repère d'un canvas du pointeur de la souris de
            l'utilisateur au moment où il a cliqué.

        Returns
        -------
        case : tuple
            Coordonnées de la case sur laquelle l'utilisateur a cliqué.

        """
        for case in self.infos[self.infos.tour].keys():
            if type(self.infos[self.infos.tour][case]) == dict and type(case) == tuple:
                if self.infos[self.infos.tour][case]["Coordonnees"][0] < x and self.infos[self.infos.tour][case]["Coordonnees"][2] > x and self.infos[self.infos.tour][case]["Coordonnees"][1] < y and self.infos[self.infos.tour][case]["Coordonnees"][3] > y:
                    return case

class IA:
    def __init__(self, joueur:str, infos:InfosDePartie):
        """
        Constructeur intégrant le joueur remplacé par l'IA et les infos de la
        partie correspondante et effectuant un premier tri entre les parties
        enregistrées à partir de ces données.

        Parameters
        ----------
        joueur : str
            Numéro du joueur actuel.
        infos : InfosDePartie
            Objet contenant les infos de jeu.

        Returns
        -------
        None.

        """
        self._joueur = joueur
        self._infos = infos
        self._partiesCompatibles = self.evaluationParties(chemin=os.path.dirname(__file__)+"/Sauvegardes")

    def evaluationParties(self, chemin:str):
        """
        Vérifie si le chemin donné est celui d'un fichier ou non. Si c'est le
        cas, vérifie si c'est une sauvegarde valide, c'est à dire dont les
        paramètres sont les mêmes que ceux de la partie en cours, et lui
        attribue un score en fonction de l'indication de fin de partie et du
        nombre de tours. Si le chemin pointe sur un dossier, exécute de façon
        récursive cette méthode sur tous les fichiers et dossiers du dossier.

        Parameters
        ----------
        chemin : str
            Chemin qui doit être testé et évalué.

        Returns
        -------
        fichiersCompatibles : list
            Liste de tuples représentant le chemin d'une sauvegarde compatible
            et le score qui lui est associé.

        """
        fichiersCompatibles = []
        #Il est vérifie que le chemin pointe sur un fichier
        if os.path.isfile(chemin) == False:
            for composant in os.listdir(chemin):
                fichiersCompatibles += self.evaluationParties(chemin+"/"+composant)
        elif os.path.splitext(chemin)[1] == ".kan":
            with open(chemin, "r") as fichierTeste:
                elementsTeste = fichierTeste.read().split("\n")[:2]
            # Verification de la validite et de la compatibilite de la sauvegarde
            try:
                elementsTeste[0] = {key:int(value) if key=='nombreDeTroupesMax' else value if key=='indicationPartie' else value=="True" for key, value in [i.split(";") for i in elementsTeste[0].split("/")]}
                parametresIdentiques = True
                for cle in elementsTeste[0]:
                    if cle != "indicationPartie" and elementsTeste[0][cle] != self._infos[0][cle]:
                        parametresIdentiques = False
                        break
                if parametresIdentiques == True:
                   nombreTours = int(elementsTeste[1])
                   score = 1 - nombreTours//1000/5
                   nombreTours -= nombreTours//1000
                   while nombreTours > 300 and score >= 0.1:
                       score -= 0.1
                       nombreTours -= 100
                   score = (score + {"0":0.5, "1":1 if self._joueur == "Joueur 1" else 0.1, "2":1 if self._joueur == "Joueur 2" else 0.1, "3":0.6}[elementsTeste[0]["indicationPartie"]]*2) / 3
                   fichiersCompatibles.append((chemin, score))
            except ValueError:
                pass
        return fichiersCompatibles

    def triTour(self, compatibiliteMin:int=0.6):
        """
        Sélectionne les tours ressemblant suffisamment au tour actuel, leur
        attribue un score et renvoie une liste des actions qui y ont été
        jouées, triée en fonction de leurs scores.

        Parameters
        ----------
        compatibilite : int, optional
            Limite minimum du score de compatibilité qu'un tour peut atteindre
            pour être sélectionné.
            The default is 0.5.

        Returns
        -------
        actionsCompatibles : list
            Liste de tuples contenant le score de compatibilité d'un tour et
            l'action qui y a été jouée. Elle est triée en fonction du score
            dans l'ordre décroissant.

        """
        actionsCompatibles = []
        for fichier in self._partiesCompatibles:
            with open(fichier[0], "r") as fichierOuvert:
                #Création d'une liste comportant tous les tours de la partie
                partie = fichierOuvert.read().split("\n")[2:-2]
            #Attibution d'un score au tour dépendant de sa ressemblance avec l'état de la partie actuelle
            for i in range(0, len(partie)):
                if float(partie[i][0]) >= 0:
                    scoreCompatibilite = 1
                    partie[i] = partie[i].split("/")[5:]
                    j = 2
                    #Vérification de la correspondance pour toutes les cases du tour
                    while j in range(2, len(partie[i])) and scoreCompatibilite >= compatibiliteMin:
                        partie[i][j] = partie[i][j].split(";")
                        partie[i][j][0] = (int(partie[i][j][0].split(",")[0]), int(partie[i][j][0].split(",")[1]))
                        #Vérification du propriétaire
                        if partie[i][j][1] != self._infos[self._infos.tour][partie[i][j][0]]["Proprietaire"]:
                            scoreCompatibilite -= 0.1
                        else:
                            #Vérification de la présence du Représentant si la case appartient bien au même propriétaire, sinon cette information n'est pas représentative
                            if (partie[i][j][3] == "True") != self._infos[self._infos.tour][partie[i][j][0]]["Representant"]:
                                scoreCompatibilite -= 0.025
                            #Vérification du nombre de troupes si la case appartient bien au même propriétaire, sinon cette information n'est pas représentative
                            if int(partie[i][j][2]) < self._infos[self._infos.tour][partie[i][j][0]]["Troupes"]:
                                for k in range (0, self._infos[self._infos.tour][partie[i][j][0]]["Troupes"]-int(partie[i][j][2])):
                                    scoreCompatibilite -= 0.01
                            elif int(partie[i][j][2]) > self._infos[self._infos.tour][partie[i][j][0]]["Troupes"]:
                                for k in range (0, int(partie[i][j][2])-self._infos[self._infos.tour][partie[i][j][0]]["Troupes"]):
                                    scoreCompatibilite -= 0.01
                        j+=1
                    #Si le score attribué au tour est supérieur au minimum requis, le score total du tour est calculé
                    #à partir du score de la partie, du score du tour et du score de compatibilité et l'action du tour est convertie et ajoutée à la liste des actions possibles
                    if scoreCompatibilite >= compatibiliteMin:
                        # Conversion de l'action du tour
                        partie[i][1] = partie[i][1].split(";")
                        if partie[i][1][0] == "recruterCase":
                            for k in range (1, len(partie[i][1])):
                                partie[i][1][k] = (int(partie[i][1][k].split(",")[0]), int(partie[i][1][k].split(",")[1]))
                        elif partie[i][1][0] == "deplacer":
                            partie[i][1][1] = (int(partie[i][1][1].split(",")[0]), int(partie[i][1][1].split(",")[1]))
                            partie[i][1][2] = (int(partie[i][1][2].split(",")[0]), int(partie[i][1][2].split(",")[1]))
                            partie[i][1][3] = int(partie[i][1][3])
                            partie[i][1][4] = partie[i][1][4]=="True"
                        #Calcul du score total et ajout de l'action du tour pondérée dans les actions compatibles avec le tour actuel
                        actionsCompatibles.append((float(partie[i][0])*fichier[1]*scoreCompatibilite, partie[i][1]))
        actionsCompatibles.sort(reverse=True)
        return actionsCompatibles

    def actionAleatoire(self):
        #Création d'une liste de coups possibles entre un déplacement, un recrutement et un passage de tour
        #Parmi les coups possible, 5 seront des déplacements. Le chiffre 5 est une valeur arbitraire qui me semble simplement être un bon ratio par rapport aux nombres des autres actions et peut-être à corriger.
        listeCoups = ["deplacer" for i in range (0, 5)]
        #Sélection des cases du joueur durant le tour actuel
        casesJoueur = []
        for case in self._infos[self._infos.tour]:
            if type(case) == tuple and type(self._infos[self._infos.tour][case]) == dict:
                if self._infos[self._infos.tour][case]["Proprietaire"] == self._joueur:
                    casesJoueur.append(case)
        #Parmi les coups possibles, le nombre de recrutements varie entre 0 et 7 selon le nombre de troupes du joueur remplacé par l'IA et le rapport entre son nombre de troupes et son nombre de cases possédées
        if self._infos[self._infos.tour][("nombreTroupes", self._joueur)] < self._infos[0]["nombreDeTroupesMax"]:
            for i in range (0, 7-self._infos[self._infos.tour][("nombreTroupes", self._joueur)] // len(casesJoueur)):
                listeCoups.append("recruter")
        #Si le nombre de troupes du joueur remplacé par l'IA est supérieur à 44 et qu'il y a en moyenne 6 troupes minimum par case, un coup possible est un passage de tour
        if self._infos[self._infos.tour][("nombreTroupes", self._joueur)] >= self._infos[0]["nombreDeTroupesMax"]-4 and self._infos[self._infos.tour][("nombreTroupes", self._joueur)] // len(casesJoueur) >= 6:
            listeCoups.append("passer")
        #Un coup est chosi et exécuté parmi ceux possibles
        action = listeCoups[random.randint(0, len(listeCoups)-1)]
        if action == "deplacer":
            #Choix de la case de départ
            caseDepart = casesJoueur[random.randint(0, len(casesJoueur)-1)]
            #Détermination de la case d'arrivée en fonction de la case de départ
            caseArrivee = random.choice(self.compatibiliteCaseArrivee(caseDepart))
            #Choix du nombre de troupes à déplacer
            if self._infos[self._infos.tour][caseDepart]["Troupes"] > 0:
                    nombreTroupes = random.randint(min(self._infos[self._infos.tour][caseDepart]["Troupes"], caseArrivee[1]), min(self._infos[self._infos.tour][caseDepart]["Troupes"], caseArrivee[2]))
            else:
                nombreTroupes = 0
            #Choix du déplacement du Représentant si il est présent sur la case de départ
            if self._infos[self._infos.tour][caseDepart]["Representant"] == True and nombreTroupes >= caseArrivee[1]:
                representant = random.choice((True, False))
            else:
                representant = False
            self._infos.deplacement(caseDepart, caseArrivee[0], nombreTroupes, representant)
        elif action == "recruter":
            #Sélection des cases où il est possible de recruter
            i = 0
            while i in range (0, len(casesJoueur)):
                if self._infos[self._infos.tour][casesJoueur[i]]["Troupes"] == 7:
                    del casesJoueur[i]
                else:
                    i += 1
            #Recrutement sur chaque case où il est possible de recruter jusqu'à ce que le nombre de troupes atteigne son maximum
            #ou qu'un recrutement ait été effectué sur toutes les cases où c'était possible
            if self._infos[self._infos.tour][('nombreTroupes', self._joueur)] + len(casesJoueur) > self._infos[0]["nombreDeTroupesMax"]:
                random.shuffle(casesJoueur)
                self._infos[self._infos.tour]["action"] = ["recruterCase"]
                i = 0
                while i in range (0, self._infos[0]["nombreDeTroupesMax"]-self._infos[self._infos.tour][('nombreTroupes', self._joueur)]) and i < len(casesJoueur):
                    self._infos.recrutementALaCase(self._joueur, casesJoueur[i])
                    i += 1
            else:
                self._infos[self._infos.tour]["action"] = "recruter"
                self._infos.recrutement()
        else:
            self._infos.passerTour()

    def compatibiliteCaseArrivee(self, caseDepart:tuple):
        """
        Renvoie la liste des cases d'arrivée possibles à partir d'une case de
        départ donnée. Chaque case d'arrivée possible se présente sous la
        forme d'un tuple comportant les coordonnées de la case, le nombre
        minimum de troupes à envoyer pour ne pas perdre et le nombre maximum
        de troupes à envoyer possible.

        Parameters
        ----------
        caseDepart : tuple
            Coordonnées de la case de départ du déplacement.

        Returns
        -------
        casesCompatibles : list
            Liste des cases d'arrivée possibles.

        """
        casesCompatibles = []
        casesVisitees = []
        file = [caseDepart]
        while file != []:
            #Si la case testée appartient au joueur remplacé par l'IA, chacune de ses cases adjacentes sont sélectionnées pour être testées
            #et, si ce n'est pas la case de départ, elle est est notée comme compatible avec comme nombre minimum de troupes à envoyer 1 et comme maximum le nombre de places qu'il y reste
            if self._infos[self._infos.tour][file[0]]["Proprietaire"] == self._joueur:
                for caseAdjacente in self._infos[self._infos.tour][file[0]]["CasesAdjacentes"]:
                    if caseAdjacente not in casesVisitees and caseAdjacente not in file:
                        file.append(caseAdjacente)
                if file[0] != caseDepart and self._infos[self._infos.tour][file[0]]["Troupes"] < 7:
                    casesCompatibles.append((file[0], 1, 7-self._infos[self._infos.tour][file[0]]["Troupes"]))
            #Si la case testée est neutre et si le déplacement y est possible, elle est est notée comme compatible avec comme nombre minimum de troupes à envoyer 1 et comme maximum 7
            elif self._infos[self._infos.tour][file[0]]["Proprietaire"] == "Neutre" and file[0] in self._infos[self._infos.tour][caseDepart]["CasesAdjacentes"] or self._infos[0]["casesNeutresNonAdjacentes"]:
                casesCompatibles.append((file[0], 1, 7))
            #Si la case testée appartient au joueur adverse et si le déplacement y est possible, elle est est notée comme compatible avec
            #comme nombre minimum de troupes à envoyer le nombre de troupes nécessaire pour faire nul lors de la bataille pour la case, tant que ce nombre ne dépasse pas 7, et comme maximum 7
            elif file[0] in self._infos[self._infos.tour][caseDepart]["CasesAdjacentes"] or self._infos[0]["casesAdversesNonAdjacentes"]:
                casesCompatibles.append((file[0], min(self._infos[self._infos.tour][file[0]]["Troupes"] + 1 if self._infos[self._infos.tour][file[0]]["Representant"] else self._infos[self._infos.tour][file[0]]["Troupes"], 7), 7))
            casesVisitees.append(file.pop(0))
        return casesCompatibles

    def choixAction(self, tourMinChoisi:int=10):
        """
        Exécute une action jugée compatible avec la situation jusqu'à ce
        qu'aucune erreur ne soit renvoyée. Si le numéro du tour actuel est
        inférieur au tour minimum choisi ou si aucune action n'est compatible,
        un coup alétoire est joué.

        Parameters
        ----------
        tourMinChoisi : int, optional
            Tour à partir duquel un coup non-aléatoire peut-être joué. Une
            limite est fixée pour éviter d'avoir éternellement les mêmes coups
            durant les premiers tours, où la situation est toujours la même et
            donc où les mêmes actions compatibles seront toujours
            sélectionnées.
            The default is 5.

        Returns
        -------
        None.

        """
        erreur = ""
        if self._infos.tour >= tourMinChoisi and random.randint(0, 100) != 0:
            actionsCompatibles = self.triTour()
            while erreur != None and actionsCompatibles != []:
                if actionsCompatibles[0][1][0] == "deplacer":
                    erreur = self._infos.deplacement(actionsCompatibles[0][1][1], actionsCompatibles[0][1][2], actionsCompatibles[0][1][3], actionsCompatibles[0][1][4])
                elif actionsCompatibles[0][1][0] == "recruter":
                    erreur = self._infos.recrutement()
                elif actionsCompatibles[0][1][0] == "recruterCase":
                    if self._infos[self._infos.tour][('nombreTroupes', self._joueur)] + len(actionsCompatibles[0][1][1:]) > self._infos[0]["nombreDeTroupesMax"]:
                        erreur = "Trop de troupes à recruter"
                    else:
                        erreur = None
                        for case in actionsCompatibles[0][1][1:]:
                            if self._infos[self._infos.tour][case]["Proprietaire"] != self._joueur or self._infos[self._infos.tour][case]["Troupes"] == 7:
                                erreur = "Cases non-conformes"
                                break
                        if erreur == None:
                            self._infos[self._infos.tour]["action"] = ["recruterCase"]
                            for case in actionsCompatibles[0][1][1:]:
                                self._infos.recrutementALaCase(self._joueur, case)
                else:
                    erreur = self._infos.passerTour()
                del actionsCompatibles[0]
        if erreur != None:
            self.actionAleatoire()

class IAAnalysee(IA):
    """
    Classe
    """
    def triTour(self, compatibiliteMin:int=0.6):
        """
        Sélectionne les tours ressemblant suffisamment au tour actuel, leur
        attribue un score et renvoie une liste des actions qui y ont été
        jouées, triée en fonction de leurs scores.

        Parameters
        ----------
        compatibilite : int, optional
            Limite minimum du score de compatibilité qu'un tour peut atteindre
            pour être sélectionné.
            The default is 0.5.

        Returns
        -------
        actionsCompatibles : list
            Liste de tuples contenant le score de compatibilité d'un tour,
            l'action qui y a été jouée et le fichier d'origine de l'action.
            Elle est triée en fonction du score dans l'ordre décroissant.
            Elle prend la forme [score, action, fichier d'origine, tour d'origine]

        """
        actionsCompatibles = []
        for fichier in self._partiesCompatibles:
            with open(fichier[0], "r") as fichierOuvert:
                #Création d'une liste comportant tous les tours de la partie
                partie = fichierOuvert.read().split("\n")[2:-2]
            #Attibution d'un score au tour dépendant de sa ressemblance avec l'état de la partie actuelle
            for i in range(0, len(partie)):
                if float(partie[i][0]) >= 0:
                    scoreCompatibilite = 1
                    tourTeste = partie[i].split("/")[0]
                    partie[i] = partie[i].split("/")[5:]
                    j = 2
                    #Vérification de la correspondance pour toutes les cases du tour
                    while j in range(2, len(partie[i])) and scoreCompatibilite >= compatibiliteMin:
                        partie[i][j] = partie[i][j].split(";")
                        partie[i][j][0] = (int(partie[i][j][0].split(",")[0]), int(partie[i][j][0].split(",")[1]))
                        #Vérification du propriétaire
                        if partie[i][j][1] != self._infos[self._infos.tour][partie[i][j][0]]["Proprietaire"]:
                            scoreCompatibilite -= 0.1
                        else:
                            #Vérification de la présence du Représentant si la case appartient bien au même propriétaire, sinon cette information n'est pas représentative
                            if (partie[i][j][3] == "True") != self._infos[self._infos.tour][partie[i][j][0]]["Representant"]:
                                scoreCompatibilite -= 0.025
                            #Vérification du nombre de troupes si la case appartient bien au même propriétaire, sinon cette information n'est pas représentative
                            if int(partie[i][j][2]) < self._infos[self._infos.tour][partie[i][j][0]]["Troupes"]:
                                for k in range (0, self._infos[self._infos.tour][partie[i][j][0]]["Troupes"]-int(partie[i][j][2])):
                                    scoreCompatibilite -= 0.01
                            elif int(partie[i][j][2]) > self._infos[self._infos.tour][partie[i][j][0]]["Troupes"]:
                                for k in range (0, int(partie[i][j][2])-self._infos[self._infos.tour][partie[i][j][0]]["Troupes"]):
                                    scoreCompatibilite -= 0.01
                        j+=1
                    #Si le score attribué au tour est supérieur au minimum requis, l'action du tour est convertie et ajoutée à la liste des actions possibles
                    if scoreCompatibilite >= compatibiliteMin:
                        # Conversion de l'action du tour
                        partie[i][1] = partie[i][1].split(";")
                        if partie[i][1][0] == "recruterCase":
                            for k in range (1, len(partie[i][1])):
                                partie[i][1][k] = (int(partie[i][1][k].split(",")[0]), int(partie[i][1][k].split(",")[1]))
                        elif partie[i][1][0] == "deplacer":
                            partie[i][1][1] = (int(partie[i][1][1].split(",")[0]), int(partie[i][1][1].split(",")[1]))
                            partie[i][1][2] = (int(partie[i][1][2].split(",")[0]), int(partie[i][1][2].split(",")[1]))
                            partie[i][1][3] = int(partie[i][1][3])
                            partie[i][1][4] = partie[i][1][4]=="True"
                        actionsCompatibles.append((float(partie[i][0])*fichier[1]*scoreCompatibilite, partie[i][1], fichier[0], tourTeste))
        actionsCompatibles.sort(reverse=True)
        return actionsCompatibles

    def choixAction(self, tourMinChoisi:int=10):
        """
        Exécute une action jugée compatible avec la situation jusqu'à ce
        qu'aucune erreur ne soit renvoyée. Si le numéro du tour actuel est
        inférieur au tour minimum choisi ou si aucune action n'est compatible,
        un coup alétoire est joué.

        Parameters
        ----------
        tourMinChoisi : int, optional
            Tour à partir duquel un coup non-aléatoire peut-être joué. Une
            limite est fixée pour éviter d'avoir éternellement les mêmes coups
            durant les premiers tours, où la situation est toujours la même et
            donc où les mêmes actions compatibles seront toujours
            sélectionnées.
            The default is 5.

        Returns
        -------
        None.

        """
        erreur = ""
        if self._infos.tour >= tourMinChoisi and random.randint(0, 100) != 0:
            actionsCompatibles = self.triTour()
            while erreur != None and actionsCompatibles != []:
                if actionsCompatibles[0][1][0] == "deplacer":
                    erreur = self._infos.deplacement(actionsCompatibles[0][1][1], actionsCompatibles[0][1][2], actionsCompatibles[0][1][3], actionsCompatibles[0][1][4])
                elif actionsCompatibles[0][1][0] == "recruter":
                    erreur = self._infos.recrutement()
                elif actionsCompatibles[0][1][0] == "recruterCase":
                    if self._infos[self._infos.tour][('nombreTroupes', self._joueur)] + len(actionsCompatibles[0][1][1:]) > self._infos[0]["nombreDeTroupesMax"]:
                        erreur = "Trop de troupes à recruter"
                    else:
                        erreur = None
                        for case in actionsCompatibles[0][1][1:]:
                            if self._infos[self._infos.tour][case]["Proprietaire"] != self._joueur or self._infos[self._infos.tour][case]["Troupes"] == 7:
                                erreur = "Cases non-conformes"
                                break
                        if erreur == None:
                            self._infos[self._infos.tour]["action"] = ["recruterCase"]
                            for case in actionsCompatibles[0][1][1:]:
                                self._infos.recrutementALaCase(self._joueur, case)
                else:
                    erreur = self._infos.passerTour()
                if erreur == None:
                    self._infos.analyse.append((copy.deepcopy(self._infos[self._infos.tour]["action"]), "Recherche", str(actionsCompatibles[0][0]), actionsCompatibles[0][2], actionsCompatibles[0][3]))
                del actionsCompatibles[0]
        if erreur != None:
            self.actionAleatoire()
            self._infos.analyse.append((copy.deepcopy(self._infos[self._infos.tour]["action"]), "Aleatoire"))

class EntraineurIA:
    """
    Fonction destinée à l'entraînement et au test de l'IA. Pour cela, un
    nombre prédéterminé de parties où les deux joueurs sont remplacés par une
    IA sont lancées et sauvegardées. En plus du fichier de sauvegarde classique
    récapitulant l'état du plateau et l'action jouée à chaque tour, un autre
    fichier retraçant la provenance de chaque action jouée est créée afin de
    pouvoir évaluer l'évolution de l'IA.
    """
    def __init__(self, nombreParties:int=1, nombreDeTroupesMax:int=49, casesNeutresNonAdjacentes:bool=True, casesAdversesNonAdjacentes:bool=False, caseDepartJ1:tuple=(13, 1), caseDepartJ2:tuple=(1, 1)):
        """
        Constructeur lançant un nombre prédéterminé de parties avec les
        options prévues.

        Parameters
        ----------
        nombreParties : int, optional
            Nombre de parties à lancer à la suite. The default is 1.
        nombreDeTroupesMax : int, optional
            Nombre de troupes maximales par joueur hors influence.
            The default is 49.
        casesNeutresNonAdjacentes : bool, optional
            Permission pour les joueurs de déplacer leurs troupes sur une case
            neutre adjacente à l'une de leur case sans qu'elle ne doive être
            adjacente à la case de départ des troupes.
            The default is True.
        casesAdversesNonAdjacentes : bool, optional
            Permission pour les joueurs de déplacer leurs troupes sur une case
            adverse adjacente à l'une de leur case sans qu'elle ne doive être
            adjacente à la case de départ des troupes.
            The default is False.
        caseDepartJ1 : tuple, optional
            Case de départ du joueur 1. The default is (13, 1).
        caseDepartJ2 : tuple, optional
            Case de départ du joueur 2. The default is (1, 1).

        Returns
        -------
        None.

        """
        for i in range (0, nombreParties):
            self._joueur = "Joueur 1"
            self.infos = InfosDePartie(nombreDeTroupesMax=nombreDeTroupesMax, casesNeutresNonAdjacentes=casesNeutresNonAdjacentes, casesAdversesNonAdjacentes=casesAdversesNonAdjacentes, caseDepartJ1=caseDepartJ1, caseDepartJ2=caseDepartJ2)
            self.infos.analyse = [time.strftime("%d-%m-%Y_%H%M%S")]
            self._IAJoueur1 = IAAnalysee("Joueur 1", self.infos)
            self._IAJoueur2 = IAAnalysee("Joueur 2", self.infos)
            self._IAJoueur1.choixAction()
            try :
                self.finDuTour()
                print("Partie", i, "terminée")
            except RecursionError:
                print("Echec de la partie", i)

    def finDuTour(self):
        """
        Gère la mise à jour des infos de jeu à la fin d'un tour, ce qui
        comprend l'influence, le compte des troupes et évidemment le passage
        au tour suivant, met à jour les indications visuelles en fonction des
        infos de jeu, vérifie que les conditions de fin de partie ne sont pas
        remplies et gère le lancement du tour de l'IA.

        Returns
        -------
        None.

        """
        #Le tour est incrémenté de manière à faire les modifications de fin de tour sur le tour suivant et de pouvoir ainsi revenir en arrière jusqu'au tour 1. Sans cette mesure, le tour vierge du début de partie n'est pas enregistré.
        self.infos.tour += 1
        representantJ1 = False
        representantJ2 = False
        for case in self.infos[self.infos.tour].keys():
            if type(self.infos[self.infos.tour][case]) == dict and type(case) == tuple:
                #Vérification de la présence d'un Représentant pour chaque joueur
                if self.infos[self.infos.tour][case]["Proprietaire"] == "Joueur 1" and self.infos[self.infos.tour][case]["Representant"] == True:
                    representantJ1 = True
                elif self.infos[self.infos.tour][case]["Proprietaire"] == "Joueur 2" and self.infos[self.infos.tour][case]["Representant"] == True:
                    representantJ2 = True
                #Toutes les cases sans troupes ni Représentant deviennent neutres
                if self.infos[self.infos.tour][case]["Troupes"] == 0 and self.infos[self.infos.tour][case]["Representant"] == False:
                    self.infos[self.infos.tour][case]["Proprietaire"] = "Neutre"
        #Vérification de l'influence
        self.infos.influence()
        #Ajout aux infos de jeu du prochain tour, pour l'instant identique à l'actuel
        self.infos.ajoutTour()
        #Compte des troupes et des cases de chaque joueur
        self.infos[self.infos.tour]["nombreTroupes", "Joueur 1"] = 0
        self.infos[self.infos.tour]["nombreCases", "Joueur 1"] = 0
        self.infos[self.infos.tour]["nombreTroupes", "Joueur 2"] = 0
        self.infos[self.infos.tour]["nombreCases", "Joueur 2"] = 0
        for case in self.infos[self.infos.tour].keys():
            if type(self.infos[self.infos.tour][case]) == dict and type(case) == tuple:
                if self.infos[self.infos.tour][case]["Proprietaire"] == "Joueur 1":
                    self.infos[self.infos.tour]["nombreTroupes", "Joueur 1"] += self.infos[self.infos.tour][case]["Troupes"]
                    self.infos[self.infos.tour]["nombreCases", "Joueur 1"] += 1
                elif self.infos[self.infos.tour][case]["Proprietaire"] == "Joueur 2":
                    self.infos[self.infos.tour]["nombreTroupes", "Joueur 2"] += self.infos[self.infos.tour][case]["Troupes"]
                    self.infos[self.infos.tour]["nombreCases", "Joueur 2"] += 1
        #Vérification du joueur actif à partir du numéro du tour
        if self.infos.tour%2 == 0:
            self._joueur = "Joueur 2"
        else:
            self._joueur = "Joueur 1"
        #Vérification des conditions de fin de partie
        if representantJ1 == False and representantJ2 == False:
            self.infos[0]["indicationPartie"] = 3
            self.infos.sauvegarder(choixSauvegarde=os.path.dirname(__file__)+"/Sauvegardes"+"/Auto/"+time.strftime("%d-%m-%Y_%H%M%S")+".kan")
            self.sauvegarderAnalyse(choixSauvegarde=os.path.dirname(__file__)+"/AnalysesIA/"+time.strftime("%d-%m-%Y_%H%M%S")+".akan")
        elif representantJ1 == False:
            self.infos[0]["indicationPartie"] = 2
            self.infos.sauvegarder(choixSauvegarde=os.path.dirname(__file__)+"/Sauvegardes"+"/Auto/"+time.strftime("%d-%m-%Y_%H%M%S")+".kan")
            self.sauvegarderAnalyse(choixSauvegarde=os.path.dirname(__file__)+"/AnalysesIA/"+time.strftime("%d-%m-%Y_%H%M%S")+".akan")
        elif representantJ2 == False:
            self.infos[0]["indicationPartie"] = 1
            self.infos.sauvegarder(choixSauvegarde=os.path.dirname(__file__)+"/Sauvegardes"+"/Auto/"+time.strftime("%d-%m-%Y_%H%M%S")+".kan")
            self.sauvegarderAnalyse(choixSauvegarde=os.path.dirname(__file__)+"/AnalysesIA/"+time.strftime("%d-%m-%Y_%H%M%S")+".akan")
        #Si la partie n'est pas terminée et que c'est au tour d'une IA de jouer, celle-ci joue et une procédure de fin de tour est à nouveau appelée
        else:
            if self._joueur == "Joueur 1":
                self._IAJoueur1.choixAction()
                self.finDuTour()
            elif self._joueur == "Joueur 2":
                self._IAJoueur2.choixAction()
                self.finDuTour()

    def sauvegarderAnalyse(self, choixSauvegarde):
        #Conversion des données de jeu au format akan
        sauvegarde = "/".join([cle + ";" + str(self.infos[0][cle]) for cle in self.infos[0].keys()]) + "\n" + str(len(self.infos)-1)
        for i in range (1, len(self.infos.analyse)):
            sauvegarde = sauvegarde + "\n" + str(i)
            if self.infos.analyse[i][0] == None:
                sauvegarde = sauvegarde + "/" + "0"
            elif type(self.infos.analyse[i][0]) != list:
                sauvegarde = sauvegarde + "/" + self.infos.analyse[i][0]
            elif self.infos.analyse[i][0][0] == "recruterCase":
                sauvegarde = sauvegarde + "/" + self.infos.analyse[i][0][0]
                for caseRecrutement in self.infos.analyse[i][0][1:]:
                    sauvegarde = sauvegarde + ";" + str(list(caseRecrutement)[0]) + "," + str(list(caseRecrutement)[1])
            else:
                sauvegarde = sauvegarde + "/" + self.infos.analyse[i][0][0] + ";" + str(list(self.infos.analyse[i][0][1])[0]) + "," + str(list(self.infos.analyse[i][0][1])[1]) + ";" + str(list(self.infos.analyse[i][0][2])[0]) + "," + str(list(self.infos.analyse[i][0][2])[1]) + ";" + str(self.infos.analyse[i][0][3]) + ";" + str(self.infos.analyse[i][0][4])
            sauvegarde = sauvegarde + "/" + self.infos.analyse[i][1] + ("/" + self.infos.analyse[i][2] + "/" + self.infos.analyse[i][3] + "/" + self.infos.analyse[i][4] if len(self.infos.analyse[i]) >= 3 else "")
        #Ecriture des données converties dans le fichier choisi
        with open(choixSauvegarde, "w") as fichierSauvegarde:
            fichierSauvegarde.write(sauvegarde)




# ------------------------------Programme principal---------------------------
if __name__ == "__main__":
    FenetreGlobale()
    #EntraineurIA(3)
