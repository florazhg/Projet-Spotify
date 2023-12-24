#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROJET SPOTIFY
    MODULE CHARGEMENT DES DONNEES
"""

##### import de librairies
import pandas as pd


##### chargement des donnees
def load():
    """
    fonction qui charge les 3 dataframes à utiliser

    Returns
    -------
    df_artists : Dataframe
        Depuis les données artists.csv
    df_tracks : Dataframe
        Depuis les données tracks.csv
    df_top200 : Dataframe
        Depuis les données spotify_top200_global.csv

    """
    
    df1 = pd.read_csv("./data/artists.csv")
    df2 = pd.read_csv("./data/tracks.csv")
    df3 = pd.read_csv("./data/spotify_top200_global.csv")
    
    # deep copy des dataframes
    df_artists = df1.copy(deep=True)
    df_tracks = df2.copy(deep=True)
    df_top200 = df3.copy(deep=True)
    
    return df_artists, df_tracks, df_top200

