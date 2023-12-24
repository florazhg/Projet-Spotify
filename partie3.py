#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROJET SPOTIFY
    PARTIE 3 : CREATION D'INTERFACE GRAPHIQUE
"""

##### import des modules
import tkinter as tk
import webbrowser


##### Chargement et nettoyage des donnees a partir des module
import data_loading
df_artists, df_tracks, df_top200 = data_loading.load()

import data_cleaning
df_artists, df_tracks, df_top200 = data_cleaning.clean(df_artists, df_tracks, df_top200)


##### import des modules de recherche
#import recherche1 salma
import search1
import search2
import search3






##### interface principale

# creation de la fenetre
fenetre = tk.Tk()
fenetre.title("Spotify")
fenetre.geometry("980x780+215+0")
fenetre.resizable(False, False) #la fenetre peut pas se réduire 
fenetre.config(background='#E6E0F8')



# Ajout de label/text
label_title = tk.Label(fenetre,text="Bienvenue sur Spotify",background="#E6E0F8",foreground="black",font="arial, 45")
label_title.pack(pady=10)



# insertion de l'image
photo = tk.PhotoImage(file="page.png").zoom(10).subsample(25)
canvas = tk.Canvas(fenetre, background='#E6E0F8',bd =0, highlightthickness=0)
canvas.create_image(15, 15, anchor="nw", image=photo)
canvas.pack(pady=10)


# zone d'entree
entree = tk.Entry(fenetre,font="arial, 20", bg='#E6E0F8',fg='black',width=20)
entree.pack(pady=10)





### fonction de barre de recherche

def barre_de_recherche():
    global resultat_recherche
    global recherche
    global boutton_wiki
    recherche = entree.get().strip() #enlever les espaces avant et apres
    
    # recherche nom d'artiste
    if search1.is_artist_valid(recherche):
        
        infos = f""""Le nombre d'abonnés de {recherche} : {search1.nb_followers(recherche)}
        
        Le top 3 des chansons de {recherche} :
        {search1.get_artist_top3_popular_songs(recherche)}
        
        Le top 3 des chansons de {recherche} :
        search1.get_artist_top3_recent_songs{recherche}
         
         
        
        """
        
        result_followers = tk.Label(fenetre,text = f"Le nombre d'abonnés de {recherche} : " + str(search1.nb_followers(recherche)),background='#F2E0F7',foreground="black",font="arial, 14")
        result_top3_songs = tk.Label(fenetre,text = f"Le top 3 des chansons de {recherche} : \n" + str(search1.get_artist_top3_popular_songs(recherche)),background='#F2E0F7',foreground="black",font="arial, 14")
        result_recent3_songs = tk.Label(fenetre,text = f"Le top 3 des chansons de {recherche} : \n" + str(search1.get_artist_recent3_songs(recherche)),background='#F2E0F7',foreground="black",font="arial, 14")
        
        boutton_wiki = tk.Button(fenetre,text="ouvrir la page wikipédia",background="#F2E0F7",foreground="black",font="arial, 9", command=lien_site)
        
        
        boutton_wiki.pack()
        result_followers.pack()
        result_top3_songs.pack()
        result_recent3_songs.pack()


    # recherche tracks
    if search2.is_title_valid(recherche):
        
        result_songs = tk.Label(fenetre,text = str(search2.get_titles(recherche)),background='#F2E0F7',foreground="black",font="arial, 14")
        result_songs.pack()    
    
    
    # recherche par annee et par genre
    else : # si la recherche par nom d'artiste et tracks
        couple_ga = recherche.split(',') # on separe année et genre
        
        if len(couple_ga) == 2 :
            annee_saisie, genre_saisi = couple_ga # on sépare la variable en 2 variables
            annee_saisie = annee_saisie.strip() # enlever les espaces avant et apres
            genre_saisi = genre_saisi.strip()
            
            if search3.is_year_valid(annee_saisie) == True and search3.is_genre_valid(genre_saisi) == True:
                result_genre_year = tk.Label(fenetre, text= str(search3.recherche_ga(annee_saisie, genre_saisi)),background='#F2E0F7',foreground="black",font="arial, 12")
                result_genre_year.pack()
                
            else : # si la recherche par nom d'artiste, tracks et (année, genre) n'aboutit a rien
                result_recherche = tk.Label(fenetre, text = "Saisie invalide. Veuillez vérifier vos entrées.",background='#F2E0F7',foreground="black",font="arial, 12")
                result_recherche.pack()

    

## fonction de recommencer
def recommencer():
    entree.delete(0,"end")
    resultat_recherche.config(text = "")
    boutton_wiki.destroy()



# lien des sites

def lien_site():
    site = {"justin" : "https://fr.wikipedia.org/wiki/Justin_Bieber",
         "taylor swift" : "https://fr.wikipedia.org/wiki/Taylor_Swift",
         "drake" : "https://fr.wikipedia.org/wiki/Drake_(rappeur)",
         "bad bunny" : "https://fr.wikipedia.org/wiki/Bad_Bunny",
         "bts" : "https://fr.wikipedia.org/wiki/BTS_(groupe)",
         "the weeknd" : "https://fr.wikipedia.org/wiki/The_Weeknd",
         "juice wrld" : "https://fr.wikipedia.org/wiki/Juice_Wrld",
         "myke towers" : "https://fr.wikipedia.org/wiki/Myke_Towers",
         "dua lipa" : "https://fr.wikipedia.org/wiki/Dua_Lipa",
         "j balvin" : "ttps://fr.wikipedia.org/wiki/J_Balvin",}
 
    site_recherche = site.get(recherche.lower())
    if recherche == "justin":
        webbrowser.open_new(site_recherche)
    else:
        tk.messagebox.showinfo("resultat", f"pas de lien pour : {recherche}")
              

            
    

##bouton d'éxecution de la barre de recherche 

boutton_entree = tk.Button(fenetre,text="recherche",background="#E6E0F8",foreground="black",font="arial, 20", command=barre_de_recherche) 
boutton_entree.pack(pady=10)

## bouton recommencer

boutton_restart = tk.Button(fenetre,text="restart",background="#E6E0F8",foreground="black",font="arial, 20", command=recommencer) 
boutton_restart.pack(pady=10)




#afficher
fenetre.mainloop()


            
    

 
