# owslib example
from owslib.wms import WebMapService
from PIL import Image

# read WMS link using owslib : Andrej Mihajlovski, at KNMI
# using: 

def getwms(service_url):

	# add default
	def_service_url = 'http://climate4impact.eu/impactportal/ImpactService?source=http://opendap.knmi.nl/knmi/thredds/dodsC/CLIPC/tier1_indicators/icclim_cerfacs/CDD/MPI-M-MPI-ESM-LR_rcp45_r1i1p1_SMHI-RCA4_v1/CDD_DEC_MPI-M-MPI-ESM-LR_rcp45_r1i1p1_SMHI-RCA4_v1_EUR-11_2006-2100.nc'
	if service_url is None:
		service_url = def_service_url


	# create wms
	wms = WebMapService( service_url , version='1.1.1')

	print "wms url: " , service_url
	print "type: "    , wms.identification.type
	print "version: " , wms.identification.version 
	print "title: "   , wms.identification.title
	print "abstract: ", wms.identification.abstract


	print "contents: " , list(wms.contents)

	print ""
	layer = list(wms.contents)[0]
	#print layer
	print "title: "   , wms[layer].title
	bb1 = wms[layer].boundingBox
	bb2 = wms[layer].boundingBoxWGS84
	print "bbox:      "   , bb1
	print "bboxWGS84: "   , bb2
	bb = bb1

	print "crsOptions: "   , wms[layer].crsOptions
	print "styles: "   
	for s in wms[layer].styles:
		print "  " , s

	print ""
	print "operations:" , [op.name for op in wms.operations]

	#print wms.getOperationByName('GetMap').methods
	#print wms.getOperationByName('GetMap').formatOptions


	bl = list(wms.contents)[1]
	ol = list(wms.contents)[3]

	
	print "wms.getmap"
	img = wms.getmap( layers=[bl,layer,ol] ,
		#styles=[style],
		srs='EPSG:3411', 
		bbox=(bb[0], bb[1], bb[2], bb[3]),
		size=(500, 500), 
		format='image/png',
		transparent = True)

	#print "url of image: " , img.geturl()

	img_name = 'image_wms_vdd.png'
	print "open img file: " , img_name

	out = open( img_name, 'wb')
	out.write(img.read())
	out.close()
	print "end"

	f = Image.open( img_name ).show()

	return wms

