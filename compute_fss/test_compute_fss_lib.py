import netCDF4
import geopandas as gpd
import pandas as pd
import numpy as np
from datetime import  *
import re
from shapely.geometry import Polygon
from scipy.interpolate import NearestNDInterpolator
import matplotlib.pyplot as plt
from matplotlib import colors as c
from mpl_toolkits.basemap import Basemap



def erre_sbl_2021(a,b,c,d):
    return (a+b)/(a+b+c+d)
def esse_sbl_2021(a,b,c,d):
    return (a+c)/(a+b+c+d)
def fbias_sbl_2021(a,b,c,d):
    return (a+b)/(a+c)

def barrelToTonnes(oil_density):
    rbm3 = 0.158987
    return 1 / (rbm3 * (oil_density / 1000))
  
def get_surface_parcels(fname,time_index):

    f = netCDF4.Dataset(fname)
    #print('time Index: ', time_index)
    
    lat = np.longdouble(f.variables['latitude'][time_index,:])
    lon = np.longdouble(f.variables['longitude'][time_index,:])
    evaporative_volume = f.variables['evaporative_volume'][time_index,:]
    non_evaporative_volume = f.variables['non_evaporative_volume'][time_index,:]
    particle_status = f.variables['particle_status'][time_index, :]
    oil_density = f.variables['non_evaporative_volume'].oil_density
    barrel2tonnes = barrelToTonnes(oil_density)   
    
    #print('lat:', lat)
    #print('lon:', lon)
    #print('particle status', particle_status)
    
    floatingParticles=np.logical_and(particle_status > 0, particle_status <= 2).nonzero()[0]
    #print('floating particles:', floatingParticles)
    lons_f=lon[floatingParticles]
    lats_f=lat[floatingParticles]
    surf_volume = (evaporative_volume[floatingParticles] + non_evaporative_volume[floatingParticles]) / barrel2tonnes

    return lons_f,lats_f,surf_volume

def make_poly_grid(xmin,xmax,ymin,ymax,cell_size):

    cols = list(np.arange(xmin, xmax+cell_size, cell_size))
    rows = list(np.arange(ymin, ymax+cell_size, cell_size))

    polygons = []
    for x in cols[:-1]:
        for y in rows[:-1]:
            polygons.append(Polygon([(x,y), (x+cell_size, y), (x+cell_size, y+cell_size), (x, y+cell_size)]))
            
    cell = gpd.GeoDataFrame({'geometry':polygons}).set_crs('EPSG:4326',allow_override=True)

    return cell
 
def get_obs_date(observation_shp):
    observation_df = gpd.read_file(observation_shp)
    observation_date_string = observation_df.IDENTIFIER[0]
    year=int(observation_date_string[0:4])
    month=int(observation_date_string[4:6])
    day=int(observation_date_string[6:8])
    hour=int(observation_date_string[9:11])
    minute=int(observation_date_string[11:13])
    
    obs_date = date(year,month,day).toordinal()
    obs_date = obs_date + hour/24.
    return obs_date
    
def get_mdksim_id(simulation_folder):
    
    # get sim _ info
    with open(simulation_folder + '/config1.txt',encoding='iso-8859-1') as f:
        lines = f.readlines()
    ss = lines[0]
    rr = re.search('=(.*)\n',ss)
    sim_name = rr.group(1)
    return sim_name
    
def get_mdksim_date(simulation_folder):
    
    # get sim _ info
    with open(simulation_folder + '/config1.txt',encoding='iso-8859-1') as f:
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
    year=int(yy)
    # sim_hora
    ss = lines[8]
    rr = re.search('=(.*)\n',ss)
    hh = int(rr.group(1))
    # sim_minute
    ss = lines[9]
    rr = re.search('=(.*)\n',ss)
    mmin = int(rr.group(1))

    # set the date when the simulation started
    iStartDay = date(year,mm,dd).toordinal()
    iStartHour = hh
    iStartMinute = mmin

    # set time steps of interest (hours by default -- Python counting starts from 0).
    # It may be a single number e.g. [146] or a list of numbers e.g. np.arange(0,15)
    # outputs can be every 6h, for instance, by changing the steps in np.arange to 6,
    # for instance.
    time_line = np.arange(0,sim_length,1)
    real_time = time_line/24. + (iStartHour+1.)/24. + iStartDay
    
    return real_time
    
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def get_parcels_gdf(lats_f, lons_f, surface_volumes, crs):
    
    # create dataframe with the location and volume of surface parcels
    df_gpan = pd.DataFrame({"lat":lats_f,
                "lon":lons_f,
                "vol":surface_volumes})
                
    # create geodataframe from pandas dataframe                 
    # parcels_gdf = gpd.GeoDataFrame(df_gpan, 
    #             geometry=gpd.points_from_xy(df_gpan.lon, df_gpan.lat),
    #             crs=crs) 
    parcels_gdf = gpd.GeoDataFrame(df_gpan, 
                geometry=gpd.points_from_xy(df_gpan.lon, df_gpan.lat),crs=crs).set_crs('EPSG:4326',allow_override=True)
    parcels_gdf = parcels_gdf.drop(columns=['lon', 'lat']) # remove useless variables
    
    return parcels_gdf

def get_observation_df(observation_folder):      
    # load satellite detection shapefile
    observation_df = gpd.read_file(observation_folder)
    # observation_gdf = gpd.GeoDataFrame(observation_df[['geometry']],crs=crs)

    observation_gdf = gpd.GeoDataFrame(observation_df[['geometry']]).set_crs('EPSG:4326',allow_override=True)
    
    return observation_gdf

def get_xp_identifier(sim_identifier, time_index):
        return sim_identifier + '_' + '%02d' % (time_index+1) + 'h_'

def get_grid_resolution(verif_grid_resolution):
    return np.longdouble(verif_grid_resolution)/110.

def get_obs_bounds(observation_gdf):
    return observation_gdf.bounds # first, getting observation bounds

def get_lonlat_minmax(lons_f, lats_f):
    
    #print('CIAO2')
    
    lonmin=np.min(lons_f)
    latmin=np.min(lats_f)
    lonmax=np.max(lons_f)
    latmax=np.max(lats_f)
    
    #print('print:', lonmin, latmin, lonmax, latmax)

    return lonmin, latmin, lonmax, latmax

def get_grid_centroid(output_frame, crs):
    
    output_frame.set_crs('EPSG:4326',allow_override=True)
    grid_centroid = output_frame['geometry'].to_crs(crs).centroid.to_crs(output_frame.crs)
    
    return grid_centroid

def get_event_set(grid_centroid):
    return np.zeros((len(grid_centroid),6))*np.nan

def get_cell_total_volume(parcels_gdf, output_frame):
    
    # group your parcels into visualization grid
    gridded_parcels = gpd.sjoin(parcels_gdf,output_frame, how='left', op='within').set_crs('EPSG:4326',allow_override=True)
    # aggregate volumes to grid cells with dissolve 
    gridded_parcels['cell_total_volume']=1
    
    return gridded_parcels.dissolve(by="index_right", aggfunc="count")

def get_model_spill(output_frame, cell_total_volume):
    output_frame.loc[cell_total_volume.index, 'cell_total_volume'] = cell_total_volume.cell_total_volume.values
    
    return output_frame[output_frame['cell_total_volume'] > 0]

def get_gridded_observation(output_frame, observation_gdf):
        return gpd.sjoin(left_df=output_frame, right_df=observation_gdf[['geometry']], how='inner').set_crs('EPSG:4326',allow_override=True)
    
def get_model_and_obs(output_frame, observation_gdf):
        return gpd.sjoin(left_df=output_frame[output_frame['cell_total_volume'] > 0], right_df=observation_gdf[['geometry']], how='inner')
    
# GETTER for FSS computing

def get_X___Y(event_set):
    return np.meshgrid(np.unique(event_set[:,1]),np.unique(event_set[:,2]))

def get_int_mod_obs_int(event_set):
    
    interp_model=NearestNDInterpolator(list(zip(event_set[:,1],event_set[:,2])),event_set[:,3])
    interp_observation=NearestNDInterpolator(list(zip(event_set[:,1],event_set[:,2])),event_set[:,4])
    interp_intersection=NearestNDInterpolator(list(zip(event_set[:,1],event_set[:,2])),event_set[:,5])
    
    return interp_model, interp_observation, interp_intersection

def get_arr_model_obs_union(interp_model, interp_observation, interp_intersection, X, Y):
    
    array_model = interp_model(X, Y)
    array_observation = interp_observation(X, Y)   
    array_intersection = interp_intersection(X, Y)    
    
    array_model[np.isnan(array_model)] = 0
    array_observation[np.isnan(array_observation)] = 0

    array_union = array_model+2*array_observation
    array_union[array_union==0]=np.nan
    
    return array_model, array_observation, array_intersection, array_observation, array_union

def get_fss_output(horizontal_scales):
        return np.zeros((len(horizontal_scales),2))
    
def create_out_file(lonmin, latmin, lonmax, latmax, X, Y, array_union, output_folder, xp_identifier, fss_output, event_set, verif_grid_resolution, time_index):
    plt.figure()
    cMap = c.ListedColormap(['y','b','m'])
    m = Basemap(llcrnrlon=lonmin,llcrnrlat=latmin,\
                urcrnrlon=lonmax,urcrnrlat=latmax,\
                rsphere=(6378137.00,6356752.3142),\
                resolution='i',projection='merc',\
                lat_0=(latmax + latmin)/2.,\
                lon_0=(lonmax + lonmin)/2.,epsg=4326)
    x_map,y_map=m(X,Y)
    m.pcolor(x_map,y_map,array_union,cmap=cMap)
    m.drawcoastlines()
    m.fillcontinents(alpha=1,zorder=3)
    m.drawmeridians(np.arange(lonmin,lonmax, (lonmax-lonmin)/4.), labels=[0,0,0,1], color='white', linewidth=0.03, fontsize = 5) # draw parallels
    m.drawparallels(np.arange(latmin,latmax, (latmax-latmin)/4.), labels=[1,0,0,0], color='white', linewidth=0.03, fontsize = 5) # draw meridians
    plt.savefig(output_folder + '/overlay_' + xp_identifier + '.png',dpi=600,bbox_inches='tight')

    np.savetxt(output_folder + '/fss_' + xp_identifier + '.txt',fss_output)
    np.savetxt(output_folder + '/event_set_' + xp_identifier + '.txt',event_set)
    
    plt.figure()    
    plt.plot(fss_output[:,0]*verif_grid_resolution,fss_output[:,1],'.-')
    plt.savefig(output_folder + '/agg_fss_' + xp_identifier + '.png',dpi=600,bbox_inches='tight')

    plt.close('all')
    
    #print('CREATE DETECTION FOLDER!')
    #print('::: TIME INDEX : ' + str(time_index) + ' :::')
    #print(':::::: ' + str(xp_identifier) + ' ::::::')
    #print('\n')