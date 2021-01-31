import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

#source activate py36-udify-direct
#python biasCDA/biasCDA/e2e-scripts/step1-stanza-conllu.py
##subprocess.call(["source activate", "py36-udify-direct"])
##install('stanza')

import stanza
#stanza.download('en')
#install('spacy_conll')
from spacy_conll import init_parser
# Initialise English parser, already including the ConllFormatter as a pipeline component.
# Indicate that we want to get the CoNLL headers in the string output.
# `use_gpu` and `verbose` are specific to stanza (and stanfordnlp). These keywords arguments
# are passed onto their Pipeline() initialisation
nlp = init_parser("stanza", "en", parser_opts={"use_gpu": True, "verbose": False}, include_headers=True)


def getCampherConlluStr(line):
            """
            conda activate CampherNlp
            wget https://github.com/PKSHATechnology-Research/camphr_models/releases/download/0.7.0/en_udify-0.7.tar.gz
            pip install en_udify-0.7.tar.gz
            pip install en_udify-0.7.tar.gz -b /home/nlpsrv/tempdir
            pip install camphr-allennlp
            pip install spacy_conll

            python
import spacy
from spacy_conll import init_parser
nlp = spacy.load("en_udify")
doc = nlp("The doctor is going home as she is tired.")
print(doc._.conll_str)
            """



def getConlluStr(line):
    #print("Line{}: {}".format(count, line.strip())) 
    myStr = line.strip()
    try:
        if not "".__eq__(myStr):

            # Parse a given string
            doc = nlp(myStr)

            # Get the CoNLL representation of the whole document, including headers
            return doc._.conll_str
            # print(conll)
            # outputFile.write(conll)
    except Exception as ex:
        print('*' + myStr + '*')
        print(ex)
        raise ex
    return ''

def getConlluStr2(line):
    return 'getConlluStr ' + str(line)

import multiprocessing
from joblib import Parallel, delayed

num_cores = multiprocessing.cpu_count() - 1

language = 'en'
filePath = '/home/nlpsrv/biasCDA/training-data/en_fr/wmt15/news-commentary-v10.fr-en.en'

print(num_cores)
from tqdm import tqdm

# from math import sqrt
# import numpy as np
# myIntList = np.arange(11, 17, 0.5).tolist()
# print(type(myIntList))
# outputLines2 = Parallel(n_jobs=num_cores)(delayed(getConlluStr2)(myIntList[i]) for i in tqdm(range(len(myIntList))))
# print(outputLines2)


# Using readlines() 
filePtr = open(filePath, 'r')
Lines = filePtr.readlines()
print(type(Lines))

#inputs = Lines
inputs = Lines[1:5]
inputsLength = len(inputs)
outputLines = []
##outputLines = Parallel(n_jobs=9)(delayed(getConlluStr)(inputs[i]) for i in tqdm(range(inputsLength)))
for inputLine in inputs:
    outputLines.append(getConlluStr(inputLine))

outputFile = open(filePath + ".conllu-input.txt", "w")
outputFile.writelines("%s\n" % conllu for conllu in outputLines)
outputFile.close()

print(f'done processing. output filename={outputFile}')

# When running with max parallelism

# /home/nlpsrv/.local/lib/python3.6/site-packages/torch/nn/modules/rnn.py:585: UserWarning: RNN module weights are not part of single contiguous chunk of memory. This means they need to be compacted at every call, possibly greatly increasing memory usage. To compact weights again call flatten_parameters(). (Triggered internally at  /pytorch/aten/src/ATen/native/cudnn/RNN.cpp:775.)
#   self.num_layers, self.dropout, self.training, self.bidirectional)
# joblib.externals.loky.process_executor._RemoteTraceback:
# """
# Traceback (most recent call last):
#   File "/home/nlpsrv/anaconda3/envs/py36-udify-direct/lib/python3.6/site-packages/joblib/externals/loky/process_executor.py", line 404, in _process_worker
#     call_item = call_queue.get(block=True, timeout=timeout)
#   File "/home/nlpsrv/anaconda3/envs/py36-udify-direct/lib/python3.6/multiprocessing/queues.py", line 113, in get
#     return _ForkingPickler.loads(res)
#   File "/home/nlpsrv/.local/lib/python3.6/site-packages/torch/storage.py", line 141, in _load_from_bytes
#     return torch.load(io.BytesIO(b))
#   File "/home/nlpsrv/.local/lib/python3.6/site-packages/torch/serialization.py", line 595, in load
#     return _legacy_load(opened_file, map_location, pickle_module, **pickle_load_args)
#   File "/home/nlpsrv/.local/lib/python3.6/site-packages/torch/serialization.py", line 774, in _legacy_load
#     result = unpickler.load()
#   File "/home/nlpsrv/.local/lib/python3.6/site-packages/torch/serialization.py", line 730, in persistent_load
#     deserialized_objects[root_key] = restore_location(obj, location)
#   File "/home/nlpsrv/.local/lib/python3.6/site-packages/torch/serialization.py", line 175, in default_restore_location
#     result = fn(storage, location)
#   File "/home/nlpsrv/.local/lib/python3.6/site-packages/torch/serialization.py", line 155, in _cuda_deserialize
#     return storage_type(obj.size())
#   File "/home/nlpsrv/.local/lib/python3.6/site-packages/torch/cuda/__init__.py", line 462, in _lazy_new
#     return super(_CudaBase, cls).__new__(cls, *args, **kwargs)
# RuntimeError: CUDA error: out of memory
# """

# The above exception was the direct cause of the following exception:

# Traceback (most recent call last):
#   File "biasCDA/e2e-scripts/step1-stanza-conllu.py", line 73, in <module>
#     outputLines = Parallel(n_jobs=num_cores)(delayed(getConlluStr)(inputs[i]) for i in tqdm(range(inputsLength)))
#   File "/home/nlpsrv/anaconda3/envs/py36-udify-direct/lib/python3.6/site-packages/joblib/parallel.py", line 1061, in __call__
#     self.retrieve()
#   File "/home/nlpsrv/anaconda3/envs/py36-udify-direct/lib/python3.6/site-packages/joblib/parallel.py", line 940, in retrieve
#     self._output.extend(job.get(timeout=self.timeout))
#   File "/home/nlpsrv/anaconda3/envs/py36-udify-direct/lib/python3.6/site-packages/joblib/_parallel_backends.py", line 542, in wrap_future_result
#     return future.result(timeout=timeout)
#   File "/home/nlpsrv/anaconda3/envs/py36-udify-direct/lib/python3.6/concurrent/futures/_base.py", line 432, in result
#     return self.__get_result()
#   File "/home/nlpsrv/anaconda3/envs/py36-udify-direct/lib/python3.6/concurrent/futures/_base.py", line 384, in __get_result
#     raise self._exception
# joblib.externals.loky.process_executor.BrokenProcessPool: A task has failed to un-serialize. Please ensure that the arguments of the function are all picklable.


################ download file ############################
# '''
# Python 3.6.12 |Anaconda, Inc.| (default, Sep  8 2020, 23:10:56)
# [GCC 7.3.0] on linux
# Type "help", "copyright", "credits" or "license" for more information.
# >>> import stanza
# >>> stanza.download('en')
# Downloading https://raw.githubusercontent.com/stanfordnlp/stanza-resources/master/resources_1.1.0.json: 122kB [00:00, 29.8MB/s]
# 2021-01-12 14:10:41 INFO: Downloading default packages for language: en (English)...
# 2021-01-12 14:10:42 INFO: File exists: /home/nlpsrv/stanza_resources/en/default.zip.
# '''