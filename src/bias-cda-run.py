#python src/main.py --in_files [input conllu files] --psi [path to psi .pt file] --reinflect [path to reinflectino model] --animate_list [path to animacy list] --inc_input --get_ids  --out_file [path to output_file] --part 100
#python biasCDA/src/main.py --in_files treebanks/UD_Spanish-GSD/es_gsd-ud-test.conllu --psi biasCDA/models/psi/spanish.pt --reinflect biasCDA/models/reinflection/spanish --animate_list biasCDA/animacy/spanish.tsv --inc_input --get_ids  --out_file treebanks/UD_Spanish-GSD/es_gsd-ud-test.conllu.out.txt --part 100
#python biasCDA/src/main.py --in_files treebanks/UD_Spanish-GSD/es_gsd-ud-test.conllu --psi biasCDA/models/psi/spanish.pt --reinflect biasCDA/models/reinflection/spanish --animate_list biasCDA/animacy/spanish.tsv --inc_input --get_ids  --out_file treebanks/UD_Spanish-GSD/es_gsd-ud-test.conllu.out.txt --part 100
# #get text from conllu file
#python biasCDA/src/conll_to_text.py --in_files treebanks/UD_Spanish-GSD/es_gsd-ud-mini-test.conllu --out_dir treebanks/UD_Spanish-GSD

from main_cmd import inflect_gender
from utils.conll import *

def main():
    print("bias-cda-run")
    input_conllu_lines = ""
    count = 0
    with open('/home/nlpsrv/biasCDA/treebanks/UD_Spanish-GSD/es_gsd-ud-mini-test.conllu', "r") as f:
        line = f.readline()
        while line:
            input_conllu_lines += line  # line.replace("sent_id", "sent_id =") if (opt.use_v1 and opt.get_ids) else line
            if line == "\n":
                count += 1
            line = f.readline()

    ##print(f"input_conllu_lines = {input_conllu_lines} \n\n")

    psi_model_path = '/home/nlpsrv/biasCDA/biasCDA/models/psi/spanish.pt' 
    reinflection_model_path = '/home/nlpsrv/biasCDA/biasCDA/models/reinflection/spanish' 
    animate_list = '/home/nlpsrv/biasCDA/biasCDA/animacy/spanish.tsv' 
    #--inc_input --get_ids  
    print("call inflect_gender()\n")
    output_conllu,  output_text = inflect_gender(psi_model_path, reinflection_model_path, animate_list, input_conllu_lines)
    print(f"output_conllu = {output_conllu} \n output_text = {output_text}")
    print("done...")

if __name__ == '__main__':
    main()
