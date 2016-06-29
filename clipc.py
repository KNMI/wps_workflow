
# coding: utf-8

# In[ ]:

#get_ipython().magic(u'matplotlib inline')

import time
import random

from dispel4py.workflow_graph import WorkflowGraph 
from dispel4py.provenance import *
from dispel4py.base import create_iterative_chain, ConsumerPE, IterativePE, SimpleFunctionPE

from clipc_combine_process import clipc_combine_process_d4p
from clipc_combine_process import serve_netcdf_d4p

import matplotlib.pyplot as plt
import traceback

from pprint import pprint

# project: CLIP_C
# authors: Alessandro and Andrej
# CLIPC combine function using dispel4py and running over jupyter
# [mihajlov@pc150396 ~]$ .local/bin/jupyter-notebook 



#print __dir__

print "/usr/people/mihajlov/python/clipc/clipccombine clean"
print "CLIPC dispel4py running"

class Collector(GenericPE):
        
    def __init__(self):
        #IterativePE.__init__(self)
        GenericPE.__init__(self)
        self._add_input('input')
        self._add_output('output_R')
        self._add_output('output_W')
        self.counter = 0;
        
    def _process(self,inputs):
        #print inputs
        
        url1 = inputs['input'][0]
        #oper = inputs['input'][2]
        url2 = inputs['input'][1]
     
        index = str(self.counter)
    
        # first  url collected
        #nc1 = clipc_combine_process_d4p.collect(url1)
        #self.write('output_R',(  index , 0 , nc1 ))
        self.write('output_R',(  index , 0 , url1 ))
    
        #second url collected
        #counter = counter + 1
        #nc2 = clipc_combine_process_d4p.collect(url2)
        #self.write('output_R',( index , 1 , nc2 ))
        self.write('output_R',(  index , 1 , url2 ))

        #print nc1
        # output written...
        #nc_out = clipc_combine_process_d4p.write(nc1 , "d4pout/output"+index+".nc" , "dr drej n spinuso rock the data flow.")
        
        #
        #self.log(type(nc_out))  
        
        #
        #self.write('output_W',( index , nc_out))
        self.write('output_W',( index , url1))

        self.counter += 1
              
    
# def readn(data):
#     prov={'format':'Random float', 'metadata':{'value':str(data)}}
#     return {'_d4p_prov':prov,'_d4p_data':data}
        
        
# def multn(data): 
#     prov={'format':'Random float', 'metadata':{'value':data*data}}
#     print data
#     return {'_d4p_prov':prov,'_d4p_data':data*data}

    
def reader(data):
    #nc = clipc_combine_process_d4p.collect(url)
    #print "reader with data:" , str(data)
    #print data[0] ,  data[1]

    print 'reader ',data[0]
    print 'reader ',data[1]
    print 'reader ',data[2]

    nc = clipc_combine_process_d4p.collect(data[2])

    var , norm = clipc_combine_process_d4p.read(nc)

    print 'reader ', type(var)
    print 'reader ', type(norm)

    return ( data[0] , data[1] , var , norm)


##################################

class Match(GenericPE):

    def __init__(self):
        GenericPE.__init__(self)
        # self._add_input('input', grouping=('prov',[0]))
        self._add_input('input', grouping=[0])
        #self._add_input('input2')
        self._accumulator = {}
        self._add_output('output_X')
        
    
    def _process(self,inputs):
        #self.log(  inputs )
        
        #url1,url2 = inputs['input'][0]
        #self._accumulator.append(inputs['input'])
        #self._accumulator.append(inputs['input2'])
        
        inp = inputs['input']
        
        #print inp[0]
        #print inp[1]
        #print len(inp[2])                
        #print inp[3]
        
        #inputs(str(0),element,var,norm)
        self.log( "received counter "+inp[0])
        
        k = str(inp[0])
        if k not in self._accumulator.keys():
            self._accumulator[k] = {} 
        
        self._accumulator[k][inp[1]] = ( inp[2] , inp[3] ) 
        
        # if( len(self._accumulator ) == 2 ):
        if( len(self._accumulator[str(inp[0])].keys() ) == 2 ):
            #combine(self._accumulator)
            
            output = self._accumulator.pop(k)
            
            self.write('output_X', (k , output[0] , output[1]) )

            #print self._accumulator[k].keys()
            
        #nc1 = clipc_combine_process_d4p.collect(url1)
        #self.write('output_R',nc1)
   
        #nc_out = clipc_combine_process_d4p.write(nc1 , "output.nc" , "dr drej n spinuso rock the data flow.")
        #self.write('output_W',nc_out)
        
        #nc2 = clipc_combine_process_d4p.collect(url2)
        #self.write('output_R',nc2)
        
def combine(data,operator):
  
    comb_var = clipc_combine_process_d4p.combine( data[1][0] , data[1][1] , data[2][0] , data[2][1] , operator)
    
    #print "combineindex:",data[0]
    #print "combineindex:",type(data[1][0])
    #print "combineindex:",type(data[2][0])
    #print "combineindex:",type(comb_var)

    return ( data[0] , comb_var)


    
class Writer(GenericPE):

    def __init__(self,op):
        GenericPE.__init__(self)
#        self._add_input('file' , grouping=('prov',[0]))
#        self._add_input('var'  , grouping=('prov',[0]))
        self._add_input('file' , grouping=[0])
        self._add_input('var'  , grouping=[0])
        self._opp = op
        self._accumulator = []
        self._add_output('final')
        
        # index hash
        self.file = {}
        self.var  = {}
        
    def _process(self,inputs):
        self.log(str(inputs))
      
        index = None
        nc_out = None #clipc_combine_process_d4p.write(nc1 , "d4pout/output"+index+".nc" , "dr drej n spinuso rock the data flow.")
        


        try:
            if 'file' in inputs:
                f = inputs['file']
                index = f[0]
                #self.file[index]=f[1]
                #print "writefile:",index
                #print "ANDREJOUT..."
                name = "output"+index+".nc"
                
                self.file[index] = (name , clipc_combine_process_d4p.write( f[1] , name , "dr drej n spinuso rock the data flow."))

                print self.file[index]

            elif 'var' in inputs:
                v = inputs['var']   
                #print "writevar:",type(v[1])
                index = v[0]
                
                self.var[index]=v[1]
                #print "writevar:",type(self.var[index])

            self.log("index writen:"+index)      
        except:
            print "exception for writer input: " , index 
            traceback.print_exc(file=sys.stdout)
            return
        
        print "Writer_process: FUTURE WARNING?"
        print "Writer_process: index",index
        print "Writer_process: ",type(self)
        print "Writer_process: ",type(self.var)
        #print "Writer_process: ",type(self.var[index])    
        print "Writer_process: ",self.file
        #print "Writer_process: ",type(self.file[index])   

        try:
            if (self.var[index] is not None and self.file[index] is not None):
                name , nc   = self.file.pop(index)

                # postprocess var and (nc , name)


                x = clipc_combine_process_d4p.postprocess( self.var.pop(index) , name , nc[0] , nc[1])
                
                #x[0].close()
                "Writer_process: DONE ", name

                meta = {}
                for key, val in nc[0].attrs.items():
                    #print key,'=', val
                    #meta[str(key)] = str(val)
                    meta[str(key)]=str(val)
                print "++++++++++++++++++DATEST"
                print meta

                self.write('final',name, metadata=[meta])
        except KeyError:
             pass
        except:
            #print "andrej exception send " , index , " in file" , self.file.keys() 
            #print "andrej exception send " , index , " in var " , self.var.keys()
            #traceback.print_stack()
            traceback.print_exc(file=sys.stdout)
            
class Visualiser(GenericPE):

    def __init__(self):
        GenericPE.__init__(self)
        self._add_input('input')
        self._add_output('res')
    
    def _process(self,inputs):
        #print inputs
        
        #self._accumulator.append(inputs['input'])
        fig = plt.figure(1)
            
        name =  inputs['input']
        
        print "Visualiser_process ", name
        print "Visualiser_process ", type(name)   

        nc = clipc_combine_process_d4p.collect(name)

        print "Visualiser_process ", nc

        # breaks here have a look...
        #serve_netcdf_d4p.visualise1( fig , nc  )
        
        self.write('res',{})
    
###################################




sc1 = Collector()
sc1.name = 'collector'

sc2 = Match()
sc2.name = 'match'

sc3 = Writer("-")
sc3.name = 'writer'

sc4 = Visualiser()
sc4.name = 'vizu'

read=SimpleFunctionPE(reader)
comb=SimpleFunctionPE(combine,{"operator":"-"})
 

#processes=[readn,multn]
#chain = create_iterative_chain(processes, FunctionPE_class=SimpleFunctionPE)

#Initialise the graph
graph = WorkflowGraph()

#Common way of composing the graph
graph.connect(sc1,'output_R',read,'input')
graph.connect(read,'output', sc2,'input')
graph.connect(sc2,'output_X',comb,'input')
graph.connect(comb,'output',sc3,'var')
graph.connect(sc1,'output_W',sc3,'file')
graph.connect(sc3,'final',sc4,'input')

# Alternatively with pipeline array
#Create pipelines from functions

#graph.connect(sc,'output',chain,'input')



#graph.flatten()


# /usr/people/mihajlov/python/clipc/clipccombine/clipc_combine_process
# file running: combine_netcdf.py
# def combine_two_indecies(url1,url2,operation,output,...):


# this is added as input2.clipc
#Prepare Input
#url1 = 'example/vDTR_JUN_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_SMHI-RCA4_v1_EUR-11_2006-2100.nc'
#url2 = 'example/vDTR_OCT_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_SMHI-RCA4_v1_EUR-11_2006-2100.nc'
#input_data = {"collector": [{"input": [(url1,url2)] },{"input": [(url1,url2)] },{"input": [(url1,url2)] }]}

#Launch in simple process
#simple_process.process_and_return(graph, input_data)


#plt.show()



# In[ ]:

#get_ipython().magic(u'matplotlib inline')

# prov service recorder bulk url...
ProvenanceRecorderToServiceBulk.REPOS_URL='http://verce-portal-dev.scai.fraunhofer.de/j2ep-1.0/prov/workflow/insert'

#unique id for process.
rid='RDWD_'+getUniqueId()

InitiateNewRun(graph,ProvenanceRecorderToServiceBulk,
    provImpClass=ProvenancePE,
    username='andrej',
    runId=rid,
    w3c_prov=False,
    workflowName="test_rdwd",
    workflowId="xx",
    description=sys.argv[1])

#simple_process.process_and_return(graph, input_data)

#plt.show()
#from IPython.display import HTML
#HTML("<iframe src='http://127.0.01:8080/provenance-explorer/html/d3js.jsp?level=PE&runId="+rid+"' width=800 height=800></iframe>")


# In[ ]:

from dispel4py.visualisation import display

display(graph)



