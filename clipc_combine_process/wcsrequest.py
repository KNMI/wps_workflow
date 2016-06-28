# python
# clipc combine process
# combine two netCDFs
# knmi team
# clipc@knmi.nl
# author: andrej
#
import netCDF4
import urllib2
import urllib
import xml.etree.ElementTree as et
import crsbbox

#import random

def defaultCallback(message,percentage):
  print "defaultCallback: "+message

def getWCS( wcs_url1, 
      bbox, 
      time, 
      output_file='wcs_output.nc',
      width=300,
      height=300,
      callback=defaultCallback,
      certfile=None):

  # Describe Coverage: used to id layer,
  # data also available in getCapabilities...
  values_describe = [  ('SERVICE' , 'WCS'), ('REQUEST' , 'DescribeCoverage') ]
  data_describe = urllib.urlencode(values_describe)
  request_describe =  wcs_url1 + "&" + str(data_describe)

  print request_describe

  #print request_describe
  if certfile != None:
    opener = urllib.URLopener(key_file =certfile, cert_file = certfile)
    response = opener.open(request_describe)
  else:
    response = urllib2.urlopen( request_describe )
          
  xmlresponse = response.read()
  tree = et.fromstring(xmlresponse)

  for i in tree.iter():
    if 'name' in str(i):
      title = i.text
      break

  # desribe coordinate ref system    
  crs = 'EPSG:4326'
    #'EPSG:3575'
  #'EPSG:28992' 
  #'EPSG:4326'

  # use standard bbox...
  # TODO if bbox provided check and use...
  if bbox is None:
    bbox = crsbbox.getBBOX(crs)

  # get coverage based on layer described in Describe coverage.
  values = [  ('SERVICE' , 'WCS'),
        ('REQUEST' , 'GetCoverage') ,
        ('COVERAGE', title),
        ('CRS'     , crs ),  
        ('FORMAT'  , 'NetCDF') ,
        ('BBOX'    , bbox ),
        ('WIDTH' , width ),
        ('HEIGHT', height ) 
        ]

  if time is not None:
    values.append( ('TIME', time))    

  data = urllib.urlencode(values)

  request =  wcs_url1 + "&" + str(data)

  defaultCallback(request,4)
  if certfile != None:
    opener = urllib.URLopener(key_file =certfile, cert_file = certfile)
    response = opener.open(request)
  else:
    response = urllib2.urlopen( request )

  output = output_file
  out = open( output , 'wb')
  out.write( bytes(response.read() ) )
  out.close()

  return output_file