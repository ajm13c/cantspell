
# finds all words that can be spelled with substrings of the input word
# I guess the name for this is 'partials'?
# this is not like an anagram unscrambler -
#  all letters are in the order they were in the original word

import sys
import string
import enchant
import itertools

#global English Dictionary
d = enchant.Dict('en_US')
blacklist = set(list(string.ascii_lowercase))
blacklist.remove('i')
blacklist.remove('a')

#parameters
singleUse = False
#lazy find is the simple subword implementation
basicSearch = False
overrideValidation = False

#this is exponential, this is the best complexity for this type of problem
def all_subsets(n: int) -> list:
	indexes = [x for x in range(n)]
	l = list()

	for i in range(len(indexes)+1):
		for subset in itertools.combinations(indexes, i):
			if len(subset) > 0:
				l.append(list(subset))

	return l

def complex_find(word: str) -> list:
	s = set()

	l = all_subsets(len(word))

	for subset in l:
		w = ""
		for index in subset:
			w += word[index]
		if is_word(w):
			s.add(w)

	if word in s:
		s.remove(word)

	return list(s)


def basic_find(word: str) -> list:
	#set of strings for fast insert I guess
	s = set()

	#simple substrings
	for start in range(len(word)):
		for end in range(start+1, len(word)+1):

			if is_word(word[start:end]):
				s.add(word[start:end])

	if word in s:
		s.remove(word)

	return list(s)

#layer over the enchant call
def is_word(word: str) -> bool:
	if word in blacklist:
		return False

	return d.check(word)

def validate(word: str) -> bool:

	if overrideValidation:
		return True

	if len(word) == 0:
		return False

	if len(word) < 2:
		print("Argument must be larger than 1 character.")
		return False

	if not word.isalpha():
		print("Input word must only contain letters.")
		return False

	if not is_word(word):
		print("Argument must be a real word, please check your spelling.")

		suggestions = [x.lower() for x in d.suggest(word) if x.isalpha() and is_word(x)]

		if len(suggestions) > 0:
			print("Did you mean: ", suggestions)
		
		return False

	return True

def findWords(word: str):
	if basicSearch:
		words = basic_find(word)
	else:
		words = complex_find(word)

	if len(words) == 0:
		print ("unable to find any subwords")
		return

	print ("You can't spell '", word, "' without:", sep='')
	for subword in words:
		print(">",subword)


if __name__ == "__main__":
	#check parametrs:
	if len(sys.argv) > 1:

		for i in range(1, len(sys.argv)):

			# argument case: '-o, -ob'
			if sys.argv[i][0] == "-" and len(sys.argv[i]) > 1:
				for j in range(1, len(sys.argv[i])):
					arg = sys.argv[i][j].lower()

					if arg == 'b':
						basicSearch = True
					elif arg == 'o':
						overrideValidation = True
					else:
						print (arg, 'is not a valid parameter.')
						raise SystemExit

			# if the last arg is an input word rather than a parameter,
			# only perform one search and then exit
			if i == len(sys.argv) - 1:
				singleUse = not (sys.argv[i][0] == '-')

	if singleUse:
		word = sys.argv[len(sys.argv) - 1]
		if not validate(word):
			raise SystemExit
		findWords(word)

		raise SystemExit

	while True:
		try:
			word = input("--> ").strip().lower()
		except EOFError:
			print("")
			break
		except KeyboardInterrupt:
			print("")
			break

		if not validate(word):
			continue

		findWords(word)
