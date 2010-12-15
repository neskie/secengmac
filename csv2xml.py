#!/usr/bin/python
# -*- coding: utf-8 -*-
#This file will conver the CSV to a structed XML file.
from xml.dom.minidom import Document
import codecs

class Symbol:
	def __init__(self):
		self.filename = ""
		self.text = ""
		self.xmldoc = Document()
		self.xmldic = Document()

		# Create the <wordlist> base element
		self.wordlist = self.xmldoc.createElement("wordlist")
		self.xmldoc.appendChild(self.wordlist)

		# Create the <dictionary> base element
		self.dictionary = self.xmldoc.createElement("d:dictionary")
		self.xmldic.appendChild(self.dictionary)
		self.dictionary.setAttribute("xmlns", "http://www.w3.org/1999/xhtml")
		self.dictionary.setAttribute("xmlns:d", "http://www.apple.com/DTDs/DictionaryService-1.0.rng")

	def set_filename(self,filename):
		self.filename = filename
	def process_file(self):
		f = codecs.open(self.filename,encoding="UTF-8")
		text = f.read().strip()
		for i,j in enumerate(text.split('\n')):
			try:
				shs,eng = j.split(';')
			except ValueError:
				print i;
			eng = unicode(eng)
			shs = unicode(shs)
			self.make_word(i,shs,eng)
			self.make_entry(i,shs,eng)
	def make_word(self,id,shs,eng):
		# Create the word <word> element
		word = self.xmldoc.createElement("word")
		word.setAttribute("id", str(id))
		self.wordlist.appendChild(word)
		# Create a <secwepemc> element
		secwepemc = self.xmldoc.createElement("secwepemc")
		word.appendChild(secwepemc)
		# Create a <english> element
		english = self.xmldoc.createElement("english")
		word.appendChild(english)

		# Give the <secwepemc> elemenet some text
		sectext = self.xmldoc.createTextNode(shs)
		secwepemc.appendChild(sectext)
		# Give the <english> elemenet some text
		engtext = self.xmldoc.createTextNode(eng)
		english.appendChild(engtext)

	def make_entry(self,id,shs,eng):
		# Create the word <entry> element
		entry = self.xmldic.createElement("d:entry")
		entry.setAttribute("d:parental-control",str(1))
		entry.setAttribute("d:title", shs)
		entry.setAttribute("id", str(id))
		self.dictionary.appendChild(entry)
		# Create a shs <index> element
		index = self.xmldoc.createElement("d:index")
		entry.appendChild(index)
		index.setAttribute("d:value", shs)

		# Create a eng <index> element
		engindex = self.xmldoc.createElement("d:index")
		entry.appendChild(engindex)
		engindex.setAttribute("d:value", eng)

		# Create a <h1> element
		title = self.xmldoc.createElement("h1")
		entry.appendChild(title)
		sectext = self.xmldoc.createTextNode(shs)
		title.appendChild(sectext)

		# Create a <ul> element
		list = self.xmldoc.createElement("ul")
		entry.appendChild(list)

		# Create a <li> element
		li = self.xmldoc.createElement("li")
		list.appendChild(li)

		engtext = self.xmldoc.createTextNode(eng)
		li.appendChild(engtext)

filename = "EnglishSecwepemcDictionary.txt"
xmlfilename = "SecwepemcEnglish.xml"
handler = Symbol()
handler.set_filename(filename)
handler.process_file()
xmltext = handler.xmldic.toprettyxml(indent="   ",encoding="UTF-8")
file = open(xmlfilename,'w')
file.write(xmltext)
file.close()

xmlfilename = "EnglishSecwepemcDictionary.xml"
xmltext = handler.xmldoc.toprettyxml(indent="  ",encoding="UTF-8")
file = open(xmlfilename,'w')
file.write(xmltext)
file.close()
