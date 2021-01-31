import argparse
from animacy import get_animate_samples
from model import Model
from sigmorphon_reinflection.decode import get_decoding_model
from sigmorphon_reinflection.reinflection_model import *
from tqdm import tqdm
from utils.conll import load_sentences_from_file, load_sentences_from_string
from conll_to_text import getTextFromConllu


def inflect_gender(psi_model_path, reinflection_model_path, animate_list, input_conllu_lines):
    # Load models
    model = Model([0, 1, 2])
    psi = torch.load(psi_model_path)
    print(psi.shape)
    with torch.no_grad():
        reinflection_model, device, decode_fn, decode_trg = get_decoding_model(reinflection_model_path)
    print("Models loaded")
    ##print(f"inflect_gender()::input_conllu_lines = {input_conllu_lines}\n")
    conll = load_sentences_from_string(input_conllu_lines)
    # Extract sentences with animate nouns
    print("    Finding animate nouns...")
    use_v1 = False
    hack_v2 = False
    get_ids = True
    samples = get_animate_samples(conll, animate_list, use_v1, hack_v2)
    del conll

    # Convert gender of sentences
    converted_sentences = []
    # converted = samples.apply(model, psi, reinflection_model, device, decode_fn, decode_trg)
    # converted_sentences.append(converted)
    for sc in tqdm(samples, total=len(samples)):
        try:
            converted = sc.apply(model, psi, reinflection_model, device, decode_fn, decode_trg)
            converted_sentences.append(converted)
        except ValueError:
            continue
        except IndexError:
            continue
    ##print("converted_sentences \n\n".join(converted_sentences) + "\n\n")
    textForm = getTextFromConllu(converted_sentences)
    print("Done")
    return converted_sentences, textForm
