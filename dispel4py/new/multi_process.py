# Copyright (c) The University of Edinburgh 2014
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
Enactment of dispel4py graphs using multiprocessing.

From the commandline, run the following command::

    dispel4py multi <module> -n num_processes [-h] [-a attribute]\
                    [-f inputfile] [-i iterations]

with parameters

:module:    module that creates a Dispel4Py graph
:-n num:    number of processes (required)
:-a attr:   name of the graph attribute within the module (optional)
:-f file:   file containing input data in JSON format (optional)
:-i iter:   number of iterations to compute (default is 1)
:-h:        print this help page

For example::

    dispel4py multi dispel4py.examples.graph_testing.pipeline_test -i 5 -n 6
    Processing 5 iterations.
    Processes: {'TestProducer0': [5], 'TestOneInOneOut5': [2],\
                'TestOneInOneOut4': [4], 'TestOneInOneOut3': [3],\
                'TestOneInOneOut2': [1], 'TestOneInOneOut1': [0]}
    TestProducer0 (rank 5): Processed 5 iterations.
    TestOneInOneOut1 (rank 0): Processed 5 iterations.
    TestOneInOneOut2 (rank 1): Processed 5 iterations.
    TestOneInOneOut3 (rank 3): Processed 5 iterations.
    TestOneInOneOut4 (rank 4): Processed 5 iterations.
    TestOneInOneOut5 (rank 2): Processed 5 iterations.
'''


import argparse
import copy
import multiprocessing
import traceback
import os
import types
from dispel4py.new.processor \
    import GenericWrapper, simpleLogger, STATUS_ACTIVE, STATUS_TERMINATED, SimpleProcessingPE
from dispel4py.new import processor


def _processWorker(wrapper):
    wrapper.process()


def parse_args(args, namespace):    # pragma: no cover
    parser = argparse.ArgumentParser(
        prog='dispel4py',
        description='Submit a dispel4py graph to multiprocessing.')
    parser.add_argument('-s', '--simple', help='force simple processing',
                        action='store_true')
    parser.add_argument('-n', '--num', metavar='num_processes', required=True,
                        type=int, help='number of processes to run')
    result = parser.parse_args(args, namespace)
    return result


def process(workflow, inputs, args):
    size = args.num
    success = True
    nodes = [node.getContainedObject() for node in workflow.graph.nodes()]
    if not args.simple:
        try:
            result = processor.assign_and_connect(workflow, size)
            processes, inputmappings, outputmappings = result
        except:
            success = False

    if args.simple or not success:
        ubergraph = processor.create_partitioned(workflow)
        print('Partitions: %s' % ', '.join(('[%s]' % ', '.join(
            (pe.id for pe in part)) for part in workflow.partitions)))
        for node in ubergraph.graph.nodes():
            wrapperPE = node.getContainedObject()
            pes = [n.getContainedObject().id for
                   n in wrapperPE.workflow.graph.nodes()]
            print('%s contains %s' % (wrapperPE.id, pes))

        try:
            result = processor.assign_and_connect(ubergraph, size)
            if result is None:
                return 'dispel4py.multi_process: ' \
                       'Not enough processes for execution of graph'
            processes, inputmappings, outputmappings = result
            inputs = processor.map_inputs_to_partitions(ubergraph, inputs)
            success = True
            nodes = [node.getContainedObject()
                     for node in ubergraph.graph.nodes()]
        except:
            print(traceback.format_exc())
            return 'dispel4py.multi_process: ' \
                   'Could not create mapping for execution of graph'

    print('Processes: %s' % processes)

    process_pes = {}
    queues = {}
    result_queue = None
    try:
        if args.results:
            result_queue = multiprocessing.Queue()
    except AttributeError:
        pass
    for pe in nodes:
        provided_inputs = processor.get_inputs(pe, inputs)
        for proc in processes[pe.id]:
            cp = copy.deepcopy(pe)
            cp.rank = proc
            cp.log = types.MethodType(simpleLogger, cp)
            wrapper = MultiProcessingWrapper(proc, cp, provided_inputs)
            process_pes[proc] = wrapper
            wrapper.input_queue = multiprocessing.Queue()
            wrapper.input_queue.name = 'Queue_%s_%s' % (cp.id, cp.rank)
            wrapper.result_queue = result_queue
            queues[proc] = wrapper.input_queue
            wrapper.targets = outputmappings[proc]
            wrapper.sources = inputmappings[proc]
    for proc in process_pes:
        wrapper = process_pes[proc]
        wrapper.output_queues = {}
        for target in wrapper.targets.values():
            for inp, comm in target:
                for i in comm.destinations:
                    wrapper.output_queues[i] = queues[i]

    jobs = []
    for wrapper in process_pes.values():
        p = multiprocessing.Process(target=_processWorker, args=(wrapper,))
        jobs.append(p)

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()

    if result_queue:
        result_queue.put(STATUS_TERMINATED)
    return result_queue


class MultiProcessingWrapper(GenericWrapper):

    def __init__(self, rank, pe, provided_inputs=None):
        GenericWrapper.__init__(self, pe)
        self.pe.log = types.MethodType(simpleLogger, pe)
        self.pe.rank = rank
        self.provided_inputs = provided_inputs
        self.terminated = 0

    def _read(self):
        result = super(MultiProcessingWrapper, self)._read()
        if result is not None:
            return result
        # read from input queue
        no_data = True
        while no_data:
            try:
                data, status = self.input_queue.get()
                no_data = False
            except:
                self.pe.log('Failed to read item from queue')
                pass
        while status == STATUS_TERMINATED:
            self.terminated += 1
            if self.terminated >= self._num_sources:
                return data, status
            else:
                try:
                    data, status = self.input_queue.get()
                except:
                    self.pe.log('Failed to read item from queue')
                    pass
        return data, status

    def _write(self, name, data):
        #self.pe.log('MP Writing %s to %s' % (data, name))
        
        try:
            targets = self.targets[name]
        except KeyError:
            # no targets
            if self.result_queue:
                self.result_queue.put((self.pe.id, name, data))
            return
        for (inputName, communication) in targets:
             
            if isinstance(self.pe, SimpleProcessingPE):
                dest = communication.getDestination({inputName: data[0]})
            else:
                dest = communication.getDestination({inputName: data})
                
            output = {inputName: data}
            for i in dest:
                #self.pe.log('Writing out %s' % output)
                try:
                    self.output_queues[i].put((output, STATUS_ACTIVE))
                except:
                    self.pe.log("Failed to write item to output '%s'" % name)

    def _terminate(self):
        for output, targets in self.targets.items():
            for (inputName, communication) in targets:
                for i in communication.destinations:
                    self.output_queues[i].put((None, STATUS_TERMINATED))

import time
def main():    # pragma: no cover
    from dispel4py.new.processor \
        import load_graph_and_inputs, parse_common_args

    args, remaining = parse_common_args()
    args = parse_args(remaining, args)

    graph, inputs = load_graph_and_inputs(args)
    if graph is not None:
        elapsed_time=0
        start_time = time.time()
        process(graph, inputs=input_data, args=args)
        elapsed_time+= time.time() - start_time
    
        errormsg = process(graph, inputs, args)
        if errormsg:
            print(errormsg)
        print ("ELAPSED TIME: "+str(elapsed_time/num))
