# python
# KNMI clipc
# author: andrej
# clipc@knmi.nl

import numpy as np
import netCDF4

def defaultCallback(message,percentage):
  print "defaultCallback: "+mesysage

#import mpl_toolkits.basemap.pyproj as pyproj

# http://bhw319.knmi.nl/~mihajlov/wps.cgi?service=wps&request=execute&version=1.0.0&identifier=dummyprocess_clipc&storeExecuteResponse=true&status=true&datainputs=[input1=200]

# copy existing netcdf to new file with name
#
def copyNetCDF(name, nc_fid , des ):
  w_nc_fid = netCDF4.Dataset(name, 'w', format='NETCDF4')

  w_nc_fid.description = des

  for var_name, dimension in nc_fid.dimensions.iteritems():
    w_nc_fid.createDimension(var_name, len(dimension) if not dimension.isunlimited() else None)

  for var_name, ncvar in nc_fid.variables.iteritems():

    outVar = w_nc_fid.createVariable(var_name, ncvar.datatype, ncvar.dimensions )
  
    ad = dict((k , ncvar.getncattr(k) ) for k in ncvar.ncattrs() )

    outVar.setncatts(  ad  )

    outVar[:] = ncvar[:]

  global_vars = dict((k , nc_fid.getncattr(k) ) for k in nc_fid.ncattrs() )
  
  for k in sorted(global_vars.keys()):
    w_nc_fid.setncattr(  k , global_vars[k]  )

  return w_nc_fid
# end copy

# combine two netcdfs based on operator after normalising by max value of each.
#
def combineNetCDFs(name, nc1 , var1 , nc2 , var2 , des , operator_func,callback=defaultCallback):
  
  # result file is a copy of first imput, uncluding metadata
  nc_combo = copyNetCDF( name , nc1 , des )

  v2 = nc2.variables[var2][:]
  v1 = nc1.variables[var1][:]

  m1 = v1.max()
  m2 = v2.max()

  c = nc_combo.variables[var1][:]

	# sepricated
	# operator used previously, changed to np for speed.
	# normalise and
	# combine
	# for k in range(v1.shape[0]):
	# 	for i in range(v1.shape[1]):
	# 		for j in range(v1.shape[2]):
	# 			c[k][i][j] = operator_func(v1[k][i][j]/m1 , v2[k][i][j]/m2)
	#end matrix		

	# np op functions used here
  callback("start combine",50)
  c = operator_func( np.divide(v1,m1) , np.divide(v2,m2) )
  callback("end combine",75)

  nc_combo.variables[var1][:] = c

  return nc_combo
# end combine

