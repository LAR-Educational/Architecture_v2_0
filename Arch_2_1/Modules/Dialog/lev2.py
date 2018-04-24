import distance
import similarity
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy


def levenshtein_short(string_one, string_two):
	
	print distance.nlevenshtein("mamae me mandou tentar alguma coisa", "mae me mandou tentar alguma coisa", method=1)  # shortest alignment
	print distance.levenshtein("mamae me mandou tentar alguma coisa", "mae me mandou tentar alguma coisa")

def function(string_one, string_two):
	
	print distance.nlevenshtein("mamae me mandou tentar alguma coisa", "mae me mandou tentar alguma coisa", method=2)  # longest alignment
	print distance.levenshtein("mamae me mandou tentar alguma coisa", "mae me mandou tentar alguma coisa")
