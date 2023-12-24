#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROJET SPOTIFY
    MODULE NETTOYAGE DES DONNEES
a rajouter au fur et a mesure encore si vous remarquez des trucs
"""

import pandas as pd
import ast

##### import de modules
import data_loading
df_artists, df_tracks, df_top200 = data_loading.load()


##### nettoyage de donnees
def clean(df_artists, df_tracks, df_top200):
    
    ##### dataframe artists
    
        # remplacer les valeurs manquantes par missing
        # verification avec .isna().sum()
    df_artists['name'] = df_artists['name'].fillna('missing')
    df_artists['followers'] = df_artists['followers'].fillna('missing')
    
    
        # renommer les colonnes car ils coincident avec df_tracks
    df_artists = df_artists.rename(columns={'id':'artist_id',
                                             'popularity': 'artist_popularity',
                                             'name': 'artist_name'})
        
        # creer une colonne avec le nom des artistes en minuscule (utile dans la partie 2, q1)
    df_artists["name_lowercase"] = df_artists["artist_name"].str.lower()
    
        
        # Formater les valeurs de la colonne genres en minuscule
    df_artists["genres_lowercase"] = df_artists["genres"].str.lower()
    
    
    
    ##### dataframe tracks
    
        # simplifier les colonnes
    df_tracks = df_tracks.drop(['duration_ms','explicit','danceability','energy',
                                'key','loudness','mode','speechiness','instrumentalness',
                                'liveness','valence','tempo','time_signature','acousticness'],axis=1, errors='ignore')
    
    
        # remplacer les valeurs manquantes par missing
    df_tracks['name'] = df_tracks['name'].fillna('missing')
    
    
        # transformer le type de popularity en float
    df_tracks['popularity'] = df_tracks['popularity'].astype("float")
    
    
        # transformer la variable release_date en DateTime mixed
        # attribue 01/01 par defaut pour les dates contenant que l'annee
    df_tracks["release_date"] = pd.to_datetime(df_tracks["release_date"], format="mixed")
    
    
        # ajouter une colonne de l'annee de sortie (utile dans la partie 1 et 2)
    df_tracks["release_year"] = df_tracks["release_date"].dt.strftime("%Y")
    
    
        # renommer les colonnes car ils coincident avec df_artists
    df_tracks = df_tracks.rename(columns={'id':'song_id',
                                          'name': 'song_name',
                                          'popularity': 'song_popularity',
                                          'artists': 'artists_name'})
        
    
        # on cree une colonne avec le nom des artistes en minuscule (utile dans la partie 2, q1)
    df_tracks["artists_name_lowercase"] = df_tracks["artists_name"].str.lower()

    
        # on convertit la colonne artists_name en liste (utile dans la partie 2, q1)
        # exemple: la string "['BTS', 'Doja Cat']" est convertie en une liste de string ['BTS', 'Doja Cat']
    df_tracks['artists_name_lowercase'] = df_tracks['artists_name_lowercase'].apply(lambda x: ast.literal_eval(x))


        # on creer une colonne avec les titres de chansons en minusculte (utile dans la partie 2, q2)
    df_tracks["song_name_lowercase"] = df_tracks["song_name"].str.lower()
    
    
    
    ##### top_200
        
        # simplifier les colonnes : on l'enleve car il s'agit de "global" partout ici 
    df_top200 = df_top200.drop(['Country'],axis=1)
    
    
        # transformer le type de streams en nombre entier
    df_top200['Streams'] = df_top200['Streams'].astype("int")
    
    
        # transformer le type en datetime
    df_top200["Date"] = pd.to_datetime(df_top200["Date"], format="%Y-%m-%d")
    
    
        # on creer une colonne avec le nom des artistes en minulscule (utile dans la partie 2,q1)
    df_top200["artist_lowercase"] = df_top200["Artist"].str.lower()
    
    
        # on prend en compte le fait qu'il peut y avoir plusieurs artistes pour une chanson
        # les artistes etant separes par une ,
    df_top200["artist_lowercase"] = df_top200["artist_lowercase"].apply(lambda x: x.split(", "))

    
    
    
    return df_artists, df_tracks, df_top200






