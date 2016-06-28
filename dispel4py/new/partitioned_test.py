import processor
from dispel4py.workflow_graph import WorkflowGraph
from dispel4py.examples.graph_testing.testing_PEs import TestProducer, TestOneInOneOut


prod = TestProducer()
cons1 = TestOneInOneOut()
cons2 = TestOneInOneOut()
    
graph = WorkflowGraph()
graph.connect(prod, 'output', cons1, 'input')
graph.connect(cons1, 'output', cons2, 'input')

graph.partitions= [ [prod], [cons1, cons2]]

ubergraph = processor.create_partitioned(graph)
processes, inputmappings, outputmappings = processor.assign_and_connect(ubergraph, 2)
print processes
print inputmappings
print outputmappings

import multi_process

inputs= { prod : [{}] }
mapped_inputs=processor.map_inputs_to_partitions(ubergraph, inputs)
print 'MAPPED INPUTS: %s' % mapped_inputs
multi_process.process(ubergraph, 2, inputs = mapped_inputs)