def gather_words():
	f = open('src/words/english.txt', 'r')
	words = f.read()
	f.close()
	return words.split('\n')[:-1]
