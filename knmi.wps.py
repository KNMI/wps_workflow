from pywps.Process import Status, WPSProcess
from pprint import pprint
import json
import os
from dispel4py import provenance

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


        self.pipein = self.addLiteralInput( identifier = "pipein" ,
                                            title      = "Input json file" ,
                                            type       = type("string"),
                                            default    = None 
                                        ) 




    '''
        self.pipein = self.addComplexInput( identifier="pipein",
                                            title="Input json file",
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
                                                        },
                                                        {
                                                        'mimeType': 'application/json'
                                                        }

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
    '''

    def execute(self):
        self.status.set("start",0);
        
        jsondata = json.loads(self.pipein.getValue())

        print( jsondata )



        with open( '/tmp/input.json' ,'wr') as outf:
            #json_str = json.dump( jsondata ,outf)
            #outf.write("\n")
            outf.write(json.dumps(jsondata))
            outf.write("\n")
            outf.flush()
            outf.close()


        # 
        # python -m dispel4py.new.processor multi clipc -n 12 -f jsondata
        stdoutdata, stderrdata = provenance.commandChain([["{}".format(
                                                    "python -m dispel4py.new.processor multi clipc -n 12 -f /tmp/input.json"
                                                    )]],os.environ.copy())

        print stdoutdata

        print stderrdata

        self.status.set("done",100);



#'''
knmiprocess = KNMIWpsProcess()

json_data=open('input.json').read()
#data = json.loads(json_data)

#print json_data

knmiprocess.pipein.setValue( {'value': json_data } )

knmiprocess.status = status
knmiprocess.execute()



