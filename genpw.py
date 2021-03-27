import argparse
import random
import string
from datetime import datetime, timezone
import pickle 

parser = argparse.ArgumentParser()
parser.add_argument('--seed', type = int)
parser.add_argument('--length', type = int, default = 9)
parser.add_argument('--wordlist_path', type = str, default = 'wordlists/wordlist_en_orig.p')
parser.add_argument('--randomness_source', type = str, default = 'from_dice', help = 'supports: [from_dice, from_seed]')

class KeyGenerator():
	def __init__(self, args, wordlist):
		keys = self.get_keys(args)
		self.passphrase = self.generate_keyphrase(keys, wordlist)
		self.summary = '{} {}'.format(self.get_summary(args), self.passphrase)

	def __call__(self):
		return self.passphrase

	def get_keys(self, args):
		if args.randomness_source == 'from_dice':
			return self.inputDigits(args.length)
		if args.randomness_source == 'from_seed':
			return self.generateDigits(args.length)

	def generateDigits(self, stringLength):
		"""Generate a random string digits """
		keys = [''.join(random.choice(['1','2','3','4','5','6']) for _ in range(5)) for _ in range(stringLength)]
		return keys
	
	def inputDigits(self, stringLength):
		keys = []
		print('Collecting {} Dice Rolls: '.format(stringLength))
		while len(keys) < stringLength:
			die = input('Enter dice results:')
			if any([int(i) > 6 for i in die]) or len(die) != 5:
				print('Value out of range. Digits must be [1-6]')
			else:
				keys.append(die)
		return keys

	def generate_keyphrase(self, list_of_keys, wordlist):
		return '_'.join([wordlist[key] for key in list_of_keys])

	def get_summary(self, args):
		if args.randomness_source == 'from_dice':
			return "Passphrase of length {} from dice:".format(args.length)
		if args.randomness_source == 'from_seed':
			return "Passphrase of length {} from seed {}:".format(args.length, args.seed)

if __name__ == '__main__':
	args = parser.parse_args()

	if args.seed is None:
		args.seed = int(datetime.now(timezone.utc).strftime('%U%m%f%H%M%d%S%Y%j%W'))

	#---------
	# Set Seed
	#---------
	random.seed(a=args.seed)

	#-------------------
	# Read wordlist dict
	#-------------------
	wordlist = pickle.load(open(args.wordlist_path, 'rb'))

	#-----------
	# Generator
	#-----------
	generator = KeyGenerator(args, wordlist)
	print(generator.summary)
