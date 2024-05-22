# -------------------------------------------------------------------------------------
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Augusto Sepp Nieves, Marco Mariano De Carlo, Gabriele Accarino, Igor Atake
# -------------------------------------------------------------------------------------

from shapely.geometry import Polygon
import numpy as np
import matplotlib.pyplot as plt
import netCDF4
import pandas as pd
from scipy.interpolate import NearestNDInterpolator
import os
from datetime import  *
from matplotlib import colors as c
from matplotlib.patches import Patch
from mpl_toolkits.basemap import Basemap
import geopandas as gpd
import glob
import xarray as xr
from shapely.geometry import Point
import re
import calendar

from library.Metrics.metrics import fss

from src.service.BayOptSetupService import BayOptSetupService
from src.service.MDK2SimExtentService import MDK2SimExtentService
from src.service.MDK2SimDateService import MDK2SimDateService
from src.service.MDK2SimParamsService import MDK2SimParamsService

from src.controller.PathController import PathController

class MetricsServiceImpl:
    
    def __init__(self):
        """ Initializes useful instances for method development """
                
        self.path_controller_instance = PathController()
        self.bay_opt_setup_instance = BayOptSetupService()
        self.mdk2_sim_date_instance = MDK2SimDateService()
        self.mdk2_sim_extent_instance = MDK2SimExtentService()
        self.mdk2_sim_params_instance = MDK2SimParamsService()
        
        self.path_controller_instance = PathController()
        
    def esse_sbl_2021_service_impl(self, a, b, c, d):
        """
        Calculates the result of a mathematical operation

        Args:
            a (int or float): The first parameter.
            b (int or float): The second parameter.
            c (int or float): The third parameter.
            d (int or float): The fourth parameter.

        Returns:
            float: The result of the operation ((a + c) / (a + b + c + d)).
        """
        return (a+c)/(a+b+c+d)
    
    def fbias_sbl_2021_service_impl(self, a, b, c, d):
        """
        Calculates the Frequency Bias (FBIAS) for a given set of parameters.

        Args:
            a (int or float): The number of hits.
            b (int or float): The number of misses.
            c (int or float): The number of false alarms.
            d (int or float): The number of correct rejections.

        Returns:
            float: The Frequency Bias (FBIAS) value calculated as (a + b) / (a + c).
        """
        return (a+b)/(a+c)

    def barrelToTonnes_service_impl(self, oil_density):
        """
        Converts a quantity of oil from barrels to metric tonnes.

        Args:
            oil_density (float): The density of the oil in kilograms per cubic meter (kg/m^3).

        Returns:
            float: The equivalent quantity of oil in metric tonnes.
        """
        # Define the conversion factor from barrels to cubic meters (m^3)
        rbm3 = 0.158987
        return 1 / (rbm3 * (oil_density / 1000))
    
    def get_surface_parcels_service_impl(self, fname, time_index):
        """
        Retrieves surface parcel data from a NetCDF file at a specific time index.

        Args:
            fname (str): The filename of the NetCDF file.
            time_index (int): The index of the time dimension to retrieve data for.

        Returns:
            tuple: A tuple containing longitude, latitude, and surface volume data for floating particles.
        """
        # Open the NetCDF file
        f = netCDF4.Dataset(fname)

        # Extract data from the NetCDF file
        lat = np.longdouble(f.variables['latitude'][time_index,:])
        lon = np.longdouble(f.variables['longitude'][time_index,:])
        evaporative_volume = f.variables['evaporative_volume'][time_index,:]
        non_evaporative_volume = f.variables['non_evaporative_volume'][time_index,:]
        particle_status = f.variables['particle_status'][time_index, :]

        # Extract oil density from the file
        oil_density = f.variables['non_evaporative_volume'].oil_density

        # Convert oil volume from barrels to metric tonnes
        barrel2tonnes = self.barrelToTonnes_service_impl(oil_density)   

        # Identify floating particles
        floatingParticles=np.logical_and(particle_status > 0, particle_status <= 2).nonzero()[0]

        # Extract data for floating particles
        lons_f=lon[floatingParticles]
        lats_f=lat[floatingParticles]

        # Calculate surface volume for floating particles
        surf_volume = (evaporative_volume[floatingParticles] + non_evaporative_volume[floatingParticles]) / barrel2tonnes

        return lons_f,lats_f,surf_volume

    def make_poly_grid_service_impl(self, xmin,xmax,ymin,ymax,cell_size,crs):
        """
        Generates a grid of polygons covering a specified extent.

        Args:
            xmin (float): The minimum x-coordinate of the grid extent.
            xmax (float): The maximum x-coordinate of the grid extent.
            ymin (float): The minimum y-coordinate of the grid extent.
            ymax (float): The maximum y-coordinate of the grid extent.
            cell_size (float): The size of each grid cell.
            crs (str): The coordinate reference system (CRS) of the generated polygons.

        Returns:
            GeoDataFrame: A GeoDataFrame containing polygons representing the grid cells.
        """
        # Generate lists of column and row coordinates based on the extent and cell size
        cols = list(np.arange(xmin, xmax+cell_size, cell_size))
        rows = list(np.arange(ymin, ymax+cell_size, cell_size))

        # Initialize a list to store generated polygons
        polygons = []

        # Iterate over columns and rows to create grid polygons
        for x in cols[:-1]:
            for y in rows[:-1]:
                # Create a polygon for each grid cell
                polygons.append(Polygon([(x,y), (x+cell_size, y), (x+cell_size, y+cell_size), (x, y+cell_size)]))
                
        # Create a GeoDataFrame from the list of polygons
        cell = gpd.GeoDataFrame({'geometry':polygons}).set_crs('EPSG:4326',allow_override=True)

        return cell
    
    def get_obs_date_service_impl(self, observation_shp):
        """
        Extracts the observation date from a shapefile.

        Args:
            observation_shp (str): The file path to the shapefile containing the observation data.

        Returns:
            float: The observation date represented as a float (ordinal date with fractional hour).
        """
        # Read the observation shapefile into a GeoDataFrame
        observation_df = gpd.read_file(observation_shp)

        # Extract the observation date string from the 'IDENTIFIER' column of the GeoDataFrame
        observation_date_string = observation_df.IDENTIFIER[0]

        # Extract year, month, day, hour, and minute from the observation date string
        year=int(observation_date_string[0:4])
        month=int(observation_date_string[4:6])
        day=int(observation_date_string[6:8])
        hour=int(observation_date_string[9:11])
        minute=int(observation_date_string[11:13])
        
        # Convert the extracted components into a Python date object
        obs_date = date(year,month,day).toordinal()

        # Add the fractional part representing the hour
        obs_date = obs_date + hour/24.
        
        return obs_date

    def get_mdksim_date_service_impl(self):
        """
        Retrieves the simulation date and time.

        Returns:
            numpy.ndarray: An array representing the simulation date and time.
        """
        # get sim _ info
        with open(self.path_controller_instance.get_MEDSLIK_RUN() + '/config1.txt',encoding='iso-8859-1') as f:
            lines = f.readlines()
        # sim_length
        ss = lines[3]
        rr = re.search('=(.*)\n',ss)
        sim_length = int(lines[1][11:15])
        # sim_day
        ss = lines[5]
        rr = re.search('=(.*)\n',ss)
        dd = int(rr.group(1))
        # sim_month
        ss = lines[6]
        rr = re.search('=(.*)\n',ss)
        mm = int(rr.group(1))
        # sim_year
        ss = lines[7]
        rr = re.search('=(.*)\n',ss)
        yy = rr.group(1)
        yy = '20' + yy
        # sim_hora
        ss = lines[8]
        rr = re.search('=(.*)\n',ss)
        hh = int(rr.group(1))
        # sim_minute
        ss = lines[9]
        rr = re.search('=(.*)\n',ss)

        # Convert the date components into a Python ordinal date and set the start time
        iStartDay = date(int(yy),int(mm),int(dd)).toordinal()
        iStartHour = int(hh)

        """     
        Set time steps of interest (hours by default -- Python counting starts from 0).
        It may be a single number e.g. [146] or a list of numbers e.g. np.arange(0,15)
        outputs can be every 6h, for instance, by changing the steps in np.arange to 6,
        for instance
        """
        # Obtain the simulation length and create a timeline array with time steps
        sim_length = self.mdk2_sim_extent_instance.get_sim_lenght()
        time_line = np.arange(0,int(sim_length),1)

        # Convert time steps to real time by adding the start time and dividing by 24
        real_time = time_line/24. + (iStartHour+1.)/24. + iStartDay
        
        return real_time

    def find_nearest_service_impl(self, array, value):
        """
        Finds the index of the nearest value in an array to a given value.

        Args:
            array (array-like): The array to search.
            value (float): The target value.

        Returns:
            int: The index of the nearest value in the array.
        """
        # Convert the array to a NumPy array if it's not already
        array = np.asarray(array)

        # Find the index of the element in the array closest to the target value
        idx = (np.abs(array - value)).argmin()

        return idx + 1
    
    def get_time_index(self, simulation_date, observation_date):
        return self.find_nearest_service_impl(simulation_date, observation_date)
    
    def compute_sin_fss(self, simulation_folder, observation_shp, output_folder, values: list):
        """
        Computes the Fractions Skill Score (FSS)

        Args:
            simulation_folder (str): The folder containing simulation outputs.
            observation_shp (str): The file path to the shapefile containing observation data.
            output_folder (str): The folder where the FSS results will be saved.
        """

        # Set the spatial resolution for the verification grid (in km)
        verif_grid_resolution = .15

        # Set mapping projection
        crs = "+proj=merc +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs"

        # Calculate grid resolution in degrees
        grid_resolution = np.longdouble(verif_grid_resolution)/110.

        # Construct the file path to the spill properties NetCDF file
        fname = simulation_folder + '/spill_properties.nc'

        # Obtain simulation date and observation date
        # simulation_date = self.get_mdksim_date_service_impl()
        # observation_date = self.get_obs_date_service_impl(observation_shp)

        # Find the time index of the simulation data closest to the observation date
        time_index = self.get_time_index(self.get_mdksim_date_service_impl(), self.get_obs_date_service_impl(observation_shp))

        # Construct an identifier for the current simulation output based on simulation name and time index
        # xp_identifier = self.mdk2_sim_extent_instance.get_SIM_NAME() + '_' + '%02d' % (time_index+1) + 'h_' 
        xp_identifier = self.path_controller_instance.get_sim_str() + '_' + '%02d' % (time_index+1) + 'h_' 


        # for time_index in output_timesteps:
        # print(':::::::::: TIME_INDEX :: ' + str(time_index))
        # print(xp_identifier)


        """
        Filter out beached, dispersed, sunk and unreleased parcels
        lons_f = longitude coordinates of each oil parcel
        lats_f = latitude coordinates of each oil parcel    
        surface_volumes = total volumes (evaporative and non evaporative) for each parcel found on the surface
        """
        lons_f,lats_f,surface_volumes = self.get_surface_parcels_service_impl(fname,time_index)

        # Create dataframe with the location and volume of surface parcels
        df_gpan = pd.DataFrame({"lat":lats_f,
                    "lon":lons_f,
                    "vol":surface_volumes})
                    
        # Create geodataframe from pandas dataframe              
        # parcels_gdf = gpd.GeoDataFrame(df_gpan, 
        #             geometry=gpd.points_from_xy(df_gpan.lon, df_gpan.lat),
        #             crs=crs) 
        parcels_gdf = gpd.GeoDataFrame(df_gpan, 
                    geometry=gpd.points_from_xy(df_gpan.lon, df_gpan.lat),crs=crs).set_crs('EPSG:4326',allow_override=True)
        parcels_gdf = parcels_gdf.drop(columns=['lon', 'lat']) # remove useless variables
                    
        # load satellite detection shapefile
        observation_df = gpd.read_file(observation_shp)
        # observation_gdf = gpd.GeoDataFrame(observation_df[['geometry']],crs=crs)

        observation_gdf = gpd.GeoDataFrame(observation_df[['geometry']]).set_crs('EPSG:4326',allow_override=True)

        
        """
        Generate comparison grid
        comparison grid is a common grid covering observed and modelled spills
        the grid resolution has been set, for now, at 150m S
        """
        # first, getting observation bounds
        obs_bounds = observation_gdf.bounds

        lonmin=np.min(lons_f)
        latmin=np.min(lats_f)
        lonmax=np.max(lons_f)
        latmax=np.max(lats_f)
        
        if obs_bounds.minx[0] < lonmin:
            lonmin=obs_bounds.minx[0]
        if obs_bounds.maxx[0] > lonmax:
            lonmax=obs_bounds.maxx[0]
        if obs_bounds.miny[0] < latmin:
            latmin=obs_bounds.miny[0]
        if obs_bounds.maxy[0] > latmax:
            latmax=obs_bounds.maxy[0]
        
        # create grid polygon consisting of multiple polygons describing squared grid cells    
        output_frame = self.make_poly_grid_service_impl(lonmin,lonmax,latmin,latmax,grid_resolution,crs)

        # (AUGUSTO SEPP ----- MODIFIED)
        output_frame.set_crs('EPSG:4326',allow_override=True)

        """
        Create numpy-compatible grid 
        by first getting the central coordinates of each grid cell
        """
        #grid_centroid = np.asarray(output_frame['geometry'].centroid) 
        grid_centroid = output_frame['geometry'].to_crs(crs).centroid.to_crs(output_frame.crs)

        """
        Then running through grid points (indices) and creating an output matrix "event_set"
        containing:
        column 0: cell index
        column 1: longitude coordinate of grid cell centroid
        column 2: latitude coordinate of grid cell centroid  
        column 3: simulated oil presence/absence
        column 4: observed oil presence/absence
        column 5: intersection between simulated and observed oil
        """
        counter=0
        event_set=np.zeros((len(grid_centroid),6))*np.nan
        
        for ii in grid_centroid:
            event_set[counter,0]=counter
            event_set[counter,1]=ii.coords[0][0]
            event_set[counter,2]=ii.coords[0][1]   
            counter=counter+1 
        # and save grid polygon
        # output_frame.to_file('grid.shp')    
        
        # Group your parcels into visualization grid
        gridded_parcels = gpd.sjoin(parcels_gdf,output_frame, how='left', op='within').set_crs('EPSG:4326',allow_override=True)

        # Aggregate volumes to grid cells with dissolve 
        gridded_parcels['cell_total_volume']=1
        cell_total_volume = gridded_parcels.dissolve(by="index_right", aggfunc="count")   

        # Place them into "cell" array with their associated coordinates   
        output_frame.loc[cell_total_volume.index, 'cell_total_volume'] = cell_total_volume.cell_total_volume.values    
        modelled_spill = output_frame[output_frame['cell_total_volume'] > 0]
        
        for ii in range(0,len(modelled_spill)):
            counter = modelled_spill.iloc[ii].name
            event_set[counter,3]=modelled_spill.iloc[ii].cell_total_volume/modelled_spill.iloc[ii].cell_total_volume

        # Fit satellite observation (spill shape) into visualization grid
        gridded_observation = gpd.sjoin(left_df=output_frame, right_df=observation_gdf[['geometry']], how='inner').set_crs('EPSG:4326',allow_override=True)
        for ii in range(0,len(gridded_observation)):
            counter = gridded_observation.iloc[ii].name
            event_set[counter,4]=1      
        # gridded_observation.to_file('observation.shp')
            
        # Find areas where model and observations coincide on oil detection
        model_and_obs= gpd.sjoin(left_df=output_frame[output_frame['cell_total_volume'] > 0], right_df=observation_gdf[['geometry']], how='inner')
        for ii in range(0,len(model_and_obs)):
            counter = model_and_obs.iloc[ii].name
            event_set[counter,5]=1

        """
        Compute your Fractional Skill Score
        """ 
        X,Y=np.meshgrid(np.unique(event_set[:,1]),np.unique(event_set[:,2]))
        interp_model=NearestNDInterpolator(list(zip(event_set[:,1],event_set[:,2])),event_set[:,3])
        interp_observation=NearestNDInterpolator(list(zip(event_set[:,1],event_set[:,2])),event_set[:,4])
        # interp_intersection=NearestNDInterpolator(list(zip(event_set[:,1],event_set[:,2])),event_set[:,5])
        
        array_model = interp_model(X, Y)
        array_observation = interp_observation(X, Y)   
        # array_intersection = interp_intersection(X, Y)    
        
        array_model[np.isnan(array_model)] = 0
        array_observation[np.isnan(array_observation)] = 0

        array_union = array_model+2*array_observation
        array_union[array_union==0]=np.nan
        
        # Set search window sizes  (in number of pixes)
        horizontal_scales = range(1,150,2) # horizontal_scales = range(1,11,2) per aumentare la scala
        fss_output=np.zeros((len(horizontal_scales),2))
        
        cc = 0
        for hh in horizontal_scales:         
            fss_= fss(array_model, array_observation, 1, hh)
            fss_output[cc,0]=hh
            fss_output[cc,1]=fss_
            cc=cc+1

        """
        Plotting and saving results
        """
        # Create a new figure for plotting
        plt.figure()

        fig, ax = plt.subplots(figsize=(10, 5))

        # Define labels for the legend
        labels = {'Yellow': 'MDK-II simulation', 'Blue': 'Observation', 'Magenta': 'Overlap between MDK-II sim and Observation'}

        # Define a colormap for the plot
        cMap = c.ListedColormap(['y','b','m'])

        # Create a Basemap object for plotting geographical data
        m = Basemap(llcrnrlon=lonmin,llcrnrlat=latmin,\
                    urcrnrlon=lonmax,urcrnrlat=latmax,\
                    rsphere=(6378137.00,6356752.3142),\
                    resolution='i',projection='merc',\
                    lat_0=(latmax + latmin)/2.,\
                    lon_0=(lonmax + lonmin)/2.,epsg=4326)
        
        # Convert grid coordinates to map coordinates
        x_map,y_map=m(X,Y)

        # Plot the array on the map using a specified colormap
        m.pcolor(x_map,y_map,array_union,cmap=cMap)

        # Draw coastlines on the map
        m.drawcoastlines()

        # Fill continents with a specified alpha value
        m.fillcontinents(alpha=1,zorder=3)

        # Draw meridians and parallels on the map with specified intervals and labels
        m.drawmeridians(np.arange(lonmin,lonmax,(lonmax-lonmin)/4.), labels=[0,0,0,1],color='white',linewidth=0.03, fontsize = 5)
        m.drawparallels(np.arange(latmin,latmax,(latmax-latmin)/4.),labels=[1,0,0,0],color='white',linewidth=0.03, fontsize = 5)

        # Legend
        legend_elements = [Patch(facecolor=color, edgecolor='None', label=label) for color, label in labels.items()]
        legend = ax.legend(handles=legend_elements, loc='upper center', fontsize=5, bbox_to_anchor=(0.5, -0.05), ncol=3, edgecolor='None')
        plt.setp(legend.get_title(), fontsize='large', fontname='sans-serif')

        config_keys = list(self.mdk2_sim_params_instance.get_config_keys())
        reversed_config_keys = config_keys[::-1]

        description = ""
        for item1, item2 in zip(reversed_config_keys, values):
            description += f"{item1} : {np.round(float(item2), 2)}\n"

        description += "\n"

        description += f"Simulation init date: {self.mdk2_sim_date_instance.get_day()} {calendar.month_name[int(self.mdk2_sim_date_instance.get_month())]} 20{self.mdk2_sim_date_instance.get_year()} \nSimulation init hour: {self.mdk2_sim_date_instance.get_hour()}:{self.mdk2_sim_date_instance.get_minutes()} \nNumber of simulated particles: {self.mdk2_sim_params_instance.get_particles_value()} \n{self.bay_opt_setup_instance.get_eval_metric()}: {np.round(fss_output[:,1].min(), 2)}"
        
        ax.text(0.5, -0.10, description, transform=ax.transAxes, fontsize=7, ha='center', va='top', bbox=dict(facecolor='white', edgecolor='none'))

        title = f"MDK-II BayesOpt Simulation in {self.mdk2_sim_extent_instance.get_SIM_NAME()} \n after {'%02d' % (time_index)}h from last detection"

        # Add title
        plt.title(title, fontweight='bold', fontname='sans-serif', fontsize=10, color='black', pad=15)

        # Save the plot as a PNG image file
        plt.savefig(output_folder + f'/{self.bay_opt_setup_instance.get_eval_metric()}_' + xp_identifier + '.png',dpi=600,bbox_inches='tight')

        # Save FSS output and event set data as text files
        np.savetxt(output_folder + f'/{self.bay_opt_setup_instance.get_eval_metric()}_' + xp_identifier + '.txt',fss_output)
        np.savetxt(output_folder + '/event_set_' + xp_identifier + '.txt',event_set)
        
        # Create a new figure for plotting
        plt.figure()

        # Plot aggregated FSS output
        plt.plot(fss_output[:,0]*verif_grid_resolution,fss_output[:,1],'.-')

        # Save the plot as a PNG image file
        plt.savefig(output_folder + '/agg_fss_' + xp_identifier + '.png',dpi=600,bbox_inches='tight')

        # Close all figures
        plt.close('all')

        return np.round(fss_output[:,1].min(), 2)

    def get_sim_date_service_impl(self, yy, mm, dd, hh):
        """
        Computes the ordinal date and time for a given simulation date and time.

        Args:
            yy (str): The year in YY format.
            mm (str): The month as a string.
            dd (str): The day of the month as a string.
            hh (str): The hour as a string.

        Returns:
            float: The ordinal date and time.
        """
        return date(2000+int(yy),int(mm),int(dd)).toordinal()+ float(hh)/24.

    def get_slick_date_service_impl(self, slick_id):
        """
        Computes the ordinal date and time for a given slick ID.

        Args:
            slick_id (str): The slick ID.

        Returns:
            float: The ordinal date and time.
        """
        return date(int(slick_id[0:4]),int(slick_id[4:6]),int(slick_id[6:8])).toordinal() + float(slick_id[9:11])/24.

    def plt_result(self, lonmin, latmin, lonmax, latmax, X, Y, array_union, xp_identifier, output_folder, time_index, metric, values):

        """
        Generates and saves a result plot based on the provided data

        Args:
            lonmin (float) : 
                Minimum longitude of the area of interest.
            latmin (float) : 
                Minimum latitude of the area of interest.
            lonmax (float) : 
                Maximum longitude of the area of interest.
            latmax (float) : 
                Maximum latitude of the area of interest.
            X (numpy.ndarray) : 
                Array of X coordinates (longitudes) of data points.
            Y (numpy.ndarray) : 
                Array of Y coordinates (latitudes) of data points.
            array_union (numpy.ndarray) : 
                Matrix containing the data to be visualized in the plot.
            xp_identifier (str) : 
                Identifier of the experiment or dataset.
            output_folder (str) : 
                Path to the folder where the resulting plot will be saved.
            time_index (int) : 
                Time index to select the subset of data to be visualized.
            metric (str) : 
                Name of the metric or variable to be represented in the plot.
            values (list of float) : 
                Specific values associated with the data that can be used to color or label points in the plot.


        Returns:
            None :
                The function does not return anything but saves a plot to the specified path
        """

        # Create a new figure for plotting
        plt.figure()

        fig, ax = plt.subplots(figsize=(10, 5))

        # Define labels for the legend
        labels = {'Yellow': 'MDK-II simulation', 'Blue': 'Observation', 'Magenta': 'Overlap between MDK-II sim and Observation'}

        # Define a colormap for the plot
        cMap = c.ListedColormap(['y','b','m'])

        # Create a Basemap object for plotting geographical data
        m = Basemap(llcrnrlon=lonmin,llcrnrlat=latmin,\
                    urcrnrlon=lonmax,urcrnrlat=latmax,\
                    rsphere=(6378137.00,6356752.3142),\
                    resolution='i',projection='merc',\
                    lat_0=(latmax + latmin)/2.,\
                    lon_0=(lonmax + lonmin)/2.,epsg=4326)
        
        # Convert grid coordinates to map coordinates
        x_map,y_map=m(X,Y)

        # Plot the array on the map using a specified colormap
        m.pcolor(x_map,y_map,array_union,cmap=cMap)

        # Draw coastlines on the map
        m.drawcoastlines()

        # Fill continents with a specified alpha value
        m.fillcontinents(alpha=1,zorder=3)

        # Draw meridians and parallels on the map with specified intervals and labels
        m.drawmeridians(np.arange(lonmin,lonmax,(lonmax-lonmin)/4.), labels=[0,0,0,1],color='white',linewidth=0.03, fontsize = 5)
        m.drawparallels(np.arange(latmin,latmax,(latmax-latmin)/4.),labels=[1,0,0,0],color='white',linewidth=0.03, fontsize = 5)

        # Legend
        legend_elements = [Patch(facecolor=color, edgecolor='None', label=label) for color, label in labels.items()]
        legend = ax.legend(handles=legend_elements, loc='upper center', fontsize=5, bbox_to_anchor=(0.5, -0.05), ncol=3, edgecolor='None')
        plt.setp(legend.get_title(), fontsize='large', fontname='sans-serif')

        config_keys = list(self.mdk2_sim_params_instance.get_config_keys())
        reversed_config_keys = config_keys[::-1]

        description = ""
        for item1, item2 in zip(reversed_config_keys, values):
            description += f"{item1} : {np.round(float(item2), 2)}\n"

        description += "\n"

        # Add description
        description += f"Simulation init date: {self.mdk2_sim_date_instance.get_day()} {calendar.month_name[int(self.mdk2_sim_date_instance.get_month())]} 20{self.mdk2_sim_date_instance.get_year()} \nSimulation init hour: {self.mdk2_sim_date_instance.get_hour()}:{self.mdk2_sim_date_instance.get_minutes()} \nNumber of simulated particles: {self.mdk2_sim_params_instance.get_particles_value()} \n{self.bay_opt_setup_instance.get_eval_metric()}: {np.round(metric, 2)}"
        ax.text(0.5, -0.10, description, transform=ax.transAxes, fontsize=7, ha='center', va='top', bbox=dict(facecolor='white', edgecolor='none'))

        title = f"MDK-II BayesOpt Simulation in {self.mdk2_sim_extent_instance.get_SIM_NAME()} \n after {'%02d' % (time_index+1)}h from the init position"

        # Add title
        plt.title(title, fontweight='bold', fontname='sans-serif', fontsize=10, color='black', pad=15)

        # Save the plot as a PNG image file
        plt.savefig(output_folder + f'/{self.bay_opt_setup_instance.get_eval_metric()}_' + xp_identifier + '.png',dpi=600,bbox_inches='tight')
        
        # Create a new figure for plotting
        plt.figure()

        # Close all figures
        plt.close('all')

    def compute_multi_fss_service_impl(self, values):
        """
        Computes the Fraction Skill Score (FSS) for the chosen observation.

        values (list) : 
            Specific values associated with the data that can be used to color or label points in the plot

        Returns (float):
            The FSS value.
        """

        yy = self.mdk2_sim_date_instance.get_year()
        mm = self.mdk2_sim_date_instance.get_month()
        dd = self.mdk2_sim_date_instance.get_day()
        hh = self.mdk2_sim_date_instance.get_hour()
        mn = self.mdk2_sim_date_instance.get_minutes()

        self.path_controller_instance.create_detection_dir(f"20{yy}{mm}{dd}_{hh}{mn}")

        FSS = self.compute_sin_fss(self.path_controller_instance.get_MEDSLIK_OUT_DIR(), os.environ.get('OBSPATH').split(":")[1], self.path_controller_instance.get_detection_dir(f"20{yy}{mm}{dd}_{hh}{mn}"), values)
    
        return FSS
    
    def metric_overlay_service_impl(self,
                       coastline_path,
                       observation_path,
                       model_path,
                       output_folder,
                       values,
                       concave_hull_ratio = 0.4,
                       concave_hull = False
                    ):
        '''
        This function calculates the overlay metric (%) between an oil observarion (in shapefile) and a model output from Medslik-II (in netcdf)
        The metric is based on the % match between the area covered from a simulation in comparison with the real observed event.
        To obtain that, all the partciles from a given moment (model_hour) at the simulation are engulfed by a convex hull.
        Concave hull can be used, but need GEOS 3.11 to be present in the instalation and could not be straightforward. Standard ratio value is 0.4 (concave_hull_ratio)
        The value is simply the intersect area from model and observation divided by the observation area in percentage
        '''
        # Opening the observation shapefile
        observation = gpd.read_file(observation_path)

        # Opening the model output
        model = xr.open_dataset(model_path)

        # Find the time index of the simulation data closest to the observation date
        time_index = self.get_time_index(self.get_mdksim_date_service_impl(), self.get_obs_date_service_impl(observation_path))

        # Selecting the appropriate time step
        rec = model.isel(time = time_index)

        # List with lat and lon for each particle in the timestep output
        geom = []
        for p in range(0,len(rec.non_evaporative_volume)):
            if rec.particle_status[p].values > 0:
                geom.append(Point(rec.isel(parcel_id=p).longitude.values,rec.isel(parcel_id=p).latitude.values))
            else:
                pass

        #Create a point shapefile from the geometries in the list
        shp = gpd.GeoDataFrame(geometry=geom)

        #Transform the point shapefile on a polygon
        if concave_hull == True:
            model_polygon = gpd.GeoDataFrame(shp.dissolve().concave_hull(ratio=concave_hull_ratio))
        else:
            model_polygon = gpd.GeoDataFrame(geometry=shp.dissolve().geometry.convex_hull)

        #Subtracting values on land from the coastline
        coastline = gpd.read_file(coastline_path)
        
        # 1 degree buffer to collect more coastline
        buffer = 1
        
        #defining minimum and maximum of coordinates from the model output
        xmin = model_polygon.bounds['minx'] - buffer
        xmax = model_polygon.bounds['maxx'] + buffer
        ymin = model_polygon.bounds['miny'] - buffer
        ymax = model_polygon.bounds['maxy'] + buffer

        # Cropping to a smaller area
        coastline = coastline.cx[xmin:xmax, ymin:ymax]
        
        # Cropping the selected linestrings to the same bounding box
        coastline = gpd.GeoDataFrame(geometry=coastline.clip_by_rect(xmin.values.max(),ymin.values.max(),
                                        xmax.values.max(),ymax.values.max()))
        
        # RETAIN ONLY THE OIL ON WATER SURFACE, REMOVING LAND OVERLAY
        model_polygon = model_polygon.overlay(coastline, how='difference')
        
        # Create the intersection between model and observed oil slick
        overlay_shp = model_polygon.overlay(observation,how='intersection')
        
        # Calculates the metric (percentage)
        overlay_value = (overlay_shp.area / observation.area)

        fname = os.path.join(self.path_controller_instance.get_MEDSLIK_OUT_DIR(), "spill_properties.nc")

        # Set the spatial resolution for the verification grid (in km)
        verif_grid_resolution = .15

        # Set mapping projection
        crs = "+proj=merc +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs"

        # Calculate grid resolution in degrees
        grid_resolution = np.longdouble(verif_grid_resolution)/110.

        xp_identifier = self.path_controller_instance.get_sim_str() + '_' + '%02d' % (time_index) + 'h_'

        """
        Filter out beached, dispersed, sunk and unreleased parcels
        lons_f = longitude coordinates of each oil parcel
        lats_f = latitude coordinates of each oil parcel    
        surface_volumes = total volumes (evaporative and non evaporative) for each parcel found on the surface
        """
        lons_f,lats_f,surface_volumes = self.get_surface_parcels_service_impl(fname,time_index)

        # Create dataframe with the location and volume of surface parcels
        df_gpan = pd.DataFrame({"lat":lats_f,
                    "lon":lons_f,
                    "vol":surface_volumes})
                    
        parcels_gdf = gpd.GeoDataFrame(df_gpan, 
                    geometry=gpd.points_from_xy(df_gpan.lon, df_gpan.lat),crs=crs).set_crs('EPSG:4326',allow_override=True)
        
        # remove useless variables
        parcels_gdf = parcels_gdf.drop(columns=['lon', 'lat'])
                    
        # load satellite detection shapefile
        observation_df = gpd.read_file(observation_path)

        observation_gdf = gpd.GeoDataFrame(observation_df[['geometry']]).set_crs('EPSG:4326',allow_override=True)

        """
        Generate comparison grid
        comparison grid is a common grid covering observed and modelled spills
        the grid resolution has been set, for now, at 150m S
        """
        # first, getting observation bounds
        obs_bounds = observation_gdf.bounds

        lonmin=np.min(lons_f)
        latmin=np.min(lats_f)
        lonmax=np.max(lons_f)
        latmax=np.max(lats_f)
        
        if obs_bounds.minx[0] < lonmin:
            lonmin=obs_bounds.minx[0]
        if obs_bounds.maxx[0] > lonmax:
            lonmax=obs_bounds.maxx[0]
        if obs_bounds.miny[0] < latmin:
            latmin=obs_bounds.miny[0]
        if obs_bounds.maxy[0] > latmax:
            latmax=obs_bounds.maxy[0]
        
        # create grid polygon consisting of multiple polygons describing squared grid cells    
        output_frame = self.make_poly_grid_service_impl(lonmin,lonmax,latmin,latmax,grid_resolution,crs)

        # (AUGUSTO SEPP ----- MODIFIED)
        output_frame.set_crs('EPSG:4326',allow_override=True)

        """
        Create numpy-compatible grid 
        by first getting the central coordinates of each grid cell
        """
        #grid_centroid = np.asarray(output_frame['geometry'].centroid) 
        grid_centroid = output_frame['geometry'].to_crs(crs).centroid.to_crs(output_frame.crs)

        """
        Then running through grid points (indices) and creating an output matrix "event_set"
        containing:
        column 0: cell index
        column 1: longitude coordinate of grid cell centroid
        column 2: latitude coordinate of grid cell centroid  
        column 3: simulated oil presence/absence
        column 4: observed oil presence/absence
        column 5: intersection between simulated and observed oil
        """
        counter=0
        event_set=np.zeros((len(grid_centroid),6))*np.nan
        
        for ii in grid_centroid:
            event_set[counter,0]=counter
            event_set[counter,1]=ii.coords[0][0]
            event_set[counter,2]=ii.coords[0][1]   
            counter=counter+1 
        # and save grid polygon
        # output_frame.to_file('grid.shp')    
        
        # Group your parcels into visualization grid
        gridded_parcels = gpd.sjoin(parcels_gdf,output_frame, how='left', op='within').set_crs('EPSG:4326',allow_override=True)

        # Aggregate volumes to grid cells with dissolve 
        gridded_parcels['cell_total_volume']=1
        cell_total_volume = gridded_parcels.dissolve(by="index_right", aggfunc="count")   

        # Place them into "cell" array with their associated coordinates   
        output_frame.loc[cell_total_volume.index, 'cell_total_volume'] = cell_total_volume.cell_total_volume.values    
        modelled_spill = output_frame[output_frame['cell_total_volume'] > 0]
        
        for ii in range(0,len(modelled_spill)):
            counter = modelled_spill.iloc[ii].name
            event_set[counter,3]=modelled_spill.iloc[ii].cell_total_volume/modelled_spill.iloc[ii].cell_total_volume

        # Fit satellite observation (spill shape) into visualization grid
        gridded_observation = gpd.sjoin(left_df=output_frame, right_df=observation_gdf[['geometry']], how='inner').set_crs('EPSG:4326',allow_override=True)
        for ii in range(0,len(gridded_observation)):
            counter = gridded_observation.iloc[ii].name
            event_set[counter,4]=1      
        # gridded_observation.to_file('observation.shp')
            
        # Find areas where model and observations coincide on oil detection
        model_and_obs= gpd.sjoin(left_df=output_frame[output_frame['cell_total_volume'] > 0], right_df=observation_gdf[['geometry']], how='inner')
        for ii in range(0,len(model_and_obs)):
            counter = model_and_obs.iloc[ii].name
            event_set[counter,5]=1

        X,Y=np.meshgrid(np.unique(event_set[:,1]),np.unique(event_set[:,2]))
        interp_model=NearestNDInterpolator(list(zip(event_set[:,1],event_set[:,2])),event_set[:,3])
        interp_observation=NearestNDInterpolator(list(zip(event_set[:,1],event_set[:,2])),event_set[:,4])
        # interp_intersection=NearestNDInterpolator(list(zip(event_set[:,1],event_set[:,2])),event_set[:,5])
        
        array_model = interp_model(X, Y)
        array_observation = interp_observation(X, Y)   
        # array_intersection = interp_intersection(X, Y)    
        
        array_model[np.isnan(array_model)] = 0
        array_observation[np.isnan(array_observation)] = 0

        array_union = array_model+2*array_observation
        array_union[array_union==0]=np.nan

        self.plt_result(lonmin, latmin, lonmax, latmax, X, Y, array_union, xp_identifier, output_folder, time_index, overlay_value[0], values)
        
        return np.round(overlay_value[0], 2)
    
    def compute_multi_overlay_service_impl(self, values):

        """
        Computes and processes multiple overlays based on the provided values.

        Parameters:
            values (list) : 
                List of numerical values to be used in the computation of overlays.

        Returns:
            final_overlay (list) : 
                A list containing the results of the computed overlays. Each element
                in the list corresponds to a processed overlay based on the input values.
        """

        yy = self.mdk2_sim_date_instance.get_year()
        mm = self.mdk2_sim_date_instance.get_month()
        dd = self.mdk2_sim_date_instance.get_day()
        hh = self.mdk2_sim_date_instance.get_hour()
        mn = self.mdk2_sim_date_instance.get_minutes()

        model_path = os.path.join(self.path_controller_instance.get_MEDSLIK_OUT_DIR(), "spill_properties.nc")

        # Create a detection directory for each observation
        self.path_controller_instance.create_detection_dir(f"20{yy}{mm}{dd}_{hh}{mn}")
                
        # Compute overlay for the current observation
        overlay = self.metric_overlay_service_impl(self.path_controller_instance.get_GSHHS_DATA(), os.environ.get('OBSPATH').split(":")[1], model_path, self.path_controller_instance.get_detection_dir(f"20{yy}{mm}{dd}_{hh}{mn}"), values)

        return overlay