# python
# clipc combine process with dispel4py
# combine two netCDFs
# knmi team
# author: andrej / alessandro
# clipc@knmi.nl
#

#import netCDF4
import xarray  
import netCDF4

import random
import wcsrequest
import numpy as np

def defaultCallback(message,percentage):
  print "defaultCallback: "+message


def collect(url):
# print "in collector ",url
  
  # old
  #nc = netCDF4.Dataset(url,'r')
  print "collect --- url: ", url
  # new
  # data set is loaded into memory
  nc = xarray.open_dataset(url)

  # data set is loaded into memory
  # xarray.decode_cf()
  return nc;



def read(nc):
#print "in read ", str(nc)
  print "read --- nc:",type(nc)

  nc.load()

  # NOTE: major change between netcdf4 and xarray is that one uses netattrs and the new lib uses attrs()
  #print "ANDREJ ", dir(nc)
  #print "ANDREJ ", nc
  #print "ANDREJ ", nc.attrs
  #print "ANDREJ ", nc.data_vars

  variableName = getTitleNC(nc)
  #print "TITLE:", variableName



  # v is a np variable object ...
  v = nc.variables[variableName][:]

  print "read v.attrs: ", v.attrs

  #print type(nc.variables[variableName])
  #print type(v)
  # normalisation
  n = v.max()

  return (v, n)



#def write(nc,outName,des):
def write(url,outName,des):
  print "write url    is ",url
  print "write output is ",outName
  print "write des    is ",des

  nc =  collect(url)

  variable = getTitleNC(nc)

  #  print "in preprocess variable name is " , variable

  # copy is removed since nc is in memory.
  #nc_combo = copyNetCDF( outName , nc , des )


  #return (nc_combo, variable)

  return (nc, variable)



def combine(  var1, norm1 , var2 , norm2 , operator_symbol ):
  # ---  
  print "combine --- ", var1
  print "combine --- ", norm1
  print "combine --- ", var2
  print "combine --- ", norm2
  print "combine --- ", operator_symbol

  # print "in preprocess ",var2, " ",norm2
  ops = { "+": np.add , 
          "-": np.subtract, 
          "*": np.multiply, 
          "/": np.divide  }

# nc_combination , combi_name = combine_two_indecies_netcdf(nc1, nc2, operation, output,callback=callback)
# callback("combo time received: "+str(netCDF4.num2date( nc_combination.variables['time'][0] , nc_combination.variables['time'].units ,calendar='standard')),3)
# parse operator symbol to function
  op_char = operator_symbol
  op_func = ops[op_char]

  combo = op_func( np.divide(var1 , norm1) , np.divide( var2 , norm2) )

  return combo


def postprocess( combi_variable , output_file_name , dataset , var_name ): 
  # , operation):
  # 
  print "postprocess ---", type(combi_variable)
  print "postprocess --- dataset :" , dataset
  print "postprocess --- var_name:" , var_name
  dataset.__setitem__( var_name , combi_variable)
  
  dataset.to_netcdf(output_file_name,'w')

  print "postprocess --- write output to ",output_file_name

  dataset.close()

  return "DONE" # nc_combo_tuple[0]

def getTitleNC(nc_fid):
#  print str(nc_fid)
  var = None
  for k, v in nc_fid.data_vars.iteritems():
    print v.attrs
    if "grid_mapping" in v.attrs.keys():  var = k

  return var

### the end
