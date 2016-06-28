# python
# knmi clipc
# author: andrej
# clipc@knmi.nl
#
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import netCDF4
import mpl_toolkits.basemap.pyproj as pyproj
import clipc_combine_process

# http://bhw319.knmi.nl/~mihajlov/wps.cgi?service=wps&request=execute&version=1.0.0&identifier=dummyprocess_clipc
#	&storeExecuteResponse=true
#	&status=true
#	&datainputs=[input1=200]

def visualise( url_1, url_2, url_combo ):

	visualiseUrl( url_1,'131')

	visualiseUrl( url_2,'132')

	visualiseUrl( url_combo,'133')

	plt.show()

def visualiseUrl( url , fig1 ):

	nc = netCDF4.Dataset(url,'r')

	title = clipc_combine_process.getTitleNC(nc)

	fig = plt.figure(1)

	lats = nc.variables['lat'][:]  # extract/copy the data
	lons = nc.variables['lon'][:]

	lat_0 = lats.mean()
	lon_0 = lons.mean()

	ax = fig.add_subplot(fig1)
	basemap = Basemap(resolution='l',projection='ortho', lat_0=lat_0,lon_0=lon_0) #lat_ts=40,

	if len(lons.shape) == 1:
		# 2D Array no time dimmension
		data = nc.variables[title][:][:]
		xi, yi = basemap(*np.meshgrid(lons, lats))
	elif len(lons.shape) == 2:
		# 3D Array time dimmension
		data = nc.variables[title][0][:][:]	 
		xi, yi = basemap(lons, lats)
	else:
		print "DATA SIZE NOT HANDLED"
		data = None

	# Plot Data
	cs = basemap.pcolormesh(xi,yi,np.squeeze(data))

	# Add Coastlines, States, and Country Boundaries
	basemap.drawcoastlines()
	basemap.drawcountries()
	basemap.colorbar()



def get(fig_no, title,url):
	nc = netCDF4.Dataset(url,'r')

	# netCDF url
	print url
	
	# print variables
	for k in nc.variables.keys():
		print k," ",nc.variables[k]

	print nc.variables[title].grid_mapping


	lats = nc.variables['lat'][:]  # extract/copy the data
	lons = nc.variables['lon'][:]
	rlats = nc.variables['rlat'][:]
	rlons = nc.variables['rlon'][:]
	time = nc.variables['time'][1]
	data = nc.variables[title][1][:][:] 

	rotated_pole = nc.variables['rotated_pole']
	pole_lon = rotated_pole.grid_north_pole_latitude
	pole_lat = rotated_pole.grid_north_pole_longitude

	print "time: " , netCDF4.num2date(time,nc.variables['time'].units)
	print rotated_pole
	# print rotated_pole[0]
	print "grid_north_pole_latitude:  " , pole_lat
	print "grid_north_pole_longitude: " , pole_lon

	fig = plt.figure(fig_no)



	ax = fig.add_subplot(121)

	#isn2004=pyproj.Proj("+proj=lcc +lat_1=64.25 +lat_2=65.75 +lat_0=65 +lon_0=-19 +x_0=1700000 +y_0=300000 +no_defs +a=6378137 +rf=298.257222101 +to_meter=1")

	mp = data.shape[1]/2
	lat_0 = lats[mp][mp]
	lon_0 = lons[mp][mp]

	basemap = Basemap(resolution='l',projection='ortho', lat_ts=40,lat_0=lat_0,lon_0=lon_0)

	# Because our rlon and rlat variables are 1D, 
	# use meshgrid to create 2D arrays 
	# Not necessary if coordinates are already in 2D arrays.	
	#	xlon, ylat = np.meshgrid( rlons , rlats)
	#	xi, yi = basemap(xlon, ylat)

	xi, yi = basemap(lons, lats)

	# Plot Data
	#cs = basemap.imshow(img)
	cs = basemap.pcolormesh(xi,yi,np.squeeze(data))
	#cs = basemap.contourf(xi,yi,np.squeeze(data),50)
	#...cs = basemap.hexbin(xi,yi) # https://basemaptutorial.readthedocs.org/en/latest/plotting_data.html#hexbin

	# Add Grid Lines
	#basemap.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
	#basemap.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

	# Add Coastlines, States, and Country Boundaries
	basemap.drawcoastlines()
	basemap.drawcountries()
	basemap.colorbar()


	ax = fig.add_subplot(122)

	basemap= Basemap(projection='rotpole',
				lat_0=lat_0,
				lon_0=lon_0,
				o_lon_p=pole_lon,
				o_lat_p=pole_lat,
       			llcrnrlat = lats[0,0], 
       			urcrnrlat = lats[-1,-1],
       			llcrnrlon = lons[0,0], 
       			urcrnrlon = lons[-1,-1],
       			resolution='l')

	xi, yi = basemap(lons, lats)

	# Plot Data
	cs = basemap.pcolormesh(xi,yi,np.squeeze(data))

	# Add Grid Lines
	basemap.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
	basemap.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

	# Add Coastlines, States, and Country Boundaries
	basemap.drawcoastlines()
	basemap.drawcountries()

	basemap.drawstates()

	plt.title(url)
	#plt.show()

	return nc

def getbasic(title,url):
	nc = netCDF4.Dataset(url,'r')

	# netCDF url
	print url
	
	# print variables
	for k in nc.variables.keys():
		print k," ",nc.variables[k]

	print nc.variables[title].grid_mapping


	lats = nc.variables['lat'][:]  # extract/copy the data
	lons = nc.variables['lon'][:]
	rlats = nc.variables['rlat'][:]
	rlons = nc.variables['rlon'][:]
	time = nc.variables['time'][1]
	data = nc.variables[title][1][:][:] 

	rotated_pole = nc.variables['rotated_pole']
	pole_lon = rotated_pole.grid_north_pole_latitude
	pole_lat = rotated_pole.grid_north_pole_longitude

	print "time: " , netCDF4.num2date(time,nc.variables['time'].units)
	print rotated_pole
	# print rotated_pole[0]
	print "grid_north_pole_latitude:  " , pole_lat
	print "grid_north_pole_longitude: " , pole_lon

	fig = plt.figure()

	ax = fig.add_subplot()#(121)
	#isn2004=pyproj.Proj("+proj=lcc +lat_1=64.25 +lat_2=65.75 +lat_0=65 +lon_0=-19 +x_0=1700000 +y_0=300000 +no_defs +a=6378137 +rf=298.257222101 +to_meter=1")
	# maarten has implementation in adaguc...
	#isn2004=pyproj.Proj("+proj=lcc +lat_1=64.25 +lat_2=65.75 +lat_0=65 +lon_0=-19 +x_0=1700000 +y_0=300000 +no_defs +a=6378137 +rf=298.257222101 +to_meter=1")
	#isn2004(pole_lo)

	mp = data.shape[1]/2
	lat_0 = lats[mp][mp]
	lon_0 = lons[mp][mp]

	basemap = Basemap(resolution='l',projection='ortho', lat_ts=40,lat_0=lat_0,lon_0=lon_0)

	# Because our rlon and rlat variables are 1D, 
	# use meshgrid to create 2D arrays 
	# Not necessary if coordinates are already in 2D arrays.	
	#	xlon, ylat = np.meshgrid( rlons , rlats)
	#	xi, yi = basemap(xlon, ylat)

	xi, yi = basemap(lons, lats)

	# Plot Data
	#cs = basemap.imshow(img)
	cs = basemap.pcolormesh(xi,yi,np.squeeze(data))
	#cs = basemap.contourf(xi,yi,np.squeeze(data),50)
	#...cs = basemap.hexbin(xi,yi) # https://basemaptutorial.readthedocs.org/en/latest/plotting_data.html#hexbin

	# Add Grid Lines
	basemap.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
	basemap.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

	# Add Coastlines, States, and Country Boundaries
	basemap.drawcoastlines()
	basemap.drawcountries()
	basemap.colorbar()

	#plt.figure()

	ax = fig.add_subplot(122)

	basemap= Basemap(projection='rotpole',
				lat_0=lat_0,
				lon_0=lon_0,
				o_lon_p=pole_lon,
				o_lat_p=pole_lat,
       			llcrnrlat = lats[0,0], 
       			urcrnrlat = lats[-1,-1],
       			llcrnrlon = lons[0,0], 
       			urcrnrlon = lons[-1,-1],
       			resolution='l')

	xi, yi = basemap(lons, lats)

	# Plot Data
	cs = basemap.pcolormesh(xi,yi,np.squeeze(data))

	# Add Grid Lines
	basemap.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
	basemap.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

	# Add Coastlines, States, and Country Boundaries
	basemap.drawcoastlines()
	basemap.drawcountries()

	basemap.drawstates()

	plt.show() #figure()

	return nc