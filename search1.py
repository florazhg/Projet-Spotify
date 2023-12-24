#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PROJET SPOTIFY
    PARTIE 2 : RECHERCHE DE CONTENU
        QUESTION 1
        
L’utilisateur saisit un nom d’artiste : le programme doit retourner son nombre d’abonnés, les 3 chansons les
plus populaires, les 3 chansons les plus récentes ainsi que le nombre de chansons qu’il a dans le top 200
global de 2020 (s’il y en a)


"""

##### Chargement et nettoyage des donnees a partir des modules
import data_loading
df_artists, df_tracks, df_top200 = data_loading.load()

import data_cleaning
df_artists, df_tracks, df_top200 = data_cleaning.clean(df_artists, df_tracks, df_top200)

import pandas as pd
pd.set_option('display.max_columns', 2)


def is_artist_valid(artist_name) :
    """ fonction qui verifie si le nom de l'artiste saisi existe bien
    
    Parameters
    ----------
    artist_name : str
        nom de l'artiste saisi par l'utilisateur.
    
    Returns
    -------
    bool
        True : le nom de l'artiste est valide.
        False : le nom de l'artiste n'est pas valide.
    
    
    """
    
    # on met le nom d'artiste saisi en minuscule pour pouvoir comparer
    artist_name_lower = artist_name.lower()
    
    # verifier si au moins un des artistes de la colonne est egale a l'artiste saisi
    if any(df_artists["name_lowercase"] == artist_name_lower) :
        
        # on cree une variable qui nous sera utile dans l'interface graphique
        global id_spotify
        # elle stocke l'id de l'artiste
        id_spotify = df_artists[df_artists["name_lowercase"] == artist_name_lower].iloc[0]["artist_id"]
    
        return True
    
    else:
    
        return False

# exemple d'utilisation
# is_artist_valid("JUSTIN bib")
# is_artist_valid("JUSTIN bieber")


def nb_followers(artist_name):
    """ fonction qui recupere le nombre d'abonnees d'un artiste
    

    Parameters
    ----------
    artist_name : str
        nom de l'artiste saisi par l'utilisateur.

    Returns
    -------
    int
        le nombre d'abonnees de l'artiste saisi.

    """
    
    artist_name_lower = artist_name.lower()
    
    if is_artist_valid(artist_name) == True :
        
        # selectionner la ligne de l'artiste qui correspond au nom de l'artiste saisi
        followers_count = df_artists.loc[ df_artists["name_lowercase"] == artist_name_lower,["followers"]]
        
        # recuperer la valeur et la transformer en int
        followers_count = int(followers_count.values[0])
        
        # separateur de milliers
        return '{:,}'.format(followers_count)
    
    else:
        
        return None
    
# exemple d'utilisation
# nb_followers("BTTS")
# nb_followers("BTs")


def get_artist_songs(artist_name):
    """ fonction renvoie chansons de l'artiste saisi
    

    Parameters
    ----------
    artist_name : str
        nom de l'artiste saisi par l'utilisateur.

    Returns
    -------
    artist_songs : TYPE
        DESCRIPTION.

    """
    
    # on met le nom d'artiste saisi en minuscule pour pouvoir comparer
    artist_name_lower = artist_name.lower()
        
    # on regarde pour chaques artistes de la colonne, si l'artiste saisi correspond
    # on peut avoir plusieurs artistes par colonne car ils chantent en feat
    # donc on utilise la fonction anonyme qui va chercher a l'interieur des listes d'artistes
    # puis on stocke les lignes correspondantes dans artist_songs
    artist_songs = df_tracks[df_tracks["artists_name_lowercase"].apply(lambda artists: artist_name_lower in artists)]
        
    return artist_songs



def get_artist_top3_popular_songs(artist_name):
    """ fonction qui renvoie les trois chansons les plus populaires d'un artiste
    

    Parameters
    ----------
    artist_name : str
        nom de l'artiste saisi par l'utilisateur.

    Returns
    -------
    top3_popular_songs : dafatrame
        les 3 chansons les plus populaires de l'artiste.

    """
    
    # on selectionne les chansons de l'artiste
    artist_songs = get_artist_songs(artist_name)
    
    # on trie les chansons par popularite decroissante et on ne garde que les 3 premieres
    top3_popular_songs = artist_songs.sort_values(by="song_popularity", ascending=False).head(3)
    
    # on verifie si top3_popular_songs contient bien des chansons
    if len(top3_popular_songs) != 0 :
        
        # on convertit en chaine de caractere et on supprime la colonne de string, utile pour l'interface graphique
        return top3_popular_songs[["song_name", "artists_name", "song_popularity"]].to_string(index = False)
    
    else:
        
        return f"{artist_name} n'a aucune chanson populaire." 

# exemple d'utilisation
# get_artist_top3_popular_songs("BTS")
# get_artist_top3_popular_songs("Wang yibo")

def get_artist_recent3_songs(artist_name):
    """ fonction qui renvoie les trois chansons les plus récentes d'un artiste
    

    Parameters
    ----------
    artist_name : str
        nom de l'artiste saisi par l'utilisateur.

    Returns
    -------
    recent3_songs : dafatrame
        les 3 chansons les plus récentes de l'artiste.

    """
    
    # on selectionne les chansons de l'artiste
    artist_songs = get_artist_songs(artist_name)
    
    # on trie les chansons du plus recent au plus ancien et on ne garde que les 3 premieres
    recent3_songs = artist_songs.sort_values(by="release_date", ascending=False).head(3)
    
    # on verifie si recents3_songs contient bien des chansons
    if len(recent3_songs) != 0 :
        
        return recent3_songs[["song_name", "artists_name", "release_date"]].to_string(index = False)
    
    else:
        
        return f"{artist_name} n'a aucune chanson récente."

# exemple d'utilisation
# get_artist_recent3_songs("Olivia rodrigo")
# get_artist_recent3_songs("the beatles")


def get_artist_top200_songs(artist_name):
    """ fonction qui retourne le nombre de chansons present dans le top200 global d'un artiste
    

    Parameters
    ----------
    artist_name : str
        nom de l'artiste saisi par l'utilisateur.

    Returns
    -------
    count_top200 : int
        nombre de chansons present dans le top200 global d'un artiste.

    """
    
    # on met le nom d'artiste saisi en minuscule pour pouvoir comparer
    artist_name_lower = artist_name.lower()
    
    # on a plusieurs artistes par colonne
    # on parcourt donc chaque artiste pour trouver les chansons dans lesquelles notre artiste chante
    # on stocke les lignes correspondantes dans top200_artist
    top200_artist = df_top200[df_top200["artist_lowercase"].apply(lambda list_artists: artist_name_lower in list_artists)]
    
    # la dataframe top200 contient les top200 pour chaque jour de 2020
    # on ne garde donc que la premiere occurence de la chanson, car elle peut etre dans le top200 pour plusieurs jours
    unique_top_200_artist = top200_artist.drop_duplicates(subset=["Artist", "Title"], keep="first")
    
    
    if len(unique_top_200_artist) != 0 :
        
        # on recupere le nombre de chanson dans le top200
        count_top200 = unique_top_200_artist.shape[0]
        return count_top200
    
    else:
        
        return f"{artist_name} n'a aucune chanson le top 200 global de 2020."


# exemple d'utilisation
# get_artist_top200_songs("Selena gomez")
# get_artist_top200_songs("the beatles")

