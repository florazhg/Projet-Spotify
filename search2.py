#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PROJET SPOTIFY
    PARTIE 2 : RECHERCHE DE CONTENU
        QUESTION 2
        
L’utilisateur saisit un titre de chanson : le programme doit retourner les résultats qui correspondent.
Les ordonner par popularité décroissante. S’il y a beaucoup de résultats, n’afficher que les 20 premiers.

"""

import pandas as pd

##### Chargement et nettoyage des donnees a partir des modules
import data_loading
df_artists, df_tracks, df_top200 = data_loading.load()

import data_cleaning
df_artists, df_tracks, df_top200 = data_cleaning.clean(df_artists, df_tracks, df_top200)

# afficher le maximum de colonnes
pd.set_option('display.max_columns', None)


def is_title_valid(song_title):
    """ fonction qui verifie si un titre de chanson existe
    
    Parameters
    ----------
    song_title : str
        titre de chanson saisi par l'utilisateur.
    
    Returns
    -------
    bool
        True : le titre de chanson saisi est valide.
        False : le titre de chanson saisi n'est pas valide.
    
    
    """
    
    # on met la chanson saisie en minuscule pour pouvoir comparer
    song_title_lower = song_title.lower()
    
    # verifier si au moins un des chansons de la colonne est egale a la chabnson saisie
    if any(df_tracks["song_name_lowercase"] == song_title_lower) == True :
        
        return True
    
    else:
        
        return False

# exemple d'utilisation
# is_title_valid("Stay")
# is_title_valid("abcde")

def get_titles(song_title):
    """ fonction qui affiche les résultats de recherche d'une chanson
    

    Parameters
    ----------
    song_title : str
        titre de chanson saisi par l'utilisateur.

    Returns
    -------
    first_20_songs : dataframe
        les 20 premières chansons correspondantes à la recherche.

    """
        
    # on met la chanson saisie en minuscule pour pouvoir comparer
    song_title_lower = song_title.lower()

    # on stocke dans songs les lignes de chansons qui correspondent a notre recherche
    songs = df_tracks.loc[df_tracks["song_name_lowercase"] == song_title_lower]
    
    # on trie les chansons par popularite decroissante et on ne garde que les 20 premieres
    songs_sorted = songs.sort_values(by="song_popularity", ascending = False).head(20)
    
    # on selectionne les colonnes a afficher
    first_20_songs = songs_sorted[["song_name", "artists_name", "release_year"]]
    
    # on verifie si le titre est valide
    if is_title_valid(song_title) :
                
        return first_20_songs.to_string(index = False)
    
    else:
        
        return f"Aucun résultat pour {song_title}."


# exemple d'utilisation
# get_titles("Stay")
# get_titles("abcde")
