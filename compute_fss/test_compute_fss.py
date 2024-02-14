import os

import sys
sys.path.append('/work/asc/machine_learning/projects/iMagine/bayes_opt')
from library.Metrics.metrics import fss

from compute_fss.test_compute_fss_lib import get_grid_resolution, get_surface_parcels, find_nearest, get_mdksim_date, get_obs_date, \
                                get_parcels_gdf,get_observation_df, get_xp_identifier, get_obs_bounds, get_lonlat_minmax, make_poly_grid, \
                                get_grid_centroid, get_event_set,get_cell_total_volume, get_model_spill, get_gridded_observation,\
                                get_model_and_obs, get_X___Y, get_int_mod_obs_int, get_arr_model_obs_union,\
                                get_fss_output, get_mdksim_id, create_out_file
                                

# forecast_folder -> simulation_folder
# observation_folder -> observation_shp -> #'/Users/asepp/work/imagine/observations/20210824-0343-SYR-PL-B-01-S1/20210824-0343-SYR-PL-B-01-S1.shp'

def compute_single_fss(simulation_folder, observation_folder, output_folder):
    
    counter=0
    cc = 0
    
    verif_grid_resolution = .15
    # set search window sizes  (in number of pixes)
    horizontal_scales = range(1,150,2) # horizontal_scales = range(1,11,2) per aumentare la scala
    fname = os.path.join(simulation_folder, 'spill_properties.nc')
    # fname = simulation_folder + '/spill_properties.nc'
    
    # set mapping projection
    crs = "+proj=merc +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs"
    
    #print('fname: ', fname)

    grid_resolution = get_grid_resolution(verif_grid_resolution)
    simulation_date = get_mdksim_date(simulation_folder)
    observation_date = get_obs_date(observation_folder)
    sim_identifier=get_mdksim_id(simulation_folder)
    time_index = find_nearest(simulation_date, observation_date)
    lons_f, lats_f, surface_volumes = get_surface_parcels(fname, time_index)
    parcels_gdf = get_parcels_gdf(lats_f, lons_f, surface_volumes, crs)
    observation_gdf = get_observation_df(observation_folder)
    xp_identifier = get_xp_identifier(sim_identifier, time_index)
    
    # generate comparison grid
    # comparison grid is a common grid covering observed and modelled spills
    # the grid resolution has been set, for now, at 150m
    obs_bounds = get_obs_bounds(observation_gdf)
    #print('lons_f:', lons_f)
    #print('lats_f:', lats_f)
    lonmin, latmin, lonmax, latmax = get_lonlat_minmax(lons_f, lats_f)
    
    output_frame = make_poly_grid(lonmin,lonmax,latmin,latmax,grid_resolution)
    grid_centroid = get_grid_centroid(output_frame, crs)
    event_set = get_event_set(grid_centroid)
    cell_total_volume = get_cell_total_volume(parcels_gdf, output_frame)
    
    if obs_bounds.minx[0] < lonmin:
        lonmin=obs_bounds.minx[0]
    if obs_bounds.maxx[0] > lonmax:
        lonmax=obs_bounds.maxx[0]
    if obs_bounds.miny[0] < latmin:
        latmin=obs_bounds.miny[0]
    if obs_bounds.maxy[0] > latmax:
        latmax=obs_bounds.maxy[0]
    
    for ii in grid_centroid:
        event_set[counter,0]=counter
        event_set[counter,1]=ii.coords[0][0]
        event_set[counter,2]=ii.coords[0][1]   
        counter=counter+1
    
    # 1. Place them into "cell" array with their associated coordinates
    modelled_spill = get_model_spill(output_frame, cell_total_volume)
    
    for ii in range(0,len(modelled_spill)):
        counter = modelled_spill.iloc[ii].name
        event_set[counter,3]=modelled_spill.iloc[ii].cell_total_volume/modelled_spill.iloc[ii].cell_total_volume     
    
    # 2. Fit satellite observation (spill shape) into visualization grid
    gridded_observation = get_gridded_observation(output_frame, observation_gdf)
    
    for ii in range(0,len(gridded_observation)):
        counter = gridded_observation.iloc[ii].name
        event_set[counter,4]=1      
    # gridded_observation.to_file('observation.shp')   
    
    # 3. Find areas where model and observations coincide on oil detection
    model_and_obs= get_model_and_obs(output_frame, observation_gdf)
    
    for ii in range(0,len(model_and_obs)):
        counter = model_and_obs.iloc[ii].name
        event_set[counter,5]=1

    # 4. Compute Fractional Skill Score
    X,Y= get_X___Y(event_set)
    interp_model, interp_observation, interp_intersection = get_int_mod_obs_int(event_set)
    array_model, array_observation, array_intersection, array_observation, array_union = get_arr_model_obs_union(interp_model, interp_observation, interp_intersection, X, Y)
    fss_output = get_fss_output(horizontal_scales)
    
    for hh in horizontal_scales:
        
        fss_ = fss(array_model, array_observation, 1, hh)
        fss_output[cc,0]=hh
        fss_output[cc,1]=fss_
        cc=cc+1
        
    create_out_file(lonmin, latmin, lonmax, latmax, X, Y, array_union, output_folder, xp_identifier, fss_output, event_set, verif_grid_resolution, time_index)
    
    
    
    
    
    
        
    
    
    
