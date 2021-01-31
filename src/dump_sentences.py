import argparse
from utils.conll import load_sentences

def get_args():
    """
    :return: command-line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_files', required=True, nargs='+', help='Input conllu file')
    parser.add_argument('--out_file', required=True, help='Output conllu file')
    return parser.parse_args()


def main():
    """
    Program to dump sentences from collu files.
    """
    # Get command line arguments
    opt = get_args()

    out = open(opt.out_file, "w")
    if not isinstance(opt.in_files, list):
        opt.in_files = [opt.in_files]
    count = 0
    # Find and convert sentences with animate nouns for each file
    for i in range(len(opt.in_files)):
        file = opt.in_files[i]
        print("Processing file " + str(i + 1) + " out of " + str(len(opt.in_files)) + " files")
        part = 1
        with open(file, "r") as f:
            # line = f.readline()
            # Work in batches of 100,000 sentences to avoid memory issues
            not_empty = True
            while not_empty:
                print("  Partition", part)
                # Load sentences
                print("    Loading partition 10000 sentences at a time...")
                conll, not_empty = load_sentences(10000, f)
                for sentence in conll:
                    print(sentence.text)
                    if sentence is not None:
                        print('-')
                        out.write(sentence.text + "\n")
                #out.write("\n\n".join(conll.text) + "\n\n")
    out.close()
    print("Done")


if __name__ == '__main__':
    main()
