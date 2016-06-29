from pywps.Process import Status
from pprint import pprint
import json
#
# run from run.wps.here.py (this allows the local cgi to be used...)
# author: ANDREJ
# tests provenance with knmi wps.
#



# target this function with __init__.py from the wps.py process.

#Override status class and method in order to print to stdout directly.
class MyStatus(Status):
    def set(self,string1,p):
        print string1 
status = MyStatus()


from pywps.Process import WPSProcess


### Basic Example applies to most ..
# #
# http://pc150396.knmi.nl:9080/impactportal/WPS?
#   service=WPS&request=execute&identifier=wps_andrej&version=1.0.0&storeexecuteresponse=true
# 
class KNMIWpsProcess(WPSProcess):

    def __init__(self):
        WPSProcess.__init__(self, 
                            identifier = 'wps_knmi', # only mandatary attribute = same file name
                            title = 'KNMI test  wps',
                            abstract = 'WPS without lineage',
                            version = "1.0",
                            storeSupported = True,
                            statusSupported = True,
                            grassLocation =False)

        self.pipein = self.addComplexInput(identifier="pipein",
                        title="Input file",
                        abstract="Input vector file, usually in GML format",
                        formats = [
                                    # gml
                                    #{mimeType: 'text/xml',
                                    #encoding:'utf-8',
                                    #schema:'http://schemas.opengis.net/gml/3.2.1/gml.xsd'},
                                    
                                    # json
                                    {
                                     'mimeType': 'text/plain',
                                     'encoding': 'iso-8859-2',
                                     'schema': None
                                    }
                                    #{
                                    #'mimeType': 'application/json'
                                    #}

                                    #,
                                    # kml
                                    #{mimeType: 'text/xml',
                                    #encoding: 'windows-1250',
                                    #schema: 'http://schemas.opengis.net/kml/2.2.0/ogckml22.xsd'}
                                    ],
                        # we need at least TWO input files, maximal 5
                        minOccurs= 1,
                        maxOccurs= 100
                        #,
                        #metadata: {'foo':'bar','spam':'eggs'}
                    )


    def execute(self):
        pprint(self.pipein.getValue())

        self.status.set("ready",100);



#'''
knmiprocess = KNMIWpsProcess()

json_data=open('input.json').read()
data = json.loads(json_data)

pprint(json_data)

knmiprocess.pipein.setValue( data )
#knmiprocess.inputs['weight'].setValue( {'value' : 'normminmax' } )
#knmiprocess.inputs['variable'].setValue( {'value' : 'vDTR' } )
#knmiprocess.inputs['tags'].setValue( {'value' : 'ale' } )

knmiprocess.status = status
knmiprocess.execute()



