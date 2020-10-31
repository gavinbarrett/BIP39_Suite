def gather_words():
	# return the list of mnemonic words
	f = open('./words/english.txt', 'r')
	words = f.read()
	f.close()
	return words.split('\n')[:-1]
