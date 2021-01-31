from pyconll import load_from_string

def load_sentences_from_file(n, file):
    count = 0
    lines = ""
    line = f.readline()
    while line and count < n:
        lines += line  # line.replace("sent_id", "sent_id =") if (opt.use_v1 and opt.get_ids) else line
        if line == "\n":
            count += 1
        line = f.readline()
    not_empty = True if line else False
    conll = load_sentences_from_string(lines)
    return conll, not_empty

def load_sentences_from_string(lines):
    print(f"load_sentences_from_string::lines = \n{type(lines)}\n{lines}\n", flush=True)
    try:
        conll = load_from_string(lines)
    except Exception:
        conll = load_from_string("")
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)
        print(f"******load_sentences_from_string()::bad conll*************", flush=True)
    print(f"load_sentences_from_string::conll = {type(conll)}\n")
    return conll


def load_sentences(n, f):
    print("load_sentences()", flush=True)
    count = 0
    lines = ""
    line = f.readline()
    while line and count < n:
        lines += line  # line.replace("sent_id", "sent_id =") if (opt.use_v1 and opt.get_ids) else line
        if line == "\n":
            count += 1
        line = f.readline()
    not_empty = True if line else False
    ##print(f"lines={lines}", flush=True)
    try:
        conll = load_sentences_from_string(lines)
    except Exception:
        conll = load_sentences_from_string("")
        print("******load_sentences::bad conll*************", flush=True)
    #print(f"conll = {conll}")
    return conll, not_empty
