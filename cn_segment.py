#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import re, string, random, glob, operator, heapq
from collections import defaultdict
from math import log10

def memo(f):
	"Memoize function f."
	table = {}
	def fmemo(*args):
		if args not in table:
			table[args] = f(*args)
		return table[args]
	fmemo.memo = table
	return fmemo

################ Word Segmentation (p. 223)

@memo
def segment(text):
	"Return a list of words that is the best segmentation of text."
	if not text:
		return []

	#candidates = ([first]+segment(rem) for first,rem in splits(text))	
	candidates = []
	for first,rem in splits(text):
		candidates.append([first]+segment(rem))

	return max(candidates, key=Pwords)

def splits(text, L=20):
	"Return a list of all possible (first, rem) pairs, len(first)<=L."
	return [(text[:i+1], text[i+1:]) 
			for i in range(min(len(text), L))]

def Pwords(words): 
	"The Naive Bayes probability of a sequence of words."
	return product(Pw(w) for w in words)

def product(nums):
	"Return the product of a sequence of numbers."
	return reduce(operator.mul, nums, 1)

class Pdist(dict):
	"A probability distribution estimated from counts in datafile."
	def __init__(self, data=[], N=None, missingfn=None):
		for key,count in data:
			self[key] = self.get(key, 0) + int(count)   # 映射到map并去重
		self.N = float(N or sum(self.itervalues()))
		self.missingfn = missingfn or (lambda k, N: 1./N)
	def __call__(self, key): 
		if key in self: return self[key]/self.N  
		else: return self.missingfn(key, self.N)

def datafile(name, sep='\t'):
	"Read key,value pairs from file."
	for line in file(name):
		yield line.split(sep)

def avoid_long_words(key, N):
	"Estimate the probability of an unknown word."
	return 10./(N * 10**len(key))

# global
N = 43514267000000 ## Number of tokens
Pw = Pdist(datafile('utf8_frequency_dict.txt', ' '), N, avoid_long_words)

def main():
	# 注意: segment()输入的字符集，需要和字典匹配
	word_list = segment('研究生教育研究生命起源不能改变研究生命运')
	print " ".join(word_list)

if __name__ == '__main__':
	main()
