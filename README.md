# Mitigating Gender Bias by Counterfactual Data Augmentation

## Citation
This code is for the paper
_Counterfactual data augmentation for mitigating gender stereotypes in languages with rich morphology_
featured in ACL 2019.
The paper can be found [here](https://www.aclweb.org/anthology/P19-1161v2.pdf).
Please cite as:
```bibtex
@inproceedings{zmigrod-etal-2019-counterfactual,
    title = "Counterfactual Data Augmentation for Mitigating Gender Stereotypes in Languages with Rich Morphology",
    author = "Zmigrod, Ran  and
      Mielke, Sabrina J.  and
      Wallach, Hanna  and
      Cotterell, Ryan",
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P19-1161",
    doi = "10.18653/v1/P19-1161",
    pages = "1651--1661"
}
```
## Requirements
* Python version >= 3.6
* Pytorch version = 1.2
* Installation instructions:
conda create --name py36-pytorch1.2 python=3.6 \
conda activate py36-pytorch1.2 \
conda uninstall pytorch \
conda install pytorch==1.2.0 torchvision==0.4.0 cudatoolkit=10.0 -c pytorch

Additional dependencies:
    - numpy
    - scikit-learn
    - pip:
        - tqdm
        - filelock
        - pyconll



## Running and Training
We provide pre-trained models for French and Spanish in the `models` folder.
All input files should be in conllu format.

In order to run a pretrained model, use the command.
```bash
python src/main.py --in_files [input conllu files] --psi [path to psi .pt file] --reinflect [path to reinflectino model] --animate_list [path to animacy list] --inc_input --get_ids  --out_file [path to output_file] --part 100
```
In order to train the model, use the following command
```bash
python src/neural-mrf.py --data [path to training data] --out_dir [path to output directory]

#Additional parameters that currentll don't work and are hardcoded in the code.
#--log_alpha 1 --lr 0.005 --wd 0.0001
```
You can train the reinflection using `reinflection_train.py`.
This has been lightly modified by the [Sigmorphon cross-lingual-baseline](https://github.com/sigmorphon/crosslingual-inflection-baseline).
If you use this code please cite the shared task appropriately.


## vishal local dev box setup

Inference:
```
conda activate py36-pytorch1.2
python biasCDA/src/main.py --in_files treebanks/UD_Spanish-GSD/es_gsd-ud-test.conllu --psi biasCDA/models/psi/spanish.pt --reinflect biasCDA/models/reinflection/spanish --animate_list biasCDA/animacy/spanish.tsv --inc_input --get_ids  --out_file treebanks/UD_Spanish-GSD/es_gsd-ud-test.conllu.out.txt --part 100
#get text from conllu file
python biasCDA/src/conll_to_text.py --in_files treebanks/UD_Spanish-GSD/es_gsd-ud-test.conllu --out_dir treebanks/UD_Spanish-GSD
```

Training:
```
python biasCDA/src/neural-mrf.py --data /home/nlpsrv/biasCDA/treebanks/UD_Spanish-GSD-master/es_gsd-ud --out_dir /home/nlpsrv/biasCDA/treebanks &
```


## Udify standalone

I ended up using udify but turns out it needs input in conllu format. The good thing is it is the SOTA and gives us gender tags that we need. Hence, i am currently doing this in the steps:

* Use stanza + spacy-conll to transform the text to a conllu format
* Then use predict code for udify directly to get all the required tags
* We then can feed this for CDA
* Thus, ideally, we should use udify with spacy but that's TBD.

Installation
* pip install spacy_conll
* pip install spacy-stanza
* Python code:
```
python
# https://stanfordnlp.github.io/stanza/installation_usage.html
# https://github.com/stephantul/spacy_conll
# using pip to install packages in coda env: https://stackoverflow.com/questions/41060382/using-pip-to-install-packages-to-anaconda-environment
import stanza
stanza.download('en')
from spacy_conll import init_parser
# Initialise English parser, already including the ConllFormatter as a pipeline component.
# Indicate that we want to get the CoNLL headers in the string output.
# `use_gpu` and `verbose` are specific to stanza (and stanfordnlp). These keywords arguments
# are passed onto their Pipeline() initialisation
nlp = init_parser("stanza", "en", parser_opts={"use_gpu": True, "verbose": False}, include_headers=True)
# Parse a given string
doc = nlp("The doctor is going home as she is tired.")

# Get the CoNLL representation of the whole document, including headers
conll = doc._.conll_str
print(conll)

f = open("stanza-conllu-input.txt", "a")
f.write(conll)
f.close()

CTRL-Z
cd udify/udify/
python predict.py logs/udify-model.tar.gz /home/nlpsrv/biasCDA/biasCDA/e2e-scripts/es-input.txt.conllu-input.txt logs/pred-stanza-es-mini.conllu

 python predict.py logs/udify-model.tar.gz ../../stanza-conllu-input-raw.txt logs/pred-non-stanza-raw.conllu --raw_text
```


Reference: \
https://github.com/hyperparticle/udify

```
conda create --name py36-udify-direct python=3.6

conda activate py36-udify-direct
python predict.py logs/udify-model.tar.gz data/ud-treebanks-v2.3/UD_English-EWT/en_ewt-ud-dev.conllu logs/pred.conllu --eval_file logs/pred.json

python predict.py logs/udify-model.tar.gz data/ud-treebanks-v2.3/UD_English-EWT/en_ewt-ud-dev.txt logs/pred.conllu --eval_file logs/pred.json
```

https://course.spacy.io/en/ \
https://spacy.io/usage/spacy-101#annotations-pos-deps \
https://spacy.io/api/doc

Another conllu generator #1\
https://spacy.io/universe/project/spacy-conll \
https://pypi.org/project/spacy-udpipe/

Another conllu generator #2\
https://github.com/explosion/spacy-stanza

https://github.com/stephantul/spacy_conll \
https://spacy.io/usage/visualizers




## Udify with spacy
TODO: Not working, for reference only \
TODO: I could not get it to work!!!

https://github.com/PKSHATechnology-Research/camphr \
https://camphr.readthedocs.io/en/latest/notes/udify.html

```
conda create --name py36-udify python=3.6
wget https://github.com/PKSHATechnology-Research/camphr_models/releases/download/0.7.0/en_udify-0.7.tar.gz
pip install en_udify-0.7.tar.gz
conda install -c conda-forge spacy=2.2
```

Try it out:
```
python
import spacy
nlp = spacy.load("en_udify")
doc = nlp("The doctor is going home since she is tired")
from spacy import displacy
displacy.serve(doc, style="dep")

Using the 'dep' visualizer
Serving on http://<ip-addrress>:5000 ...
```
