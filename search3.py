#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PROJET SPOTIFY
    PARTIE 2 : RECHERCHE DE CONTENU
        QUESTION 3
        
L’utilisateur saisit une année et un genre : le programme doit retourner les chansons correspondant
ordonnées par popularité d’artiste décroissante.
S’il y a plusieurs chansons pour un même artiste, les ordonner par popularité décroissante.


N.B. : artists et tracks contiennent des noms identiques de variable (id, name, popularity..)
            et nous devons faire une jointure des deux tables par la suite
            nous avons donc modifié les noms en amont dans le module data_cleaning
"""


##### import des librairies
import pandas as pd
import ast

##### Chargement et nettoyage des donnees a partir du module
import data_loading
df_artists, df_tracks, df_top200 = data_loading.load()

import data_cleaning
df_artists, df_tracks, df_top200 = data_cleaning.clean(df_artists, df_tracks, df_top200)


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def load_unique_years() :
    """
    fonction qui génère une liste de toutes les années présentes dans la dataframe tracks

    Returns
    -------
    liste_annees_unique : list
        liste contenant toutes les annees uniques des chansons.

    """
    
    global liste_annees_unique # utilisable en dehors de la fonction
    
    # on recupere la colonne des annees existants et on la converti en set (éléments uniques)
    liste_annees_unique = set(df_tracks["release_year"])
    
load_unique_years()


def is_year_valid(annee_saisie) :
    """
    fonction qui verifie si l'annee saisie est presente dans la dataframe tracks

    Parameters
    ----------
    annee_saisie : str
        année saisie par l'utilisateur.

    Returns
    -------
    bool
        True : l'année est valide.
        False : l'année n'est pas valide.
    """
    
    # on verifie si l'annee saisie est valide
    if annee_saisie in liste_annees_unique :
        
        return True
    
    else :
        
        return False

# exemple d'utilisation
# is_year_valid("2020")
# is_year_valid("1850")



def load_unique_genres():
    """
    fonction qui génère une liste de toutes les genres existants dans la dataframe artists

    Returns
    -------
    list_genres_unique : list
        liste contenant tous les genres uniques des artistes.

    """
    
    # initialisation : on cree une liste vide de genres
    list_genres = []
    
    
    ## autre methode qu'utilisee dans search1
    # pour toutes les lignes de genres...
    for genres_str in df_artists["genres_lowercase"] :
        
        # ...on la convertit en liste
        genres = ast.literal_eval(genres_str)
        
        # pour chaque genre dans les listes de genres
        for genre in genres :
            
            # on ajoute le genre a la liste precedemment creee
            list_genres.append(genre)
    
    
    global list_genres_unique # utilisable en dehors de la fonction
    
    # on ne garde que les valeurs uniques de genres
    list_genres_unique = set(list_genres)

load_unique_genres()


def is_genre_valid(genre_saisi) :
    """
    fonction qui vérifie si le genre saisi est bien présent dans nos donnees

    Parameters
    ----------
    genre_saisi : str
        genre saisi par l'utilisateur.

    Returns
    -------
    bool
        True : le genre est valide.
        False : le genre n'est pas valide.

    """
    
    # on met le genre saisi en minuscule pour pouvoir comparer
    genre_saisi = genre_saisi.lower()
    
    # verifier si le genre saisi est valide    
    if genre_saisi  in list_genres_unique :
        
        return True
    
    else:
        
        return False

# exemple d'utlisation
# is_genre_valid("classic")
# is_genre_valid("rap")



##### jointure de artists et tracks

# transformer dans la table tracks, id_artists en liste
df_tracks['id_artists'] = df_tracks['id_artists'].apply(lambda x: ast.literal_eval(x))



# transformer dans la table artists, genres_lowercase en liste
df_artists['genres_lowercase'] = df_artists['genres_lowercase'].apply(lambda x: ast.literal_eval(x))



## pb : il y a plusieurs id d'artistes dans id_artists
# fonction qui "deplie" artists : 1 id d'artiste par ligne ## attention il y a des NaN
df_tracks_exploded = df_tracks.explode('id_artists')


# jointure de artists et tracks avec comme cle l'id de l'artiste
merged = pd.merge(df_artists, df_tracks_exploded, left_on = 'artist_id', right_on = 'id_artists', how = 'outer')



## pb : genres_lowercase contient des NaN -> on remplace par une liste vide
# fonction anonyme : pour chaque ligne, si la ligne est deja une liste, on ne change rien
# si elle ne l'est pas, on remplace par une liste vide []
merged['genres_lowercase'] = merged['genres_lowercase'].apply(lambda x: x if isinstance(x, list) else [])


# trier par popularite d'artiste decroissante et par popularite de chanson decroissante
merged = merged.sort_values(by=['artist_popularity', 'song_popularity'], ascending=[False, False])



def get_titles_year_genre(annee_saisie, genre_saisi):
    """ fonction qui retourne une liste de chansons filtrées par l'année et le genre,
        triée par popularité d'artistes décroissante puis par popularité de chansons décroissante.

    Parameters
    ----------
    annee_saisie : str
        année saisie par l'utilisateur.
    genre_saisi : str
        genre saisi par l'utilisateur.

    Returns
    -------
    filtered_songs : dataframe
        liste de titres de chansons filtrées par année et genre, et triées par popularité decroissante.

    """
    
    # on met le genre saisi en minuscule pour pouvoir comparer
    genre_saisi = genre_saisi.lower()
    
    # verifier si l'annee saisie et le genre saisi sont valides
    if is_genre_valid(genre_saisi) == True and is_year_valid(annee_saisie) == True :
        
        # on applique les deux filtres
        # 1e filtre : on selectionne les chansons correspondantes a l'annee saisie
        # 2e filtre : on selectionne les chansons correspondantes au genre saisi
        filter_year_genre = merged[
                            (merged["release_year"] == annee_saisie) &
                            (merged["genres_lowercase"].apply(lambda liste_genres: genre_saisi in liste_genres))
                            ]
        
        # on selectionne uniquement les colonnes qu'on veut afficher et on met une mise en forme
        filter_year_genre['song_artist'] = filter_year_genre['song_name'] + "  -  " + filter_year_genre['artists_name'] + "\n"
        
        # Retourner une liste des titres correspondants à l'année et au genre saisis
        return filter_year_genre['song_artist'].tolist() # on convertit en liste
        
    
    else:
        
        return "Aucune chanson correspond à votre recherche."

# exemple d'utilisation
# get_titles_year_genre("2020", "classic")
# get_titles_year_genre("2015", "pop")
