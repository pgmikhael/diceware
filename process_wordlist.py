import os
import argparse
import pickle
import re 

parser = argparse.ArgumentParser()
parser.add_argument('--wordlist', type = str, default = 'wordlists/wordlist_en_orig.asc')
parser.add_argument('--output_path', type = str, default = 'wordlists/wordlist_en_orig.p')

RE_NUMBERED_WORDLIST_ENTRY = re.compile(r'^[0-9]+(\-[0-9]+)*\s+([^\s]+)$')

def refine_entry(entry):
    entry = entry.strip()
    match = RE_NUMBERED_WORDLIST_ENTRY.match(entry)
    return match, entry

if __name__ == '__main__':
    args = parser.parse_args()
    output = {}
    with open(args.wordlist, 'r') as wordlist:
        for line in wordlist:
            match, line = refine_entry(line)
            if match:
                key, word = line.split('\t')
                output[key] = word

    pickle.dump(output, open(args.output_path, 'wb'))