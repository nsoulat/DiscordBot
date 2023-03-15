from unidecode import unidecode

def clean(s: str) -> str:
	"""
	Remove all kind of artefacts for a word (or combination of words), to make comparison easier.
	"""
	s = unidecode(s) 		# transform all accented letters to non-accented letters
	s = s.lower()			# we want the string to be lowercase
	s = s.replace("-", " ") # change hyphens to spaces
	s = str.rstrip(s) 		# remove trailing whitespace characters
	s = str.lstrip(s) 		# remove leading whitespace characters
	# remove all multiple spaces following each other
	s = "".join([s[i] for i in range(len(s)) if i==0 or s[i].isalpha() or (s[i]==" " and s[i-1]!=" ")])
	return s