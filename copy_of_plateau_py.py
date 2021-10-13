# -*- coding: utf-8 -*-
"""Copy of plateau.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16_D_ctIeFYjRHZ6JPf1oMGJzddrvdqwx
"""

import numpy as np
import pandas as pd
from random import *
import matplotlib.pyplot as plt 
from collections import defaultdict


def liste_quad(l, c):
  liste=[]
  #horisontale
  for lcpt in range(0 , l):
    for ccpt in range(0, c-3):
      liste.append([(lcpt,ccpt),(lcpt,ccpt+1),(lcpt,ccpt+2),(lcpt,ccpt+3)])

      #ajout des tuples de victoires sur les colonnes
  for ccpt in range(0 , c):
      for lcpt in range(0, l-3):
        liste.append([(lcpt,ccpt),(lcpt+1,ccpt),(lcpt+2,ccpt),(lcpt+3,ccpt)])

        #ajout des tuples de victoires sur les diagonales vers le bas
  for lcpt in range(0 , l-3):
    for ccpt in range(0, c-3):
      liste.append([(lcpt,ccpt),(lcpt+1,ccpt+1),(lcpt+2,ccpt+2),(lcpt+3,ccpt+3)])

        #ajout des tuples de victoires sur les diagonales vers le haut
  for lcpt in range(0, l-3):
    for ccpt in range(3, c):
      liste.append([(lcpt,ccpt),(lcpt+1,ccpt-1),(lcpt+2,ccpt-2),(lcpt+3,ccpt-3)])
  return liste



# lil= liste_quad(6,7)
# print( lil)
# plateau = np.zeros((6, 7), dtype=int)
# quadruplet = liste_quad(l=6,c=7)

# for a,b,c,d in quadruplet:
#   print(plateau[a])
#   print(plateau[b])
#   print(plateau[c])
#   print(plateau[d])

class Joueur():
	

	def __init__(self,couleur_j):
		if couleur_j == "bleu":
			self.valeur = 1
		else:
			self.valeur=-1	
 
  
	
	def play(self,pl, grille):
		# print("play1")
		liste=[] #Tous les coups (colonnes) possibles 
    #Parcourir toutes les colonnes : Pourquoi Tjs la colonne 0
		for i in range(grille.shape[1]):
				if 0 in grille.transpose()[i]: #Verifier si la colonne est valable 
					liste.append(i)
		return int(randint(0,len(liste)-1))

class Plateau():
	

	def __init__(self, l, c):
		self.l=l
		self.c=c
		self.quad= liste_quad(l, c)
		# self.reset(l, c)
		self.grille=np.zeros((l, c), dtype=int)

	def reset(self, l, c):
		self.grille=np.zeros((l, c), dtype=int)

	def has_won(self, jVal, grille): 
		# print("has won")
		#J represente le joueur 1 ou -1 
		#Parourir la liste des coordonees dans la liste quad
		for i,j,k,z in self.quad:
			a,b,e,d =  grille[i],  grille[j],  grille[k], grille[z]
			if a==b==e==d==jVal:
				return True
		return False


	def play(self, x, jVal, grille): # j'ai remplcé  joueur  par jVal
		# print("play 2")
		for i in range(self.l - 1, -1, -1):
			if grille[i][int(x)]==0:
				grille[i][int(x)]= jVal 
				break

	def is_finished(self, jVal, grille):
		# print("is_finished")
		if self.has_won(jVal, grille) or self.has_won(-jVal, grille):
			return True 
		elif np.prod(np.array(grille))==0:  
			# le Produit de tous les éléments de la grille à la recherche d'a Zéro
			return False
		return True #personne n'a gagne et on ne peut pas continuer a jouer

	def run(self, jVal):

		fini= self.is_finished(1, self.grille) 
		# print(fini)
		j1= Joueur("bleu")
		j2= Joueur("rouge")
		nb_coups_j1=nb_coups_j2=0 #Le nombre de coups avant de gagner pour j1/j2
		cpt=0 # alterner les Joueurs
		while(not fini):
			if cpt%2==0:
				#J1 joue
				col= j1.play(self) #Determiner la colonne choisie par le joueur 1 
				self.play(col, 1) #Le joueur j1 joue 
				nb_coups_j1+=1 #Nombre déssayes augmente
			else: 
				#J2 joue 
				col= j2.play(self) #Determiner la colonne choisie par le joueur 1 
				self.play(col, -1) #Le joueur j1 joue 
				nb_coups_j2+=1 #Nombre déssayes augmente		
			cpt+=1 	
			fini= self.is_finished(1, self.grille) #Verifier si le jeu est fini 
				
		#Fin du while 

		#Verifier lequel des joeueur a gagné 
		if self.has_won(1, self.grille):
			return (1,nb_coups_j1) 
		elif self.has_won(-1, self.grille): 
			return (-1,nb_coups_j2)
		else: 
			return (0,0)

# plateau= Plateau(3, 3)
# print(plateau)

def modeliser():
  L1=[]
  L2=[]
  L=[]
  for i in range(20):
    plateau= Plateau(6, 7)
    r= plateau.run(1)

    if r[0]==1:
      L1.append(r[1])
    elif r[0]==-1:
      L2.append(r[1])
  plt.hist(L1, label="j1" )
  plt.hist(L2, label="j2")
  plt.legend()
  plt.show 

# modeliser()

#classe joueur Monte-Carlo 
class Monte_Carlo():

  def __init__(self, joueur): #Joueur est un objet de la classe Joueur 
    self.joueur=joueur
				

  def Monte_Carlo_Moteur(self, etat, col, adv, grid):
    #monte - carlo joue la colonne col 
    
    etat.play(col, self.joueur.valeur, grid)
    cpt=1
    while(not etat.is_finished(self.joueur.valeur, grid)):#Verifier si le jeu est terminé 
      # if cpt==0: #La colonnes passée en argument est utilisée 
      #   if cpt%2 == 0: #Le premier joueur joue 
      #     etat.play(col, joueur)
      #   else: 
      #     etat.play(col, adversaire)
      # else:
      if cpt%2 == 0: #Le premier joueur joue 
        # etat.play(col1, joueur.valeur)
        # col1=joueur.play(etat)
        col= self.joueur.play(etat, grid) #Determiner la colonne choisie par le joueur 1
        etat.play(col, self.joueur.valeur, grid) #Le joueur j1 joue 
      else:
        # etat.play(col2, adv.valeur)
        # col2=adv.play(etat)
        col= adv.play(etat, grid) #Determiner la colonne choisie par le joueur 1
        etat.play(col, adv.valeur, grid) #Le joueur j1 joue
      cpt+=1 
    if etat.has_won(self.joueur.valeur, grid) or etat.has_won(adv.valeur, grid):#Si au moins un des deux a gagné, on ajoute le nombre de coups pour cette colonne
      return cpt 
    return 0

  def Monte_Carlo_Play(self, pl, N):
    """ trouver la meilleure colonne a jouer """
    adv= Joueur("rouge") #Instanciation du joueur adversaire pour faire la simulation du jeu 
    #Recompense de l'action choisie
    lst=[]
    # for col in (0, etat.c):
      # lst.append((col, 0,0)) #Stocker dans un tuple: la colonne, le nombre de coups et le nombre de fois que la colonne a été choisi 
    
    for i in range(N):
      grid=pl.grille.copy()
      #cpt=0 #le nombre de coups avant que l'un des deux joueurs gagne pour une colonne choisi
      col= randint(0, pl.c - 1) #Choisir une colonne aleatoire
      # while(not etat.is_finished(joueur, adversaire)):#Verifier si le jeu est terminé 
      #   if cpt%2 == 0: #Le premier joueur joue 
      #     etat.play(colonne, joueur)
      #   else: 
      #     etat.play(colonne, adversaire)
      #   cpt+=1

      cpt= self.Monte_Carlo_Moteur(pl, col, adv, grid)
      # Nbre de coup qui a abouti à un Gain ou Pas
      #A la sortie du while, le jeux est terminé 
      if cpt>0: #Si au moins des deux a gagné, on ajoute le nombre de coups pour cette colonne 
        #Chercher la colonne dans la liste des triplets 
        lst.append((col, cpt))
      
    lst=pd.DataFrame(
        lst,columns=["ind", "occ"]).groupby("ind").agg("mean").reset_index().to_numpy()
    lst
    # sums = defaultdict(int)
    # for i, k in lst:
    #     sums[i] += k
    # lst=list(sums.items())

    #Trouver les moyennes des victoires
    # ll=[] #Liste contenant les colonnes et les moyennes en forme de couples 
    # # for j in lst: 
    # #   ll.append( ( j[0], j[1]/j[2] ) )

    # ll=np.array(
    #     pd.DataFrame(lst, colnames=["ind", "occ"]).groupby("ind").agg("mean"))

    #Trouver a meilleure   Min Or Max?
    Best_col= max(lst, key=lambda x:x[1])
    return Best_col[0]



  def run_Monte_carlo(self, Joueur_Ad, pl, nb, is_alea):
    """ Fonction d'un jeu entre un joueur monte_carlo et un autre joueur (monte_caro ou aleatoire) qui renvoie le 
        joueur gagna avec le nombre de coups """
    finish= pl.is_finished(self.joueur.valeur, pl.grille)
    cp=0 #Compteur pour alterner entre joueur 1 et 2 
    nb_coupsj1=0 
    nb_coupsj2=0

    while(not finish):
      #Tant que le jeu n'est pas terminé les joeuurs jouent

      if cp%2==0: #Le joueur monte carlo joue 
        col= self.Monte_Carlo_Play(pl, nb) #La meilleure colonne est choisie 
        pl.play(col, self.joueur.valeur, pl.grille) #Le joueur joue 
        nb_coupsj1+=1
      elif is_alea: #Si le joueur adversaire est un joueur aleatoire 
        #Determiner dans quelle colonnes le joueur aleatoire va jouer en utilisant la fonction play dans la classe Joueur  
        col= Joueur_Ad.play(pl, pl.grille) 
        pl.play(col, Joueur_Ad.valeur, pl.grille) 
        nb_coupsj2+=1
      else: #Jouer contre un joueur monte carlo 
        col= Joueur_Ad.Monte_Carlo_Play(pl, nb)
        pl.play(col, Joueur_Ad.valeur, pl.grille)
        nb_coupsj2+=1
      cp+=1
      finish= pl.is_finished(self.joueur.valeur, pl.grille)

		#Verifeir lequel des joeueur a gagné 
    if pl.has_won(self.joueur.valeur, pl.grille): 
      return (self.joueur.valeur,nb_coupsj1) 
    elif pl.has_won(Joueur_Ad.valeur, pl.grille): 
      return (Joueur_Ad.valeur,nb_coupsj2)
    return (0,0)

# Test pour un joeur Monte_Carlo contre lui meme

# Instanciation du joueur Monte_carlo 

j1= Joueur("bleu") #Le joueur Monte_carlo blue
#Instatiation monte_carlo 
mc= Monte_Carlo(j1)

p= Plateau(6,7) #Initialisation du plateau vide au debut 
for k in range(30):
  mc.run_Monte_carlo(j1, p, 20, False)

# quadruplet = liste_quad(l=6,c=7)
# for i,j,k,l in quadruplet:
#   a,b,c,d = plateau.grille[i], plateau.grille[j], plateau.grille[k], plateau.grille[l]
#   if a==b==c==d:
#     print(a)
#     break


"""-   Joueur A   appel MonteCarlo   à la recherche de la meilleurs colonne à y placer son Jeton
    + Montecarlo(Grille, N ) [  créer un  Joueur Dummy ]==>  colonne
    + 

"""