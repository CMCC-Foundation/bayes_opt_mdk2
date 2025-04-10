import geopandas as gpd
from shapely.geometry import box
import matplotlib.pyplot as plt
import numpy as np

import os

def get_bounding_box(shapefile_path):
    """
    Calcola gli estremi di un bounding box che racchiude l'intero shapefile.

    Args:
        shapefile_path (str): Percorso al file shapefile.

    Returns:
        dict: Un dizionario contenente minx, miny, maxx, maxy.
    """
    # Carica il shapefile
    gdf = gpd.read_file(shapefile_path)

    # Calcola il bounding box (minx, miny, maxx, maxy)
    bounds = gdf.total_bounds  # Restituisce [minx, miny, maxx, maxy]

    return {
        "minx": bounds[0],
        "miny": bounds[1],
        "maxx": bounds[2],
        "maxy": bounds[3],
    }

def crop_land_mask(shapefile_path, output_path, bounding_box):
    """
    Ritaglia una land mask (shapefile) utilizzando un bounding box.

    Args:
        shapefile_path (str): Percorso al file shapefile originale.
        output_path (str): Percorso per salvare il file shapefile ritagliato.
        minx (float): Coordinata minima X del bounding box.
        miny (float): Coordinata minima Y del bounding box.
        maxx (float): Coordinata massima X del bounding box.
        maxy (float): Coordinata massima Y del bounding box.

    Returns:
        None: Salva il risultato nel percorso specificato.
    """
    # Carica lo shapefile
    gdf = gpd.read_file(shapefile_path)

    minx = np.round(bounding_box['minx'], 2)
    miny = np.round(bounding_box['miny'], 2)
    maxx = np.round(bounding_box['maxx'], 2) + 0.5
    maxy = np.round(bounding_box['maxy'], 2)

    '''
    minx = bounding_box['minx']
    miny = bounding_box['miny']
    maxx = bounding_box['maxx']
    maxy = bounding_box['maxy']
    '''
    
    # Crea il bounding box come oggetto geometrico
    bounding_box = box(minx, miny, maxx, maxy)
    
    # Converti il bounding box in un GeoDataFrame con lo stesso CRS dello shapefile
    bbox_gdf = gpd.GeoDataFrame({"geometry": [bounding_box]}, crs=gdf.crs)
    
    # Intersezione: ritaglia lo shapefile con il bounding box
    cropped_gdf = gpd.overlay(gdf, bbox_gdf, how="intersection")

    fig, ax = plt.subplots(figsize = (15,15))

    cropped_gdf.plot(ax = ax, color = "brown", edgecolor = "black", alpha = 0.5, label = "Land")

    # Salva il risultato in un nuovo shapefile
    cropped_gdf.to_file(output_path)

def apply_land_mask(target_shapefile_path, land_mask_path, output_path):
    """
    Applica una land mask a un altro shapefile e rimuove le aree in comune.

    Args:
        target_shapefile_path (str): Percorso al file shapefile da modificare.
        land_mask_path (str): Percorso al file shapefile della land mask.
        output_path (str): Percorso per salvare il file shapefile risultante.

    Returns:
        None: Salva il risultato nel percorso specificato.
    """
    # Carica il shapefile target e la land mask
    target_gdf = gpd.read_file(target_shapefile_path)
    land_mask_gdf = gpd.read_file(land_mask_path)

    # Assicurati che entrambi abbiano lo stesso CRS
    if target_gdf.crs != land_mask_gdf.crs:
        land_mask_gdf = land_mask_gdf.to_crs(target_gdf.crs)

    # Unisci tutte le geometrie della land mask in una singola geometria
    land_mask_union = land_mask_gdf.unary_union

    # Rimuovi le parti in comune con la land mask
    target_gdf['geometry'] = target_gdf['geometry'].difference(land_mask_union)

    # Rimuovi geometrie vuote risultanti dall'operazione
    target_gdf = target_gdf[~target_gdf.is_empty]
    
    print(type(target_gdf))

    fig, ax = plt.subplots(figsize=(15,15))

    target_gdf.plot(ax = ax, color = "purple", edgecolor = "black", alpha = 0.5, label = "cropped_sim")

    # Salva il risultato in un nuovo shapefile
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    target_gdf.to_file(output_path)