# ------------------------------------------------------------------------- 
# Bayesian Optimization Workflow for Medslik-II Simulations
# Copyright (c) 2023-2024 CMCC Foundation
# Licensed under The MIT License [see LICENSE for details]
# Written by Augusto Sepp Nieves, Marco Mariano De Carlo, Gabriele Accarino
# -------------------------------------------------------------------------

from shapely.geometry import Polygon
import numpy as np
import matplotlib.pyplot as plt
import netCDF4
import pandas as pd
from scipy.interpolate import NearestNDInterpolator
import os
from datetime import  *
from matplotlib import colors as c
from mpl_toolkits.basemap import Basemap
import geopandas as gpd
import glob

import sys
sys.path.append("/work/asc/machine_learning/projects/iMagine/bayes_opt_mdk2")

from library.Metrics.metrics import fss

from src.service.MDK2SimExtentService import MDK2SimExtentService
from src.service.MDK2SimDateService import MDK2SimDateService

from src.controller.PathController import PathController

class MetricsServiceImpl:
    
    def __init__(self):
        """ Initializes useful instances for method development """
                
        self.path_controller_instance = PathController()
        self.mdk2_sim_date_instance = MDK2SimDateService()
        self.mdk2_sim_extent_instance = MDK2SimExtentService()
        
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
    
    def get_surface_parcels_service_impl(self, fname,time_index):
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
        # Obtain year, month, day, hour, and minute from the simulation date instance
        yy = self.mdk2_sim_date_instance.get_year()
        mm = self.mdk2_sim_date_instance.get_month()
        dd = self.mdk2_sim_date_instance.get_day()
        hh = self.mdk2_sim_date_instance.get_hour()
        mmin = self.mdk2_sim_date_instance.get_minutes()

        # Convert the date components into a Python ordinal date and set the start time
        iStartDay = date(int(yy),int(mm),int(dd)).toordinal()
        iStartHour = int(hh)
        iStartMinute = int(mmin)

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

        return idx
    
    def compute_sin_fss(self, simulation_folder, observation_shp, output_folder):
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

        # Calculate area covered by each grid cell (assuming a square grid)
        area = (grid_resolution*110.)**2

        # Define a fill value (assuming it's used for missing or invalid data)
        fillval = 0

        # Construct the file path to the spill properties NetCDF file
        fname = simulation_folder + '/spill_properties.nc'

        # Open the spill properties NetCDF file for reading
        nc_read = netCDF4.Dataset(fname, 'r')

        # Obtain simulation date and observation date
        simulation_date = self.get_mdksim_date_service_impl()
        observation_date = self.get_obs_date_service_impl(observation_shp)

        # Find the time index of the simulation data closest to the observation date
        time_index = self.find_nearest_service_impl(simulation_date, observation_date)

        # Construct an identifier for the current simulation output based on simulation name and time index
        # xp_identifier = self.mdk2_sim_extent_instance.get_SIM_NAME() + '_' + '%02d' % (time_index+1) + 'h_' 
        xp_identifier = self.path_controller_instance.get_sim_str() + '_' + '%02d' % (time_index+1) + 'h_' 


        # for time_index in output_timesteps:
        print(':::::::::: TIME_INDEX :: ' + str(time_index))
        print(xp_identifier)


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

        # Save the plot as a PNG image file
        plt.savefig(output_folder + '/overlay_' + xp_identifier + '.png',dpi=600,bbox_inches='tight')

        # Save FSS output and event set data as text files
        np.savetxt(output_folder + '/fss_' + xp_identifier + '.txt',fss_output)
        np.savetxt(output_folder + '/event_set_' + xp_identifier + '.txt',event_set)
        
        # Create a new figure for plotting
        plt.figure()

        # Plot aggregated FSS output
        plt.plot(fss_output[:,0]*verif_grid_resolution,fss_output[:,1],'.-')

        # Save the plot as a PNG image file
        plt.savefig(output_folder + '/agg_fss_' + xp_identifier + '.png',dpi=600,bbox_inches='tight')

        # Close all figures
        plt.close('all')

    def get_sim_date_service_impl(self, yy, mm, dd, hh):
        """
        Calculates the ordinal date and time for a given simulation date and time.

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
        Calculates the ordinal date and time for a given slick ID.

        Args:
            slick_id (str): The slick ID.

        Returns:
            float: The ordinal date and time.
        """
        return date(int(slick_id[0:4]),int(slick_id[4:6]),int(slick_id[6:8])).toordinal() + float(slick_id[9:11])/24.

    def compute_multi_fss_service_impl(self):
        """
        Computes the maximum Fractions Skill Score (FSS) for multiple observations.

        Returns:
            float: The maximum FSS value.
        """
        # Get a list of observation folders
        # list_of_obs = glob.glob(self.path_controller_instance.get_OBS() + self.path_controller_instance.get_DAYS_GROUP())

        # Convert the initial date into a datetime object
        initial_date = datetime.strptime("20" + 
                                         self.mdk2_sim_date_instance.get_year() +
                                          self.mdk2_sim_date_instance.get_month() + 
                                          self.mdk2_sim_date_instance.get_day(),
                                          "%Y%m%d")
        
        num_days = ''.join([c for c in self.mdk2_sim_extent_instance.get_sim_lenght() if c != '0'])

        # Retrieve and concatenate the OBS directly for each incremented date
        list_of_obs = [obs for date in map(lambda x: initial_date + timedelta(days=x), range(int(int(num_days)/12)))
                       for obs in glob.glob(os.path.join(self.path_controller_instance.get_OBS(), 
                                                         date.strftime("%Y%m%d") + "*"))]
		
        # Get simulation length and date
        # sim_lenght = self.mdk2_sim_extent_instance.get_sim_lenght()

        yy = self.mdk2_sim_date_instance.get_year()
        mm = self.mdk2_sim_date_instance.get_month()
        dd = self.mdk2_sim_date_instance.get_day()
        hh = self.mdk2_sim_date_instance.get_hour()

        sim_date = self.get_sim_date_service_impl(self.mdk2_sim_date_instance.get_year(), 
                                                  self.mdk2_sim_date_instance.get_month(), 
                                                  self.mdk2_sim_date_instance.get_day(), 
                                                  self.mdk2_sim_date_instance.get_hour())

        # Initialize a DataFrame to store FSS results
        fss_df = pd.DataFrame(columns=['folder', 'fss'])

        obs = 0
        for slick_folder in list_of_obs:
            
            # Extract slick ID from the folder path
            null, slick_id = os.path.split(slick_folder)
            
            slick_date = self.get_slick_date_service_impl(slick_id)

            # Check if the difference between slick date and simulation date is within simulation length
            if (slick_date-sim_date) < float(self.mdk2_sim_extent_instance.get_sim_lenght())/24:

                # Create a detection directory for each observation
                self.path_controller_instance.create_detection_dir(str(obs))
                
                # Compute FSS for the current observation
                self.compute_sin_fss(self.path_controller_instance.get_MEDSLIK_OUT_DIR(), 
                                     slick_folder, 
                                     self.path_controller_instance.get_detection_dir(str(obs)))

                # Get FSS results for the current observation
                files = glob.glob(os.path.join(self.path_controller_instance.get_detection_dir(str(obs)), 
                                               f"fss_{self.path_controller_instance.get_sim_str()}*.txt"))

                for file in files:
            
                    f = pd.read_csv(file, sep = ' ', header = None)
        
                    row = pd.DataFrame([{"folder" : self.path_controller_instance.get_sim_result_dir(), 
                                         "fss" : round(f.iloc[0,1], 4)}])
                    fss_df = pd.concat([fss_df, row])

                obs += 1
        
        # Get the maximum FSS value
        FSS = fss_df['fss'].max()
        print(FSS)
    
        return FSS