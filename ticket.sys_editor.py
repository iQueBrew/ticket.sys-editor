#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import BooleanVar, BOTH, Button, END, Entry, Frame, Label, LabelFrame, Listbox, Menu, StringVar, Tk, Toplevel
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.ttk import Notebook
from tkinter.messagebox import askyesno, showerror
from zlib import compressobj, decompress, DEFLATED
from PIL.Image import open as imageopen, frombytes
from PIL.ImageTk import PhotoImage
from os.path import isdir, splitext
from os import mkdir, getenv
from sys import argv
from json import dump, load
from io import BytesIO

VERSION = "1.7.1"

class LabelledEntry(Frame):
	def __init__(self, parent, text = None, textvariable = None, state = 'normal', isHex = True, length = 8):
		Frame.__init__(self, parent)
		self.text = text
		self.textvariable = textvariable
		self.state = state
		self.isHex = isHex
		self.length = length

		self.label = Label(self, text = self.text, textvariable = self.textvariable)
		self.entry = Entry(self, state = self.state)
		self.label.pack(side = "left")
		self.entry.pack(side = "right")

		self.entry.config(validate = 'key', validatecommand = (self.entry.register(self.checkEntry), '%P'))	

		self.insert = self.entry.insert
		self.delete = self.entry.delete
		self.get = self.entry.get

		self.newText = None

	def set(self, text):
		self.newText = text
		self.state = self.entry['state']
		self.entry.config(state = 'normal')
		self.delete(0, END)
		self.insert(END, text)
		self.entry.config(state = self.state)

	def checkEntry(self, text):
		if (all(i in "0123456789abcdefABCDEF" for i in text) or not self.isHex) and (not self.length or len(text) <= self.length):
			return True
		return False

class ButtonEntry(Frame):
	def __init__(self, parent, text = None, textvariable = None, state = 'normal', command = None):
		Frame.__init__(self, parent)
		self.text = text
		self.textvariable = textvariable
		self.state = state
		self.command = command

		self.button = Button(self, text = self.text, textvariable = self.textvariable, command = self.command)
		self.entry = Entry(self, state = self.state)
		self.button.pack(side = "left")
		self.entry.pack(side = "right")

		self.insert = self.entry.insert
		self.delete = self.entry.delete
		self.get = self.entry.get

	def set(self, text):
		self.state = self.entry['state']
		self.entry.config(state = 'normal')
		self.delete(0, END)
		self.insert(END, text)
		self.entry.config(state = self.state)

class ButtonImage(Frame):
	def __init__(self, parent, text = None, textvariable = None, command = None, uImg = None, bg = None):
		Frame.__init__(self, parent)
		self.text = text
		self.textvariable = textvariable
		self.command = command
		self.uImg = uImg
		self.bg = bg

		self.button = Button(self, text = self.text, textvariable = self.textvariable, command = self.command)
		self.img = Label(self, image = self.uImg, bg = self.bg)
		self.button.pack(side = "left")
		self.img.pack(side = "right")

class OwO_UwU(Tk): # Just a random name choice, no reason behind it at all

	def __init__(self):
		Tk.__init__(self)
		
		self.icon = b'x\x9c\x9dV\tP\x93W\x1e\xffPZ\xab\xd5Z\xc5\xda\xd9\x9d\xedj\xdb\xe9\xacV\xad\xa5\xb5\x80\xa2\x80\x07*r\x88\x1c\x06\xe4\x88\xdc\x87@\xe4\x0c\xc8M8\x92p\t$!\x04\xc2\x15B\xb8\xef#\x80B\x8a\x80 (xPE\xb4\xd5\xaa\xdd\xba;\xbb\xed\xb8\xb5\xdb\x9d\xdd\x99\xdf\xfe\x13\xa4\xe3\xec\xba\x9d\xba/\xf3\xcb\xff}\xef{\xef\xff\xfb_\xdf{\x8fa\xf4\xe8\xb7q#\xa3\xfdg\xea\xded\x98\xf5\x0c\xc3l"\xd0\x10c\xc1,\x8c/6\x83\xd7\x17\xf0\xb2\xcd\xd2\xf2\xe0\xbb\x87\x0e\x1e\xf6\xb0\xb1\xb6\x95\x1e\xb3w\x18qppz\xe0\xe8\xe0\xf4\xc4\xe1\x98\xe3\x13;;\xfb\x87V\x87\xad\xc7\xf6\xef?P\xb2\xdbt\x8f\x87\xb1\x91\xc9{/\xcf\xf0\xe2fcc\xbb\xdd\xc1\xdeA\xe6\xe9\xe1\xf9\xc0\xdb\xd7\x1f\xde\xbeA`{\x05\xc1\xd3+\x18\x1e\xec@\xb8y\x04\xc0\xd5\xdd\x0f,\xd7\x93p>\xee\x0e\'\'\x16lm\x8f>\xd8k\xb1\xaf\xcc\xc4x\x97\xe1\xff\xcb\xeb\xe8\xe0\xf8\x96\xb3\x93s\xb6\x8f\x8f\xef?BB8\x08\x0e\x89\xc0\xe9\xd3\xd1H\x8d\x0bGA\xaa\x07\xca2lP-8\x8aj\xbe\x9d\xae\x9f\x9f\xe2\x89\x84\xe8P\xf8\xf8\x06\xc2\xd9\xc5\x13\xce\xce\xae\xb0\xb7w\xf8\xa7\xd9\x1e\x8b<\xa3\x1dFo\xbf\x0c7\xeb\xb8\x8b\xa1\xa7\'\xfb2\',\x1c\x9c\x88x\xc4\xc5r!\xe3\x07\xa2=\xc7\x10}\xc2\xdf\xa1\x9f\xff\n\xcee2\x18\xc8 \x90\xd4\xf5\xf9\xcb\xd0/\xfc=\xdarw@\x9a\x15\x88S\xc1\xc1pt\xf6\x84\x933\x0b\x87\x0f\x1e\x9e\xa6\x9c|\xfak\xb8\xdd\xdd<\xf6\x06\x06\x04}\xc3\x8d%\xdex\x1e\x8a\x05\x1ct\xe5|\x085\x8fAO\x1a\xf1d\xbf\n\x8dh3FJ?\xc5X\xf9\x0e\x8cW\xee\xc0(\xf5\x87\x8a6\xa1\x9f\xde\xf5\xd2\xbc\xbet=\xf4\xe6\x7f\x8a\xc2\xf4Sp\xf3\xf4\xa7X\x9c\x80\x9d\xed\xd1o\xc9\x86\x03\xbf\xc4}\x92\xcd\xde\x16\x16\x1a\xfa8!1\r\xe9\xe99\xa8\xc9qDw\xfaJt$\x117\x7f\x15\x86K\x8cpI\xe1\x88I%\x1b\x97j\xbc0\xa1\xf4\xd2I-&k<I:aXf\x8a^\xc1\x1a\xb4\'2Pg\xbd\x89\x9a\\g\xf8\xf9s(\x16\xae\xb0\xb59\xfag\xa3\xcf\x8c?~\x11\xb7\xbf\x9f\xef\xba\xb0\xb0\xb0\xc9\x8c\x0c\x01\x04\x82\xb3\xa8\xe1\x1fAK\x02\x83\x16\xe2\xee\xce\xd2\x87Fj\x84\xd1r{\x8c\xcam1"\xb7"y\x84\x9e\xadI.\xc2\x86\xe2q\x14c\x15\x0e\xb8Pj\x86\x1e\xe1\n\xb4\x90\r\xed\xc9KQ\x97{\x8cl\x08\xc3q\xd6\tXYYO\x93\r\xffU\x0f!\xc1\xa7\x04YY\x02\xe4\xe6KP\x9e\xe5\x0c\x15w\t\x1a\xe2\x89?\x85|\x17.\xc1@\xc1Z\x0c\x89\xde\xc3\x90\xf8\x0f\x18\x14o&\xb9\x1d\x83\x12C\xeaS\xec%\x9f@S\xfc\t\xf5\xb7\xe0\xbch#\x06\xce\xaeE\x8f@_\xb7\xb6\x81|h\x8c\xd7G\xb9\x80E\xdf\x8b?\\\\\xdcaa\xbe/\xf7yn\x8a\xf9\x96\xb44\xde\x8f"\xb1\x1c\xc591\x90G.\x87\x92\xcb\xe8\xf8\x9b\xc8\xff\xd6T\x06\x1dTk\x9dY\x0c\xba\xf8\x04\x92\xdd\xa4\xbfG\xf8*\xba\t=\x82\x05\xd9%\xd0C\'\xd5b\x1b\xd5IK2\xad\xd5r\x13jc\x19\xd4\x9cy\x03\xb9\xa9\xa1`\xb9\xd0w\xea\xc4\xfa\xc9\xd8x\xe7G\x8b\xfc\xdc\xe8h\xa9DR\x02iq\t\n\xa3\xb6\xa2\xf44\xad\x89cP\x7f\xe6\x99\xfd\x89\x0bz\xb4Rk\x8f\xeeYk\x1b\xc9\xe6\xe4\x85\xb1E\xa9}\xa7\xb5{\x11\xf5\xf1\x0b\xba\xe4\xe1\x0c\xca\x12wA\xfb-\x9fp\xf3\xc4\x81\xfd\x96eZ\xee\x98\xa8\xc8\r\x82,\xfe\xa3\xca\xeaZ\x14dFA\xe0\xcb\xa0<\x9a\x81\x92lV\xd1\xba\xba3\x0bR\x15\xbb\xd0W\xd2;E\xe4R\xa8\x927\xa06~=j)N\xaa\xc59/\x80\x96[\xeb\x7f\x05\xad+\x0c\xd1\x87 9\x94\xf6,\x1f89:?61\xde\xf9\xfe\x99\xb8X\x17YI\x19\xaa\xaaj\x90\xc91A~ \xcd\x8dbPMPh\xb9b\x16l\xa9!YIqiH\xfb\x10\x97\xd4\xc5\xb8\x7f\xff>\xa6/jP\x97\xf2\x81n^U\xc4\xc2\xfc\x1a-h\xad6\x7f\xda~u$\x8d\xd3s\xa5\x96?\x98A\x1e\xd7\x1cAA\x1c\xb8{\x9c\xa4:\xb0\xf0\xe0\xa5\xa5IT\xaaF\xc8\x8b\xc5H\xf2^\x87\xa2S\xa4\x8b\xbb\x02\x8a\x84\xf7Q\x9b\xf8\x01\xe5m%\xca\x89\xb7"r5\xba\x8a\x8e\xe3\xe1\xdd[x4\x7f\x03=\x85;i?\xda\x8cz\xde\x16z\xb7\nM\x02\x13\xd4\xa5nBu\xdc\xdb\xb4\xf6=TE\xeb\x13\xe7j\xa8x\x86\xf4\xfc.\xcaH\x87(\x94\x810\xe4\x1d\xc4F\x85\x83}\xd2\x17G\xac\xacKssr.\xb4\xb5v@$LD\x82\xfbk:\x1b\xab\xe2\xd6bZ\xd3\x86\xe1\x0e\t\xca8\xcb\xd1$\xdc\x8b\xcbC\xf5\xe8\x93\xfb\xa0\x99o\x82\xaeBgt\x97\x05B\x16\xf6\x9a\xce\xb6\xa9>\x19\xc6\xba\x8a\xe9\x9d\x11\xae\x0c\xaa0~\xbe\x99\xf6\xc1C\x98\x9d\x1c\xc0\xfc\x17\xb3\x18W7\xa2AxX\xe7[\xa6\xdfj\xa4pC\xe0\xe5\x1d\x00GG\xa7\xb1b\xb1\xe8aWw?rR|\x10\x7f\x82bDs\x8a\t\xf3\x97\xdb1\xd4$@m\xd2&|}\xef\x1e\xd4\xf2\x00Hi\\\x16\xc2@J6\x8e4\xa5\xa1\xbfI\x84J\xeez\xdc\x9f\x9bEC\xce1H\xfc\x19\\\x1f>\x8b\xf1\x01\x05f\xce\xe7\xe3\xcb\x9b\xd3P\x9cy\x97r\xbf\x12\xd5\t\x1bP\x14\xa2\x87T\xf6\x12\xf0\xb8l\xda\x0fB\xe0v\xc2\xfdQ\x85\\\xfe\xbd\xbao\x10Yq,\xc4\xba0\xc8\x0f\xa28Q\r\xdc\x9chB\xbf*\x01W\x87\xf2q\xeb\xeaU\xc8\xc2\r \xa5\xf8\xc98\x0c\xc44\xa7\x99\xbf\x037\xaf_\x83*\xf3\x10\xe6gF\xa0\x128@D\xb5;}.\x15\x17\xfb[p}\xa4\x11\x03\xaaL\x94F\xfc\x06r\xee;\x90E\xacB\x01\xd9\x9d\xe8\xc6\x80\x17\xc3B\xf0)\xca\x81\xe7\xc9\'\xd5\x95\x95\xdf\x9f\x1f\x1cFf\x9c+\xa2\x9c\x18d\x93\x0f\xe2\xb0\x95\xb8{M\x83\xc1f\t\xbe\x9e\x9b\xc0X\x9f\x12\xa2\xa0%(&~-\xb4\xfc5\t\x1f\xe2\x1e\xf9\xddY\x9e\x8e;\xd7\xc6Q+pD\x817\x83\xab\x1a\tF\xfb\xca\xa1.\xf7\x86\xa6M\x06y\x8c!f\xc7\x070\xd8T\x00\xa1\x8f\x9e\xce\xc7\xd4h\x16BB#\xe1\xed\xe5\xfd\xa4\xaa\xa2\xe2\x81\xe6\xf3\x11\x08\x93\x03\x11fO\xf9!\x1d\xe2\xd3\xebp\xa19\x0f\xea\xb2(\xdc\xbb9\x89\xcf;e\xba\x98\x94\x84-@\xcb\xdf\x90\xb1\x03\x8f\x1f=\xc2\x98\xba\t\xb3\xa3\x1dP\xa6Y\xa0,j\x1d\xc5\xbf\x03C\xf5\xc9\x10\x07\xafD[\xa1\x07Z\n\xe8|\xe8\x92B\x1e\xb7\x19\x99^\x0c\xa2\x9c\xf5\x91\x1c\xe5\r\x0e\x9d\xe5>\xde\xbe\x0f+\xe4e\xc3cc\x13\x90\xe4e\xc0\xdf\xe6U\xa4x2\xc8\xa18\x16\x04\xbf\x85\xa2\x8070= \xc2\xc4P\x1f$!+t\xfbR\x19\xed#E\x14#\x8d\xe24\xfe\xf2\xd7\xa7P\xa6\xeeAq\xf0\xc2xY\x84\x1eJ8K!%\x1b\xa5\x94\'\t\xc5\xaa4j\x05\xf2i\xbe\x90\xfcJe3\xe08\xadF\x12\x97\x83\x88\xc8X\x9cd{\x8d\xc9\xa4\xc5\xe2\x8b\x17\xc7\xd1\xa8\xaa\x81\x8f\xedZ\xc4\x1cgp6\xf4\xb7\xf8bj\x12\xdd5|T\xc7n\xc4\xf4h?\x1a\xf3X\xb4\x87\xad\x80<b\x19j\x92\x0c\xf1\xcdW_a\xa2\xb3\x08r\xce+\xa8\x8c1\xa0o\xcd@\'+H\x96G\xafCy\xcc\xdb(#Y\x12\xbe\x8c\xea\x8eA\x96\x0f\xa3\x8b}(\xeb\x1d$\'\xc4#:\xe6\x0c\x9d\x05\xae\xb2\x82\xfc<\xd6\xd0\xe0\x104\x9a\x0b8\xcd\xde\x8d \x1b\xaa\x0f\xaf\xd5\xb8\xa2\x96A\xa3LFi\x98\x01\x9a\xd2wcH\x99\x8d\xce\xc2`\x82?&{\x14\x18\xa9O\x82\x82\xea\xaa6~3j\x13\xb6B\x95\xb0\x8d\xfa\x1f\xe9\xa0L\xd8\x0ee\xfc\xc7\xa8>c\x88r\xee6\xca\xa7\x81\xce\xf7\x90\xa3\x14\x7f\xbfCHI\xe1!:\x9a\x8bcG\x8f\xb9\xe7f\x0b7\xb4\xb7\xb6>\xbaz\xf5:\xf2\xb3\x12\xe1\xbe\x9fA4\xc5 ?`\rji}c\xaa\x19\xea\x92>AC\xd2\xc7h\xe3[\xd2]\xc4\x0e\xad\xe9\xb4\xd7\x10oK\xfa.\xb4\xf0LI\x9a.\xc8gh\xe6\xedBc\x9a)\x1aR\xf6\xa0>\xc5\x02b\xceF\xc4\xb0\x18xY\xe9\x83\x17\x1f\x89\xe4d\x1eBC9\xdfZ\x1f\xb1\xd6\xddS\xcbdR\xc9\xcc\xf4\x0c\x06\xcf\x0f\xc2\xd7a\x1b\xbc\xad\x18\xa4\xb0_\xd7\xe9\xed\xe2[\x10\xcc\xd0\xcd\xdfC0\xa5{\xc8.\x82)\xfa\xb2-\xd0\x97c\x0e\xb5\xd0\x8c\xfa\xe6\xcf`\x01u\xf6\xc2X\x8f\xc0\x02\xbd\xc2}h\xcf\xb4@\x9a\xd7\x1b\xf0>D\xfe\xbb\xed\x84\x80\x9f\x8b\xd4T\x1e<=\xd8\xb2\xc5\xf3\xaf0/ws\x7f_\xef\xd3[\xb7\xe6PR(\x84\x93\xf9r\x04P\x1e\xc4\xe1\xefc\xb4\xd8\x06C\x85\x07t\xf8\xbc\xc8\x12\xc3"K\\\x10\x1f\xc4\x88\xc4\x92p\x00#\xe2\x03\x18\xa5\xfe\xa8\x84\xc6t\xe3\x87\x9e\xcd9\x84\x89R{H#?\x80\xbf5\x037\xcb5\xe0\xa7%@\x98\x9d\x07.7\xf6\xeft\xa7\xde\xf6\xfc\x1d\xa0\xbc\xb4$sff\x1a33\xd7\x90\x14\xe9\x03\xc7\xddz\x08\xb4[\x02e\x8a1n\xd4\xfb\xe0\x8a\xc2\rSU.\xb8R}\x02\xd3\n-\xdc0Ss\xe2\x19\xdc~\xc6\x95jW\\Sz\xe0V\xa3?\x1a(\x17\x81\xb6z`\x99\xeb#1\xd2\x1fEER\xf0\xe9\x8e\xe3\xe3\xed\x93\xfd\x9f\xf7\x9f\xa2\xb3\xf9\x06M\x8d\xf5\xe3\xb7\xe7\xe60~q\x02\x11~\xf6\xb0\xdf\xc9\xc0\xf7\x88\x1e\xaa(\x87_\xaaS\xf1\xf0|\x06\xee\xf6\xc4\xe3vW,\xe6:\xb9\xb8\xdd\x19\xa3\x83\xb6?\xdf\x15Gs\x12\xf1h0\x13\xf7\xfby\xa8I\xdd\x0f?+=8\xed^\x82\x98\xa0\xe3(\x91\x95\x13\xbf\x04\x91\xe1\x91S\xac\xe3\xac\xf5/\xba\x03\x8a\x0b\xf2\xb7\xa8\xbb;\xbf\xb9{\xf7\x0e&\xc8\x06\xad\xcdv;\x97\x83e\xc6 -`+45\xf1x<\xdd\x8c\'sj<\xbd\xdd\x8b\x1f\xe6\xba\xf0\xc3|7\x9e\xde\xe9\xc5\xdfn\xab\xf1\xa7\x99V\x0c\xd7&"=p;\x9c\xf70p0[\x85\x04\xd2QQ\xa9\x80\xbc\xbc\ni\xa9i\x8f\xd9\x9e\xecm/\xe2^l\x12Q\xa1\x99\xba\xb7\xfb\xc1\x9d\xf9y\\\xbbv\x83\xea!\x07\x9ev\xdba\xfd\x19\x03\x17\x8b%\x88\xf7\xda\x8aJ\xa1\x17\x06\xeb\xf30\xd9[\x85\xc9>\x05\x86\x1a\xf2i\x8c\xce/\xaf\x8f\xe0j\xb1\x14\xb6\xc6\x0c\xbc\x1dw O\x90\x0eU]\x13\x94\xcaZ\x8a;\xff\x8f~>\xbe{\x7f\x89\xfb\xe78\x14\x15l\xebhm\x9e\x98\x9d\xbd\x8e\xbbw\xbf\xc4\x85\xe1a\x9c\xe5\xa7\xc0\x9fe\x0e\xfb=\xabac\xb4\x04\xf6&\x0c\x1cM\x97\xea`o\xa2G\x9cKq\xccl\r\x02]\xf7A\xc8KD]]\x03\xda;\xbaP\xa7\xaaCfF\xe6d`@\xc0\x0b\xef\xdd\xff\xab\x15\x8b\n\r\xaa+\xe4\x99\xc3\x9a\xa1\x1f\xe7\xe6na\x8e\xea\xe2\xd2\xc4\x04Z\x1aT(\xce\x17"=\xe14\xd5\xa9\x1f\x92\xa2\xfc\xe8\x9b\xe6\xa0(7\x0b\xca\xaa*\xf4\xf4\xf4\xe2\xdc\xb9Atw\xf7\xa0B^\xf1SB|\xbc\x90\x13\x1a\xb6\xeee\xb8\x9foRQ\xe1\x16eu\xa5d\xa0_}\xef\xca\xe5)\xcc\xde\xb8A\x98\x85v\xbf\x9a\xba<\x8d\xcbS\xd3\x98\xbc4\x05\xed\x1e><|\x01\xbd==PT+\xee\x0b\xf8|i\x1c\x97\xfb\x8b\xb9~\x99Vx6o\x83T"vQTU\x8a\x9a\x1a\xea\x87;\xdb\xdb\x1etut|\xd7\xd1\xd6\xfa]Sc\xe3C:G\x87E\x85\x85\xe2\xcct\x9e+\xf9\xbc\xf1\xd7\xea\xc5\xbde\x00\x89\x7f1\x8c\xf9O\x0c\xb3\xe1{\x86Y}\x8fa\x96i\x18f\xa9\x16)\x0c\xa3\xb7\x88_\xab\xf3\xf95\x8bz\xb4:\xb5\xba\xb5\x1cZ.-\xa7\x96\xfb\xdf\xa5)\x04\x82'

		dec = decompress(self.icon)
		
		iconphoto = PhotoImage(imageopen(BytesIO(dec)))
		
		self.wm_iconphoto(True, iconphoto)

		self.strings = {"en": ["ticket.sys editor", "Open file", "Reload current file", "Save", "Save as", "Exit", "File", "New ticket", "New ticket.sys", "Import ticket.dat", "Edit", "Overwrite keys when importing", "Use more accurate colour mapping", "Options", "About", "Help", "Ticket options", "General", "App info", "Misc.", "Ticket data", "Title:", "ISBN:", "Unknown value #1:", "Unknown value #2:", "Export ticket", "Replace ticket data", "Delete ticket", "Select ticket.sys", "iQue Player system files", "All files", "This file is not a valid ticket.sys!\nTicket #1 magic: {}", "None found", "Magic:", "Thumb image length:", "Title image length:", "Thumb image:", "Title image:", "Allowed SK calls:", "CID:", "Ticket ID:", None, "Select file to save to", "Invalid value for {} {}\nPlease make sure it is {}-byte long hex integer!", "Title or thumb image length is incorrect! Please tell Jynji that this message appeared, or try a less complex image.", "numTickets is incorrect! Please report this to Jynji, along with what you were doing before saving the ticket file.", "Select PNG format {} image", "title", "thumb", "Portable Network Graphics file", "Please select a ticket first!", "Are you sure you want to delete the ticket for \"{}\"? This can't be undone!", "Select ticket.dat", "iQue Player ticket files", "This file is not a valid ticket!\nTicket magic: {}", "This file's length is incorrect! To import a CMD or contentDesc file, please make a new ticket and use the 'Replace data' function.", "iQue Player content description files", "iQue Player content metadata files", "Select data to import", "Binary files", "The file you selected does not appear to be a contentDesc file or content metadata file! Continue to import {} bytes?", "The file you selected appears to be a complete ticket file! Import as ticket? (Selecting 'No' will cancel the import.)", "Is trial ticket:", "ID:", "Version {} of ticket.sys editor by Jynji. Watch this space!\nCurrent numTickets: {}\n\nChinese translation: tenyuhuang, SKSA\nFrench translation: MelonSpeedruns\nGerman translation: Mr_ZG, BY\nItalian translation: asper\nCroatian translation: LuLGuy9999", "Sort tickets", "English", "简体中文", "Language", "Français", "Deutsch", "Italiano", "Hrvatski", "繁體中文"],
		                
		                "zh-Hans": ["神游机程序数据库编辑器", "打开", "重新加载当前文件", "保存", "另存为", "退出", "文件", "新建信息表", "新建程序数据库", "导入ticket.dat", "编辑", "导入时覆盖密钥", "导入图片时使用更精准的颜色映射", "设置", "关于", "帮助", "信息表设置", "常规", "程序信息", "其他", "信息表数据", "标题：", "ISBN：", "未知数值 #1", "未知数值 #2", "导出信息表", "替换信息表数据", "删除信息表", "选择ticket.sys", "神游机系统文件", "所有文件", "这不是有效的ticket.sys！\n信息表#1的幻数：{}", "未填写", "幻数：", "缩略图文件大小：", "标题图片文件大小：", "缩略图：", "标题图片：", "允许调用的SK功能：", "程序编号：", "信息表ID：", None, "选择要保存的文件名", "{}的值“{}”无效！\n请输入长度为{}字节的16进制整数。", "图片文件大小有误！请将此问题反馈给Jynji，或者更换一张简单一些的图片。", "numTickets有误！请将此问题反馈给Jynji，描述一下错误产生之前您所做的操作。", "请选择一张PNG格式的{}", "标题图片", "缩略图", "PNG图片文件", "请先选择一张信息表！", "你确定要删除“{}”的信息表吗？本操作无法撤销！", "选择ticket.dat", "神游机程序信息表文件", "这不是一个有效的信息表！\n信息表幻数：{}", "文件大小有误！想要导入文件，请新建一个数据表并选择“替换数据”。", "神游机内容描述文件", "神游机内容元数据文件", "请选择要导入的数据", "二进制数据文件", "所选文件不像是描述文件或者元数据文件，依然要导入{}字节的数据吗？", "所选文件好像是一个完整的信息表，要作为信息表导入吗？\n（选择“否”将取消导入）", "是否为试玩版：", "ID：", "神游机程序数据库编辑器 by Jynji / 版本：{} / 静候佳音！\n当前数据库中有{}张信息表。\n\n中文版翻译：tenyuhuang、SKSA\n法语版翻译：MelonSpeedruns\n德语版翻译：Mr_ZG、BY\n意大利语翻译：asper\n克罗地亚语版翻译：LuLGuy9999", "重排信息表顺序", "English", "简体中文", "语言", "Français", "Deutsch", "Italiano", "Hrvatski", "繁體中文"],
		                
		                "zh-Hant": ["神遊機程序數據庫編輯器", "打開", "重新加載當前檔案", "保存", "另存為", "退出", "檔案", "新建信息表", "新建程序數據庫", "導入ticket.dat", "編輯", "導入時覆寫密鑰", "導入圖片時使用更精准的顏色映射", "設置", "關於", "幫助", "信息表設置", "常規", "程序信息", "其他", "信息表數據", "標題：", "ISBN：", "未知數值 #1", "未知數值 #2", "導出信息表", "替換信息表數據", "刪除信息表", "選擇ticket.sys", "神遊機系統檔案", "所有檔案", "這不是有效的ticket.sys！\n信息表#1的幻數：{}", "未填寫", "幻數：", "縮略圖檔案大小：", "標題圖片檔案大小：", "縮略圖：", "標題圖片：", "允許調用的SK功能：", "程序編號：", "信息表ID：", None, "選擇要保存的檔案名", "{}的值“{}”無效！\n請輸入長度為{}字節的16進制整數。", "圖片檔案大小有誤！請將此問題反饋給Jynji，或者更換一張簡單一些的圖片。", "numTickets有誤！請將此問題反饋給Jynji，描述一下錯誤產生之前您所做的操作。", "請選擇一張PNG格式的{}", "標題圖片", "縮略圖", "PNG圖片檔案", "請先選擇一張信息表！", "你確定要刪除“{}”的信息表嗎？本操作無法撤銷！", "選擇ticket.dat", "神遊機程序信息表檔案", "這不是一個有效的信息表！\n信息表幻數：{}", "檔案大小有誤！想要導入檔案，請新建一個數據表並選擇“替換數據”。", "神遊機內容描述檔案", "神遊機內容元數據檔案", "請選擇要導入的數據", "二進制數據檔案", "所選檔案不像是描述檔案或者元數據檔案，依然要導入{}字節的數據嗎？", "所選檔案好像是一個完整的信息表，要作為信息表導入嗎？\n（選擇“否”將取消導入）", "是否為試玩版：", "ID：", "神遊機程序數據庫編輯器 by Jynji / 版本：{} / 靜候佳音！\n當前數據庫中有{}張信息表。\n\n中文版翻譯：tenyuhuang、SKSA\n法語版翻譯：MelonSpeedruns\n德語版翻譯：Mr_ZG、BY\n義大利語翻譯：asper\n克羅地亞語版翻譯：LuLGuy9999", "重排信息表順序", "English", "简体中文", "語言", "Français", "Deutsch", "Italiano", "Hrvatski", "繁體中文"],
		                
		                "fr": ["Éditeur ticket.sys", "Ouvrir un fichier", "Recharger le fichier", "Sauvegarder", "Sauvegarder sous", "Quitter", "Fichier", "Nouveau Ticket", "Nouveau ticket.sys", "Importer un ticket.dat", "Modifier", "Remplacer les clés lors de l'importation", "Utilisez des couleurs plus précises", "Paramètres", "À propos", "Aide", "Options de Ticket", "Général", "Infos de l'app", "Divers.", "Données du Ticket", "Titre:", "ISBN:", "Valeur Inconnue #1:", "Valeur Inconnue #2:", "Exporter le Ticket", "Remplacer les données", "Supprimer le Ticket", "Sélectionner un Ticket.sys", "Fichiers système du iQue Player", "Tout les fichiers", "Ce fichier n'est pas un ticket.sys valide !\nTicket #1 magie: {}", "Aucun trouvé", "Magie:", "Longueur de l'image bannière:", "Longueur de l'image titre:", "Image bannière:", "Image titre:", "Appels SK autorisés:", "CID:", "ID du Ticket:", None, "Sélectionnez un fichier à remplacer.", "Valeur non valide pour {} {}\nVeuillez vous assurer qu'il s'agit d'une valeur longue de {} bytes.", "La longueur du titre ou de l'image de bannière est incorrecte! Merci de dire à Jynji que ce message est apparu ou d'essayer une image moins complexe.", "numTickets est incorrect! Signalez-le à Jynji, ainsi que ce que vous faisiez avant de sauvegarder le fichier de ticket.", "Sélectionez une image PNG {}", "titre", "bannière", "Fichier Portable Network Graphics", "Veuillez d'abord sélectionner un ticket!", "Êtes-vous sûr de vouloir supprimer le ticket pour \"{}\" ? Cela ne peut pas être annulé!", "Sélectionnez le ticket.dat", "Fichiers Ticket iQue Player", "Ce fichier n’est pas un ticket valide !\nTicket magie: {}", "La longueur de ce fichier est incorrecte! Pour importer un fichier CMD ou contentDesc, créez un nouveau ticket et utilisez la fonction \"Remplacer les données\".", "Fichiers de description du contenu du iQue Player", "Fichiers de métadonnées du contenu du iQue Player", "Sélectionnez les données à importer", "Fichiers binaires", "Le fichier que vous avez sélectionné ne semble pas être un fichier contentDesc ni un fichier de métadonnées ! Continuer à importer {} octets ?", "Le fichier que vous avez sélectionné semble être un fichier de ticket complet! Importer en tant que ticket? (Si vous sélectionnez 'Non', l'importation sera annulée.)", "Est un Ticket d'essai:", "ID:", "Version {} de l'éditeur de ticket.sys par Jynji. Surveillez cet endroit !\nNuméros actuels: {} \n\nTraduction en Français: tenyuhuang, SKSA\nTraduction en Français: MelonSpeedruns\nTraduction en Allemand: Mr_ZG, BY\nTraduction en Italien: asper\nTraduction en Croate: LuLGuy9999", "Trier les tickets", "English", "简体中文", "Langue", "Français", "Deutsch", "Italiano", "Hrvatski", "繁體中文"],
		                
		                "de": ["ticket.sys bearbeiten", "Datei öffnen", "Aktuelle Datei neu laden", "Speichern", "Speichern unter", "Beenden", "Datei", "Neues Ticket", "Neues Ticket.sys", "Ticket.sys importieren", "Bearbeiten", "Schlüssel beim Importieren überschreiben", "Genauere Farbzuordnung benutzen", "Optionen", "Über", "Hilfe", "Ticket-Optionen", "Allgemein", "App-Infos", "Diverses", "Ticket-Daten", "Titel:", "ISBN:", "Unbekannter Wert #1:", "Unbekannter Wert #2:", "Ticket exportieren", "Ticket Daten ersetzten", "Ticket löschen", "ticket.sys auswählen", "iQue Player Systemdateien", "Alle Dateien", "Diese Date ist kein gültiges ticket.sys!\nTicket #1 magic: {}", "Keine gefunden", "Magic:", "Größe des Vorschaubildes:", "Größe des Titelbildes:", "Vorschaubild:", "Titelbild:", "SK abrufen erlauben:", "CID:", "Ticket ID:", None, "Datei zum Speichern auswählen", "Ungültiger Wert für {} {}\nStelle sicher, dass sie ein {}-byte langer Hexadezimalwert ist!", "Titel- oder Vorschaulänge is falsch. Informiere Jynji hierüber oder wähle ein weniger komplexes Bild", "numTickets ist falsch! Informiere Jynji darüber was du getan hast, bevor du die Ticket Datei gespeichert hast.", "Wähle PNG format aus {} Bild", "Titel", "Vorschaubild", "PNG-Datei", "Wähle zuerst ein Ticket aus!", "Bist du sicher das du das Ticket für \"{}\" löschen willst? Dies kann nicht rückgängig gemacht werden!", "ticket.sys auswählen", "iQue Player Ticket-Dateien", "Diese Datei ist kein gültiges\n Ticket Magic: {}", "Diese Dateigröße ist falsch! Zum importieren einer CMD- oder contentDesc- Datei, bitte ein neues Ticket erstellen und die \"Datei ersetzen\"-Funktion verwenden.", "iQue Player Inhaltsbeschreibung", "iQue player Inhaltsmetadaten", "Wähle Datei zum importiern", "Binärdateien", "Die ausgewählte Datei ist scheinbar keine contentDesc oder Inhaltsmetadateien-Datei! Mit dem Importieren von {} bytes fortfahren?", "Die ausgewählte Datei sieht wie eine komplette Ticket-Datei aus! Als Ticket importieren? ('Nein' wird den Import abbrechen)", "Ist ein Test-Ticket", "ID:", "Version {} des ticket.sys Editor von Jynji. Achte auf diesen Bereich!\nAktuelle numTickets: {}\n\nChinesische Übersetzung: tenyuhuang, SKSA\nFranzösische Übersetzung: MelonSpeedruns\nDeutsche Übersetzung: Mr_ZG, BY\nItalienische Übersetzung: asper\nKroatische Übersetzung: LuLGuy9999", "Tickets sortieren", "English", "中文", "Sprache", "Français", "Deutsch", "Italiano", "Hrvatski", "繁體中文"],
		                
		                "it": ["Editor del ticket.sys", "Apri file", "Ricarica file corrente", "Salva", "Salva con nome", "Esci", "File", "Nuovo ticket", "Nuovo ticket.sys", "Importa ticket.dat", "Modifica", "Sovrascrivi le chiavi mentre si importa", "Utilizza color mapping accurato", "Opzioni", "Informazioni", "Aiuto", "Opzioni ticket", "Generale", "Info app", "Varie", "Dati ticket", "Titolo", "ISBN:", "Valore sconosciuto #1", "Valore sconosciuto #2", "Esporta ticket", "Sostituisci dati ticket", "Cancella ticket", "Seleziona ticket.sys", "Files di sistema iQue Player", "Tutti i files", "Questo non è un ticket.sys valido!\nTicket #1 magic: {}", "Non trovato", "Magic:", "Lunghezza immagine di anteprima:", "Lunghezza titolo immagine:", "Immagine di anteprima:", "Immagine titolo:", "Calls SK permesse:", "CID:", "Ticket ID:", None, "Seleziona file in cui salvare", "Valore non valido {} {}\nAssicurarsi che sia un valore hex intero lungo {}-byte", "Lunghezza immagine titolo o di anteprima non corretta! Informa Jynji della comparsa di questo messaggio oppure prova con una immagine meno complessa.", "numTickets non corretto! Informa Jynji di questo errore, assieme ad informazioni riguardo cosa stavi facendo prima di salvare il file ticket.", "Seleziona immagine {} in formato PNG", "titolo", "anteprima", "Portable Network Graphics file", "Si prega di selezionare prima un ticket", "Sicuro di voler cancellare il ticket per \"{}\"? Questa operazione non puo'essere annullata!", "Seleziona ticket.dat", "Ticket files iQue Player", "Questo non è un file ticket valido!\nTicket magic: {}", "La lunghezza del file non è corretta! Per importare un CMD o un file contentDesc, creare un nuovo ticket ed utilizzare la funzione \"Sostituisci dati\".", "Files descrizione contenuto iQue Player", "Files metadata contenuto iQue Player", "Seleziona dati da importare", "Files binari", "Il file selezionato non sembra essere un file contentDesc o metadata content! Continuare ad importare {} bytes?", "Il file selezionato sembra essere un file ticket completo! Importarlo come ticket? (Selezionando 'No' l'operazione di importazione verrà annullata.)", "E'un ticket dimostrativo:", "ID:", "ticket.sys editor versione {} by Jynji. Controlla questo spazio!\nCurrent numTickets: {}\n\nTraduzione Cinese: tenyuhuang, SKSA\nTraduzione Francese: MelonSpeedruns\nTraduzione Tedesca: Mr_ZG, BY\nTraduzione Italiana: asper\nTraduzione Croata: LuLGuy9999", "Ordina tickets", "English", "简体中文", "Lingua", "Français", "Deutsch", "Italiano", "Hrvatski", "繁體中文"],
		                
		                "hr": ["ticket.sys Urednik", "Otvori Datoteku", "Ponovno učitaj Datoteku", "Spremi", "Spremi na...", "Izađi", "Datoteka", "Novi Ticket", "Novi Ticket.sys", "Dodaj Ticket.sys", "Uredi", "Kljuć prepiši kod dodavanja", "Koristi točniji Kontrast Boja", "Opcije", "Vise Informacija", "Pomoć", "Ticket Opcije", "Generalno", "O Aplikaciji", "Misc", "Ticket-informacije", "Titel:", "ISBN:", "Nepoznata Jedinica #1", "Nepoznata Jedinica #2", "Exportiraj Ticket", "Zamjeni Ticket", "Izbriši Ticket", "Otvori ticket.sys", "iQue Player System Datoteke", "Sve Datoteke", "Ova Datoteka Nema vrijedni ticket.sys!\nTicket #1 magija: {}", "Nije Pronađeno", "Magija:", "Velicina Predgledne Slike:", "Velicina Titla:", "Pregled:", "Titelslika:", "Dopusti Dozivanje SK:", "CID:", "Ticket ID:", None, "Izaberi Datoteku za Spremanje", "Nevaljana Vrijednos za {} {}\nJeste li sigurni da {}-byte jedna duga Hex vrijednost", "Titel ili predgled dužina je kriva Informiraj Jynji Oko ove stavke ii uzmi manje kompliciranu Sliku", "numTicket je krivi! Informiraj Jynji oko šta ste napravili i što ste napravili prije nego ste spremili Ticket Datoteku", "Izaberi PNG format iz {} Slika", "Titel", "Palac ", "PNG-Datoteka", "Izaberi Prvo Tiket", "Je si li siguran da hoćes izbrisati \"{}\" ovo se ne može vise Upotrijebiti!", "izaberi ticket.sys", "iQue Player Ticket Datoteka", "Ova Datoteka ima jednu nevaljanu Velićinu\nTicketa Magija: {}", "Ova Velicina je Kriva! za importiranje jedne CMD ili contentDesc- Datotke i napravi novi Ticket ", "iQue Player opisanje", "iQue Player meta Datoteke", "Dodaj datoteku za imporitranje", "Binarske Datoteke", "Izabrana Datoteka nije contentDesc ili opisanjska-Datoteka sa importiranjem od {} byta nastaviti ?", "Izabrana Datoteka izgleda kao Dovršena Ticket-Datoteka svejedno inportirarj? ('Ne' Prekini Import)", "Jeli Jedan Test Ticket", "ID:", "Verzija {} Ticket.sys Urednika od Jynji. Pazi na ovaj teretorij!\nAktualni Broj Ticketa: {}\n\nKineski Prijevod: tenyuhuang, SKSA\nFrancuski Prijevod: MelonSpeedruns\nNjemački Prijevod: Mr_ZG, BY\nItalianski Prijevod: asper\nHrvatski Prijevod: LuLGuy9999", "Sortiraj Tikete", "English", "简体中文", "Jezik", "Français", "Deutsch", "Italiano", "Hrvatski", "繁體中文"]}

		self.langs = list(self.strings.keys())
		
		self.textvars = [StringVar() for i in self.strings["en"]]
		
		self.localappdata = getenv("localappdata")

		if not isdir("{}\\Programs\\ticket.sys editor".format(self.localappdata)):
			mkdir("{}\\Programs\\ticket.sys editor".format(self.localappdata))

		self.saveDataPath = "{}\\Programs\\ticket.sys editor\\config.json".format(self.localappdata)

		try:
			self.settings = load(open(self.saveDataPath))
			for i in ["lastFile", "overwriteKeys", "accColours", "lang"]:
				if i not in self.settings.keys():
					raise KeyError

		except:
			self.settings = {"lastFile": "", "overwriteKeys": True, "accColours": True, "lang": "en"}			
			self.changeSettings()

		self.lang = self.settings["lang"]
		
		for i, j in enumerate(self.strings[self.lang]):
			self.textvars[i].set(j)	

		self.srcPath = self.settings["lastFile"]

		self.tickets = Frame(self)
		self.tickets.pack(fill = BOTH, expand = 1)

		self.ticketListbox = Listbox(self.tickets)
		self.ticketListbox.pack(side = "left", fill = BOTH, expand = 1)
		self.ticketListbox.bind("<<ListboxSelect>>", self.populateOptions)

		self.menubar = Menu(self)		

		self.filemenu = Menu(self.menubar, tearoff = 0)
		self.filemenu.add_command(command = self.openFile, accelerator = "Ctrl+O")
		self.filemenu.add_command(command = self.reloadFile, accelerator = "Ctrl+R")
		self.filemenu.add_command(command = self.saveFile, state = "disabled", accelerator = "Ctrl+S")
		self.filemenu.add_command(command = self.saveFileAs, state = "disabled", accelerator = "Ctrl+Shift+S")
		self.filemenu.add_separator()
		self.filemenu.add_command(command = self.quit)
		self.menubar.add_cascade(menu = self.filemenu)
		
		self.bind_all("<Control-o>", self.openFile)		
		self.bind_all("<Control-r>", self.reloadFile)

		self.newmenu = Menu(self.menubar, tearoff = 0)
		self.newmenu.add_command(command = self.newTicket, state = "disabled", accelerator = "Ctrl+N")
		self.newmenu.add_command(command = self.newTicketSys, accelerator = "Ctrl+Shift+N")
		self.newmenu.add_separator()
		self.newmenu.add_command(command = self.importTicket, state = "disabled", accelerator = "Ctrl+I")
		self.newmenu.add_separator()
		self.newmenu.add_command(command = self.sortTickets, state = "disabled")		
		self.menubar.add_cascade(menu = self.newmenu)
		
		self.bind_all("<Control-Shift-N>", self.newTicketSys)						

		self.optionsVars = [BooleanVar(), BooleanVar()]

		self.optionsmenu = Menu(self.menubar, tearoff = 0)
		self.optionsmenu.add_checkbutton(variable = self.optionsVars[0], command = lambda: self.settingsChanged("overwriteKeys", self.optionsVars[0].get()))
		self.optionsmenu.add_checkbutton(variable = self.optionsVars[1], command = lambda: self.settingsChanged("accColours", self.optionsVars[1].get()))
		self.menubar.add_cascade(menu = self.optionsmenu)
		self.optionsVars[0].set(self.settings["overwriteKeys"])
		self.optionsVars[1].set(self.settings["accColours"])
		
		self.langButtonVar = StringVar()
		
		self.flags = [b"\x01W\x02\xa8\xfd\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x0b\x08\x02\x00\x00\x00\xf9\x80\x9an\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x01\xf9IDATx\xdab\x9c4s\x9f\x9a\x8d\xde\xe1C\xb7^\xbea``\xf8\xfb\xf7\xdf\xdf\x8a\x18\xdd+mS\xfe\xff\xfd\xab[\x9b_\xd0w\xf2\xffo\xa6\xaf\xdf~\xc8\xaar:]\xd8v\xdf'\x8cE\x88\x9f\xc7\xfd\xce>\xb7\xf4\xd0\xbb\x8f\xbf\x1e?\xff\xfc\xef\x7fFUE!5Cn\x86_?\xff+\ny\x9a\xc9\xfe\xfe\xf3\xd7F[\xd8\xf4\xd0L\x865]\x93\xb6^g\xdaw\xe7\xfb^\t\x17\xc6\xe5+T\x1e\x9c\x8c\xf5Wy\xfe\xfc'##\x03\xc3\xc5\xbb\x0c\x97\xee\x00\x19\x8f\xde\xfeOg\xbd\xa3wx\x05ci\xf3\x82\xb57;\x9bN0\x01\xdd\xf1\xf4\xf9\xfb\xfa7z\x8f\xfe*\xfdmn\xa8\xcc\xd4\x02\x8a0|\xff\xcc\xf0\xfd;\x90\xee\xbe?\x9d\xdb\xcd\xe6f`\x92\x93\xd7\x8a+7>\xfd\xf8\xf9\x93\xe1\xe6\xdd\xb7\xff\xfe\xfdG\x07\xa1\xa1\xff\xfd\xfc\xd0\xc4\x80\xca\xce\\{\xc9r\xb9e\x82\x9a\x117\xc3\xc5;\x0c\xbf\x7f3\xfc\xfa\x05%\x81\x92?\x7f\xfeqp\xf8\xff\xeb\xd7\xbf\xdf\xbf\xff\x01E\xfe\xfee\xd1\x90\xdey\xe6\x0b\x0e\x1blm\xff\x98Y@\xcc\x05\xe2\xbf\x7f\xff\xfe\xf9\xfb\xe7\xf7\x9f?'\xaf\xbe`Jk<\xda7\xefBt\xfa\xce\xab\xd7>0\xbc{\xfb+%\x01\xe8\xf4\xff_\xbf\x03m\x00y\x86\xe1\xff3g\xa7Csv\xc8\xc8\xcd\x8bL\xd9ln\xd7\xcc\xf4\xe3\xc7\x1fqa\xb6\xa53\xdd\xe5\xd7\xf4\x7f\x9c;/Y0\x1d\xa8\xea\xdf\xcf\x9f@\xc70\xfc\xffo\xed\xb0\\d\xef>S\xc6\x17\x17\\\x0f\xe9\x99\xca3\xfc\xfb\xc3\x14\x13\xab\x1a\xed\xaf\xf1\xa3\xa3\xf2\x92}l\xe37s!\x9e\xbf\xff\xff30jJ3jJ\x00\x1d#\xab.\x14\x13\xbf\xe6\xb0\xa6\xad\xe8\x9c9\x99\xa7\xeb\xb3\x13mY\x9e\xbf~;\xcd-m\xbd\xaa\xfd\xb9\xa5\x07\x7f\xff\xf9\xfe\xe7\xef\xdf\xc40\xd5m\xc7?\xfc\xff\xf3\xc7\xfd\xfa\x9b\x95\x1b\xf72\xfc\xfb\xbbz\xeb!\x119\xc1\xca\xee\xae[\x95\xd3\x01\x02\x0c\x00\r\xc4A\n\xe5K~\x81\x00\x00\x00\x00IEND\xaeB`\x82%\xea:\xcd", b'\x01\xd8\x01\'\xfe\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x0b\x08\x02\x00\x00\x00\xf9\x80\x9an\x00\x00\x00\x04gAMA\x00\x00\xaf\xc87\x05\x8a\xe9\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x01jIDATx\xdab\xbc\xce\xc0\xf0\x0f\x8c\x98\x18@@\xc0\x95\xe1\xd5n\x10\x03"\xf8\x07,\xf8\x07\x89\r\x10@,@\x96D}5o,\xc3\xe7\x15\xffX\x15\xff\xb1\x9b\xfe\x15x\xfa\xf7\xf3\x86?\x0c\xbf\xfe\xfc\xff\xf3\xe7\xff\xef\xdf\xff\xc0$\x84}m\xd3&\x80\x00\x02i\xe0\x8d\xfb\xcf,\xf6\x947\xee\xef\xdb\xaa\xbf\xff\xbe\xfdf3\xf9\xcb\xaa\xfe\xfb\xcb\xc6\xdf u\xbf\x80\xe4\xaf\x7f\xbf~\x01\xd9,\xb2\xb2@K\x00\x02\x08\xe4\x90/k\xfe\xff\xfb\xfc\xf7\xeb\xb6\xbf\x7f\x7f\xfcf\xe4\xfd\xfb\xff\xcf\xaf\xbf/AJ\xc1\xea~\x02I(\xfa\xfd\x1b\xa8\x01 \x80X@\xce\xfd\xf0\xf7u\xd1\x1f\x86\xff\x7f8M\xff\xb0\xa8\xfc\xfe~\xe4\xf7\xf7\xc3@\xd5\x08\xb3\xff\x83U\xff\x07k\x00\x08 \x90\x93\xfe\xfd\xfc\x0bq\xeb\xf7\x93\x7f\x188\x7f\x7f\xde\x00V\xf4\xfb7\xc4T\x06\x98\xf1@\x05@\r\x00\x01\x04\xd2\xf0\xff/\xc8\x7f\x0c\xbf\x7f\xfd\xfd\xf6\xe7\xd3:\x90\xc1\x10\xf7\xfc\x83\x9b\r\xd1\x00D\x0c\x0c\x00\x01\x04\xd6\x00\x11\x02\x86\x03\x92\x03\xd0U\x03M\x04\xdb\x00\x10@ \r@\x16\xc4\x89\xff\xc0\xce\x80\xaa\x80\xb9\x1bl\x160X\xff\xfe\xff\xfb\x17\xa8\x16 \x80X@\x91\xf2\xfb\x0f\xb3\xa4$P\x8e\t(\xfa\xe77\xd4xX\xf0\x83\xcc\xfe\xfb\xf7\xdf_\x90\x06\xa0b\x80\x00b<\x8e\x14\x91\xc8\x8c?H\x91\xfd\x0f\x86\x80a\n\x10`\x00:\xaes0\xd656\xbd\x00\x00\x00\x00IEND\xaeB`\x82\x1cW\xdbb', b'\x01!\x02\xde\xfd\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x0b\x08\x02\x00\x00\x00\xf9\x80\x9an\x00\x00\x00\x04gAMA\x00\x00\xaf\xc87\x05\x8a\xe9\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x01\xb3IDATx\xdab,\x9ez\x99\x01\x06\xfe\xfd\xf9\x97\xe7\xc7\xf7\xf7\xef\xdf\x9f?\x7f\x02\xc9?\x7f\xfe022*\xb9\x18\xfe\xfb\xc2\xf0\xe7\'\xc3\x1f\xa0\x02\x06\x06\x80\x00b\x01\xaa\x0b\xb4\x93\x02\x92\xff\xff\xfd\xff\xf7\xef\xbf\xa4$\xef\xff\xff\xffA\xdc\xff@\xee? \xc9\xda\xd2\xf7\xff\xcf\xef\x7f\xbf~\xfd\xff\xfd\xfbmE\x13@\x00\x8140\xfcg\xf8\xfc\xed\xf7\xdf\xbf \x15_\xbf~\xfd\x0f\x06@6\xd0x\xa0=|\xcf\x9e\xfc\xfb\xf5\xf3\xff\xaf\x9f\x0c\xc2"@K\x00\x02\x908\x069\x00\x800\x08K\xf8\xff\x83\xddt\xd5&\xde8\xb4@\x9c\xb1[z\xe0\xccM"-\xfa\x83\x1a\xbd\xa8b\xeb\xb4\x97\x9e\x00b\xf9\xf3\xe7\x1fP\xe9\xdf\xbf@\xf4\x1f\xc8\x04*\x02)\xfd\x07q\x0e\xc8m@\xd5@\xe3\xff\xfd\xfa\xcd\xf8\xeb\xd7/\x06\x06\x80\x00\x14\x8fA\x0e\x000\x08\xc20\xf8\xff\x07\xa3q\x83;\xa5\xd0\xd2^\x0c7\xc6\xf6\x91L\x18h\xbb3\xaa\x02\x8c\xfc\xa1\xdc\r|\x01\xc4\x02T\x0ft\xc9\xef\xbf@\xf2\x1fP\xe4?\x12\x00z\x00D\xfd\xfa\xf9\x17\xe8\xe3_\xbf\x99\xc06\x00\x04\x10\xcb\x8f_\x7f@\xae\xff\xf3\x0f\xa4\x07\x88\xffA]\x03T\ra\x83U\x03\xfd\xf0\x9b\x01\x18V\x0c\x0c\x00\x01\xc4\xf2\xe3\xc7\x1f\x90j\xa0=\x7f\xfe\x02I,\x00\xe8$\xa0\xd2\xdf\xbf\x19\xff\xfc\x05\x86\x12@\x00\xb1|\x03z\xe2\xcf?.Nf \xef\xcf\x1f&H\xf8@\xe2\x91\x11\x0c\x98\xc5%\x81\x861\x02\xfd\xf7\x17d\x03@\x00\xb1|\xfb\xf6\xa7m\xc1\xe5\x1f?~}\xfb\xf1\xe7\xcb\x8f_\xd2\x9c\x92@\xa7\xfe\x06\xf2\xff\x02\xdd\xf2\xeb\xc7\x8f\x1fz\x93\xe7\x03\xd5A\xa2\x19\x08\x00\x02\x0c\x00\xee\xad{f\x9b\x0cuD\x00\x00\x00\x00IEND\xaeB`\x82\x02\xb0\xf9\xd4', b'\x01!\x02\xde\xfd\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x0b\x08\x02\x00\x00\x00\xf9\x80\x9an\x00\x00\x00\x04gAMA\x00\x00\xaf\xc87\x05\x8a\xe9\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x01\xb3IDATx\xdab\xf4\xf1qf\xf8\xfb\x9d\xe1\xdf?\x06f\x96_\x7f\xfe\xfd\xfa\xfd\xe7\xff\xbf\xdf\x0c\x0c\xff\x18p\x00\x80\x00b\xf9\xfd\xfb{qq9\x90\xf5\x0f\x0c\xfe\xfe\xfd\xf3\xf7/\x84\xfc\x03\x05\xbf\x7f\xff\xf9\x0b\xa6~\xff^\xb7n5@\x00\xb1011\x01U\x9f8y\t$\x01\x16\xfe\x05\x04?A\x10\x0e~\xfc\xf8\x01\xc4\xfe\x01N@\x95\x00\x01\xc4"\xcb\xc0 \xf0\xef\x9f,X\xf5\x9f_\xbf@:~\xfe\x04"\xa0\xae\xdf?~\xfc\xfa\xf9\x03\xa8\xe1\xf7\xf7\x1f@\xfd\x12\x7f\x80Ne\x00\x08@b\x1c\xdc\x00\x00\x82@\x10\xe4\x81\x15\xd1\x8c\xfd7\xe1\x1d\x08h4\xd9LVg\xd02-\xa2\xdd\xfbK\xde\n,\xe2\rz\xb1\x1c#\xb6\x8a\x1c\x01\xc4\xf2\xff\xf7\xaf\xff\x7f\xff2\x00\xd5\xfd\xfa\xfd\x1f\xa8\xe2\xd7\xaf\x7fP\r`\xd5@\xf4\xfd;D?H%\x03\x03@\x00\xb1\x001\xc3\xdf?\x08\x83\x81\x8c\x1f?\x80\xaa\xa1\xda\x80\xaa\x7f\xfd\xfc\x0bT\r\x14\xff\xfb\xfb/\x03\x03@\x00\xb1\xfc\xb6b`P\xfb\xff\x9f\xf9\xdf\xff\xbf\xff\xfe\xfd\x06\xa2\xbf\x10\xc6\x7fP\xf0\x02I\x86\xbf\xbf\xff\x03\xc9\x7f@\xd2\x84\xf1\xc7a\x06\x80\x00b\xf9\xaf\xc7\xf0_\xe6\xdf\x7fA\xa0*\x10\xfa\x0f$\x81\x16\x82B\xf8\x0f$\x98\x81b`.\xc3\x7fa\xc6\x7f\xae\x0c\x00\x01\xc4\xc2\xf0\x8b\xe1?\xd0\xfb\xacFL\x0c\xbf\x18A\x1a\x80\xe4\x1f\x86\xff\xbf\xff\x83\xd8@\xf2\xcf\xff\xff@\x1d\x7f@\xb6\xfc\xfa\xc3\xf4\x95\x01 \x80X~\xbce\xd83o\xd2?\xa06f\x86\x9f\xdfA1\xfc\x9f\x8f\x81\xe9\x07\xc3?`@03\xfc\xfd\x05b\xb021\xfc\xfb\xc1\xc0\xc0\xcc\xf0\xed\x17\x03@\x80\x01\x00wt\x88\xc9\x18\xad_X\x00\x00\x00\x00IEND\xaeB`\x82}n\xfa\xd4', b'\xeb\x0c\xf0s\xe7\xe5\x92\xe2b``\xe0\xf5\xf4p\t\x02\xd2\x02@\xcc\xcd\xc1\x04$\x7f6\xcc\xca\x03R,\xe9\x8e\xbe\x8e\x0c\x0c\xebO\x98\xb3v\xbd\x04\xf2%K\\#J\x82\xf3\xd3J\xca\x13\x8bR\x19\x1cS\xf2\x93R\x15<s\x13\xd3S\x83R\x13S*\x0bO\xa6\xda000\x9ay\xba8\x86T\xdcJJ\x99q\xe2\xc0\x87fF\x96\x7f\x86\x06\x7f\x12+f}\xf9"\xaf5!(\xf4/\xfb\xb4\x16\x85\x06\x86\xa4\xc4\x1f\x87\x02\xdeF\xf1\x06\xf1\xb3\xfc\xff\xef\xe9\xe5\xf5\xef?\xff\x93\xbf\xff\xf9\x97\'%\xfd\xfb\xff\xef\xef\xff\xf3\xf2\n?S/\xab\x81\xd4%0v\xda\xff\xfc\xf5\xe5\xfd\xfe\xfd\x0e\r\x01\xec\xec\xdb\xf3\xff\xff\xff\xca\xbdbV`\x98X\x06\xb3\x03\xc3F\x86\xb5\x8c\xb3xB\xfe\xb2w\xfc\xfb\xe7\x16\xce\xcb\xe2p5\x81\x97g\x7f=\xb3)\x03\x8b\xc0\x89?\xfby\xea\xff3\xac\xfd\xc3\xee\xf4\xdf\x90q\x12\xdb\x82$\xa0y\x8cU"\x19\xdf\x80\x86\xfd\xff\xa3\xba\x84Q\xe3\xfc\x01\x06\x01\x07\x05\xde\xfa\x83i\xff\x7f}\xe7^\xc1\xde\xcf\xe6\xb6a2\x03S\x07\xe7\x8a\x87\xdf\xff\xdf\xdf\xff\xaf)\xe4\xff\xbf\xdf\xdc\xbb\xd96|t\x08\xff\x9f\x98\xc0\xc0\xa1\xb0a\xb2\x83W\xbd\xb3@\x19o}\x83T\x83\xdd_\xee/`G$\xbf\xfd\xbe\xdf~\xd2\x9dI\n\xf9\x7f~r\xf79\xb1\xb9\xb9\xb9\xb1Y\x04\x041i\xb2*/\x00\x997q\xe1\x94\xc6\x87\xc2\x1a}\x8e\x1f\xff6?\xcc\xb9\x1a\xb9\xe0\xec\x01\x8b\x96\t\x0e_\xb9\xbe}\x9b`\xd1\xc6\xd0\xc0\xc0\xcc\xa0\x17V\xde\x12x\xa8h>0\x98\x19<]\xfd\\\xd69%4\x01\x00\x19\xa9\xad@', b'\x01\x0c\x02\xf3\xfd\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x0b\x08\x02\x00\x00\x00\xf9\x80\x9an\x00\x00\x00\x04gAMA\x00\x00\xaf\xc87\x05\x8a\xe9\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReadyq\xc9e<\x00\x00\x01\x9eIDATx\xdab\xfc\xcf\x80\x00\xffP\xd9X\x11@\x00\xb1\x80$\xab\xab\x81\xc4\xff\x7f\xff\x18\x81\x14\x13\xd3\xff\x7f\xff\xff\xfd\xfd\xf3\xff\xef?\xa6\xdf\xbf\x98~\xff\xfe\xff\xe7\xcf\x7f\x18\xf9e\xe5J\x80\x00\x02k`\xf8\xff\xff\xc9S\x86\xbf\x7f\x81\x08(Z\x1a\xda\xf3G\xfe\xff\x9f;\xff\xff(\xfc\x9b\\\x91\xf8\xff\xf7\xaf\xff\xbf~\x01\xc5\x19ee\x816\x00\x04\x10\x13\xd8\xec\xffp\xd5\xbf\xff\xfe\xedZ\x94\xdd\xcb\xf1q\xc2\xdc\x94\xc9\x1c\x1f~\xff\xfe\tR\xfd\x0b\xaa\x07\xa8\x01 \x80\x80\xca\xfe\xfe\x03\x03 \xe3\xef\x9f\xbf\xdf\xbf\x7f\xff}\xe1\xc2/G\xc7\x9fg\xce\xfc03\xfb\xf4\xe9\xd3\xb7o\xdf\xbe~\xfd\xfa\xe5\xcb\x17 \xf9\xfc\xf9s\x80\x00\x82j\x00)\x06\x03\xa0\xf4/\x07\x07\x88\xea\xef\'N|\xf8\xf8\x11\xa2\xfa\xf3\xe7\xcf@\x1dO\x9f>\x05\x08 \x90\x06\x88\xea\xdf\x7f\x80\x0e\xfa\r\x94\x06\xa965\x05\xaa\xfe\xa6\xa5\xf5\xfe\xfd{\x88j\xa0U@\xc6\xe3\xc7\x8f\x01\x02\x88\x91!\xfcp{\xbc\xd2\xd3\x0f?\x7f\xff\xfd\xff\xe7\xef\xbf\xdf\x7f\xff}~|c\xd9\xfa:\xa0\x8b}\xbc\xea\xd9$5\x80"\x7f\xfe\xfd\xfb\xf3\xf7\xbf\xac \xfb\x8a\xac\x03\x00\x01\xc4\xc2\xf0\xeb\x0f\x90\xff\x1b\xa4\x14\xaa\x81YL5*e\x19\x90\xc1\n\xe6\xfe\xfe\xf3\xef\xcf\x7f\xa0\x140\x9c\x81q\xf6\x0f \x80\x80\x1a\x80\x06\xfc\x17\xe1a\x05\xaa\x06z\x07\x18\x10@\x12$\rb\x83\xc8\xbf`\xd5\xff\x80$X\x03@\x0012\xb8\xeed\xf8\xf3\x8f\xe1\xc7\x1f\xa0U@\xcd \xf2\x07\x8c\x01D\x7f\xc0\xec\xbf\xf0\x88f\x00\x080\x008\x9dv%3%&\x05\x00\x00\x00\x00IEND\xaeB`\x82@\x0e\xfdF']
		
		self.flagVars = []
		for i in self.flags:
			dec = decompress(i, -15)
			fileObj = BytesIO(dec)
			temp = imageopen(fileObj)
			self.flagVars.append(PhotoImage(temp))
		
		self.langmenu = Menu(self.menubar, tearoff = 0)
		self.langmenu.add_radiobutton(variable = self.langButtonVar, command = self.langButtonClicked, value = "en", accelerator = "Ctrl+L", image = self.flagVars[0], compound = "left")
		self.langmenu.add_radiobutton(variable = self.langButtonVar, command = self.langButtonClicked, value = "zh-Hans", accelerator = "Ctrl+L", image = self.flagVars[1], compound = "left")
		self.langmenu.add_radiobutton(variable = self.langButtonVar, command = self.langButtonClicked, value = "zh-Hant", accelerator = "Ctrl+L", image = self.flagVars[1], compound = "left")
		self.langmenu.add_radiobutton(variable = self.langButtonVar, command = self.langButtonClicked, value = "fr", accelerator = "Ctrl+L", image = self.flagVars[2], compound = "left")
		self.langmenu.add_radiobutton(variable = self.langButtonVar, command = self.langButtonClicked, value = "de", accelerator = "Ctrl+L", image = self.flagVars[3], compound = "left")
		self.langmenu.add_radiobutton(variable = self.langButtonVar, command = self.langButtonClicked, value = "it", accelerator = "Ctrl+L", image = self.flagVars[4], compound = "left")		
		self.langmenu.add_radiobutton(variable = self.langButtonVar, command = self.langButtonClicked, value = "hr", accelerator = "Ctrl+L", image = self.flagVars[5], compound = "left")		
		self.menubar.add_cascade(menu = self.langmenu)
		self.langButtonVar.set(self.lang)
		
		self.bind_all("<Control-l>", self.langButtonClicked)		

		self.helpmenu = Menu(self.menubar, tearoff = 0)
		self.helpmenu.add_command(command = self.displayAbout)
		self.menubar.add_cascade(menu = self.helpmenu)

		self.config(menu = self.menubar)		

		self.tikBinData = []
		self.savePath = None
		self.numTickets = None
		self.lastTikIndex = None
		self.curImagesBytes = []
		self.tikNamesUnicode = []

		self.editor = LabelFrame(self.tickets)
		self.editor.pack(side = "right", fill = BOTH, expand = 1)

		self.nb = Notebook(self.editor)
		self.nb.pack(fill = BOTH, expand = 1)

		self.general = LabelFrame(self.nb)
		self.nb.add(self.general)

		self.appInfo = LabelFrame(self.nb)
		self.nb.add(self.appInfo, state = "disabled")

		self.misc = LabelFrame(self.nb)
		self.nb.add(self.misc, state = "disabled")

		self.ticket = LabelFrame(self.nb)
		self.nb.add(self.ticket, state = "disabled")

		self.titleBox = LabelledEntry(self.general, textvariable = self.textvars[21], isHex = False, length = None, state = "readonly")
		self.titleBox.pack()

		self.ISBNBox = LabelledEntry(self.general, textvariable = self.textvars[22], isHex = False, length = None, state = "readonly")
		self.ISBNBox.pack()

		self.otherValue1 = LabelledEntry(self.general, textvariable = self.textvars[23], isHex = False, length = None, state = "readonly")
		self.otherValue1.pack()

		self.otherValue2 = LabelledEntry(self.general, textvariable = self.textvars[24], isHex = False, length = None, state = "readonly")
		self.otherValue2.pack()	

		self.miscLeft = Frame(self.misc)
		self.miscLeft.pack(side = "left")

		self.miscRight = Frame(self.misc)
		self.miscRight.pack(side = "right")

		self.exportTikButton = Button(self.general, textvariable = self.textvars[25], command = self.exportTicket, state = "disabled")
		self.exportTikButton.pack()

		self.replaceTikDataButton = Button(self.general, textvariable = self.textvars[26], command = self.replaceTikData, state = "disabled")
		self.replaceTikDataButton.pack()

		self.delTikButton = Button(self.general, textvariable = self.textvars[27], fg = "#FF0000", command = self.deleteTicket, state = "disabled")
		self.delTikButton.pack()
		
		self.ticketSplitOffsets = [0x00, 0x04, 0x08, 0x0C,
		                           0x10, 0x14, 0x18, 0x1C,
		                           0x20, 0x24, 0x28, 0x2C,
		                           0x30, 0x34, 0x38, 0x3C,
		                           0x40, 0x43, 0x44, 0x46,
		                           0x48, None, None, 0x2800,
		                           0x2804, 0x2808, 0x280C, 0x2810,
		                           0x2814, 0x2824, 0x2838, 0x2848,
		                           0x284C, 0x2850, 0x2854, 0x2858,
		                           0x2898, 0x289C, 0x28AC, 0x29AC,
		                           0x29B0, 0x29B2, 0x29B4, 0x29B6,
		                           0x29B8, 0x29BC, 0x29CC, 0x2A0C,
		                           0x2A4C, 0x2B4C]

		self.ticketSplitNames = {"en": ["EEPROM RDRAM location:", "EEPROM size:", "Flash RDRAM location:", "Flash size:", "SRAM RDRAM location:", "SRAM size:", "Controller Pak 0 RDRAM location:", "Controller Pak 1 RDRAM location:", "Controller Pak 2 RDRAM location:", "Controller Pak 3 RDRAM location:", "Controller Pak size:", "osRomBase:", "osTvType:", "osMemSize:", "Unknown value #3:", "Unknown value #4:", "Magic:", "Number of .u0x files:", None, None, "Thumb image:", "Title image:", None, "Padding:", "Certificate Authority CRL version:", "Content Protection CRL version:", "Size:", "Unknown value #5:", "Titlekey IV:", "SHA-1 hash of plaintext:", "Content IV:", "Exec flags:", "Hardware access rights:", None, "CMD BBID:", "CMD certificate:", "CID:", "Titlekey:", "Signature:", "Ticket BBID:", "Ticket ID:", "Type of trial:", "Minutes or launches for trial:", "Padding:", "Ticket CRL version:", "Titlekey IV 2:", "ECC public key:", "Ticket certificate:", "Signature:"],
		                         
		                         "zh-Hans": ["EEPROM RDRAM位置：", "EEPROM大小：", "Flash RDRAM位置：", "Flash大小：", "SRAM RDRAM位置：", "SRAM大小：", "Controller Pak 0 RDRAM位置：", "Controller Pak 1 RDRAM位置：", "Controller Pak 2 RDRAM位置：", "Controller Pak 3 RDRAM位置：", "Controller Pak大小：", "osRomBase：", "osTvType：", "osMemSize：", "未知数值 #3：", "未知数值 #4：", "幻数：", ".u0x文件的个数：", None, None, "缩略图：", "标题图片：", None, "填充：", "证书颁发机构CRL版本：", "内容保护CRL版本：", "应用程序大小：", "未知数值 #5：", "Titlekey IV：", "明文数据的SHA-1：", "内容IV：", "执行参数：", "硬件访问权限：", None, "内容元数据BBID：", "内容元数据证书：", "程序编号：", "Titlekey：", "签名：", "信息表BBID：", "信息表ID：", "试玩类型：", "试玩版总共可用的分钟数/次数：", "填充：", "信息表CRL版本：", "Titlekey IV 2：", "ECC公钥：", "信息表证书：", "签名："],
		                         
		                         "zh-Hant": ["EEPROM RDRAM位置：", "EEPROM大小：", "Flash RDRAM位置：", "Flash大小：", "SRAM RDRAM位置：", "SRAM大小：", "Controller Pak 0 RDRAM位置：", "Controller Pak 1 RDRAM位置：", "Controller Pak 2 RDRAM位置：", "Controller Pak 3 RDRAM位置：", "Controller Pak大小：", "osRomBase：", "osTvType：", "osMemSize：", "未知數值 #3：", "未知數值 #4：", "幻數：", ".u0x文件的個數：", None, None, "縮略圖：", "標題圖片：", None, "填充：", "證書頒發機構CRL版本：", "內容保護CRL版本：", "應用程序大小：", "未知數值 #5：", "Titlekey IV：", "明文數據的SHA-1：", "內容IV：", "執行參數：", "硬件訪問權限：", None, "內容元數據BBID：", "內容元數據證書：", "程序編號：", "Titlekey：", "簽名：", "信息表BBID：", "信息表ID：", "試玩類型：", "試玩版總共可用的分鐘數/次數：", "填充：", "信息表CRL版本：", "Titlekey IV 2：", "ECC公鑰：", "信息表證書：", "簽名："],
		                         
		                         "fr": ["EEPROM RDRAM location:", "EEPROM size:",  "Flash RDRAM location:", "Flash size:",  "SRAM RDRAM location:", "SRAM size:",  "Controller Pak 0 RDRAM location:",  "Controller Pak 1 RDRAM location:",  "Controller Pak 2 RDRAM location:",  "Controller Pak 3 RDRAM location:",  "Controller Pak size:", "osRomBase:",  "osTvType:", "osMemSize:",  "Unknown value #3:", "Unknown value #4:",  "Magic:", "Number of .u0x files:",  None, None,  "Thumb image:", "Title image:", None,  "Padding:", "Certificate Authority CRL version:",  "Content Protection CRL version:", "Size:",  "Unknown value #5:", "Titlekey IV:",  "SHA-1 hash of plaintext:", "Content IV:",  "Exec flags:", "Hardware access rights:",  None, "CMD BBID:", "CMD certificate:",  "CID:", "Titlekey:", "Signature:", "Ticket BBID:",  "Ticket ID:", "Type of trial:",  "Minutes or launches for trial:", "Padding:",  "Ticket CRL version:", "Titlekey IV 2:",  "ECC public key:", "Ticket certificate:", "Signature:"],
		                         
		                         "de": ["Position EEPROM RDRAM:", "Größe EEPROM:", "Position Flash RDRAM:", "Größe Flash:", "Position SRAM RDRAM", "Größe SRAM:", "Position Controller Pak 0 RDRAM:", "Position Controller Pak 1 RDRAM:", "Position Controller Pak 2 RDRAM:", "Position Controller Pak 3 RDRAM:", "Größe Controller Pak:", "osRomBase:", "osTvType:", "osMemSize:", "Unbekannter Wert #3:", "Unbekannter Wert #4:", "Magic:", "Anzahl der .u0x Dateien:", "None", "None", "Vorschaubild", "Titelbild:", "None", "Padding:", "CRL Autorität Zertifikat:", "CRL Sicherheits Version:", "Größe:", "Unbekannter Wert #5:", "Titlekey IV:", "SHA-1 hash:", "Content IV:", "Exec flags:", "Hardware Zugriffsrechte:", "None", "CMD BBID:", "BBID Zertifikat:", "CID:", "Titlekey:", "Signatur:", "Ticket BBID:", "Ticket ID:", "Typ von Demo:", "Minuten oder Starts für Demo:", "Padding:", "Ticket CRL version:", "Titlekey IV 2:", "ECC Offizieller Schlüssel:", "Ticket Zertifikat:", "Signatur:"],
		                         
		                         "it": ["Locazione EEPROM RDRAM:", "Dimensione EEPROM:", "Locazione flash RDRAM:", "Dimensione flash:", "Locazione SRAM RDRAM:", "Dimensione SRAM:", "Locazione Controller Pak 0 RDRAM:", "Locazione Controller Pak 1 RDRAM:", "Locazione Controller Pak 2 RDRAM:", "Locazione Controller Pak 3 RDRAM:", "Dimensione controller Pak:", "osRomBase:", "osTvType:", "osMemSize:", "Valore sconosciuto #3:", "Valore sconosciuto #4:", "Magic:", "Numero dei files .u0x:", "None", "None", "Immagine anteprima", "Immagine titolo", "None", "Riempimento (padding):", "Versione Certificate Authority CRL:", "Versione Content Protection CRL:", "Dimensione:", "Valore sconosciuto #5:", "Titlekey IV:", "Hash SHA-1 del testo non criptato:", "Content IV:", "Flags Exec:", "Permessi hardware:", "None", "CMD BBID:", "Certificato BBID:", "CID:", "Titlekey:", "Firma:", "Ticket BBID:", "Ticket ID:", "Tipo di versione dimostrativa:", "Minuti o numero avvii per la versione dimostrativa:", "Riempimendo (padding):", "Versione ticket CRL:", "Titlekey IV 2:", "Chiave pubblica ECC:", "Certificato ticket:", "Firma:"],
		                     
		                         "hr": ["EEPROM RDRAM Lokacija:", "Veličina EEPROMa:", "flash RDRAM Lokacija:", "Veličina flasha:", "SRAM RDRAM Lokacija:", "Veličina SRAMa:", "Lokacija Kontroller Paketa 0 RDRAM:", "Lokacija Kontroller Paketa 1 RDRAM:", "Lokacija Kontroller Paketa 2 RDRAM:", "Lokacija Kontroller Paketa 3 RDRAM:", "Velicina Kontroller paketa:", "osRomBase:", "osTvType:", "osMemSize:", "Nepoznata Jedinica #3:", "Nepoznata Jedinica #4:", "Magija:", "Količina .u0x datoteka:", "None", "None", "Predvidna Slika:", "Titel Slika:", "None", "Od (U tjeku):", "CRL Certifikat:", "CRL Sigurnosna Verzija:", "Veličina:", "Nepoznata Količina #5:", "Titlekey IV:", "SHA-1 hash:", "Content IV:", "Exec Zastava:", "system dozvole:", "None", "CMD BBID:", "BBID certifikat:", "CID:", "Titlekey:", "Licenca:", "Tiket BBID:", "Tiket ID:", "Tip od Demo-a:", "Minute ili Startovi od Demonstracije:", "Od (U tjeku):", "CRL Ticket Verzija:", "Titlekey IV 2:", "ECC Javni Kljuć:", "Zertifikat Tiketa:", "Licenca:"]}
		
		self.splitnamevars = [StringVar() for i in self.ticketSplitNames["en"]]		

		self.skCalls = ["skGetId",
		                "skLaunchSetup",
		                "skLaunch",
		                "skRecryptListValid",
		                "skRecryptBegin",
		                "skRecryptData",
		                "skRecryptComputeState",
		                "skRecryptEnd",
		                "skSignHash",
		                "skVerifyHash",
		                "skGetConsumption",
		                "skAdvanceTicketWindow",
		                "skSetLimit",
		                "skExit",
		                "skKeepAlive"]

		self.defaultTik = bytearray(b'\xed\xdaWP\x13\xda\xba\x07\xf0\x84\xb2U\xc4M\x0f\xa1J\x00\x01\xa5H\xa8\x86\x1eJ@A\x10\x02\x04$(\xa1\x85\xdeB\x15\x08D\x11\x90\x12\x8a\x80t\x04\x14T\xa4\x13\xa9\x12\x9a\x11\x90"\xa8\xa8\x80\xe0\x06\x04)!4CU\xce>\xf7\xdc\xb9\xf7<\xdc\x07\xe7\xbe\x9e\xfc^\xd6\xf7\xadYk\xe6\x9b\xf9?\xad\x99\x15\x1b\x05\xf8\x1b\x13\xe0w\xd4\xfdk\x01\x02\xf4\xfew\xcf\x00~\x15\xc0\n;\xa1Zd\xafI\x9c\xd3\xe3\xd5b\x86\x00\xc7\x93|\xd2\xd3%\x98\xe4\xb8\xf6\xc18\x96\xdb\\0T`\x1f\xb0\x05\x88\x82L\xc6\xa6\xf3\x0c\x99[*\xac\xbc\x0c-p\x0b+\xbe\xf5\xc5o\xca\xd1\x916\xb53\x02jL8:8\x13\xb1t\xd0P\x84_\xbc\xe0`ti\xeaxp\xadO\x8d<l\xeev\xda\xeaa\xb4\xca<\xbdys\xaf\xf0\xa4%\xa2\xff\x14U\xdb3a\xf5\x88R\xf1+H\x9b\xdcji\x8bM;\x05\xad\xa9\x97\x12\\"\xc9\xcf8\xd4\xb8\x9c\xb5j\xcfI\xacmi\xca\x8e,\rPS\rt\xf6\x16\xba!ox\x84\xf2}a\xd1\xa4&\xc6\x16\x1d\x12\xcfy\xf5;\x17U\x1bO\x8de\xd9?\x9a\x1b\xa2\xc6\x0e\xd3\xa1;S\x15\xde\x89\xe0\xa9\xc8\xa325X\xa4!\x88\xa9\x16M(\x16\x18c\xaa\xbd\xf5\xaa\x962,\x1cA\x8dw/\xee\x1a\x14\x9em\xbey\xe6i\xb4xV\xe270Wy\xda\x85\x83\xca\xb7C\xe7\xd4\xef\x1d|qA\xf7\xb7<0$&\xbe\x12$\xbfXV\xdf8\x05Y\xa7=\xa0\x86\xec\xfeL\r\xfd<\x977\x16$\x0b\xc3\x12\xc7t\xb3\xa5c\x03\xbf`\xdc\xf1\xc7\xfb!Z\x9c\xa7sW\xa8\xb4CMh\x88H\xedC\xa1p\x84f\xd2\xcd\xf7\xdf\x7f\xfd\xfa\xb9\xa7)\x1a\x1b\xa6\xf5\xf0\xa2\xf9a$\xb9\xfbgH\x98\x16@\xb9\xfc\x03\xcc\x98823\x143\x97 P\xafQ\xe6\xf8b\x01\x1e\xf7\xc66\xb1\x87w\x0b\\\xf4\x82\xcfy\xca\x10?.C\x19\x18\xee_@\x94\xe2\xeb\x93\x12A\xad\x83\xc9\x0b0\xeaWU\xba\xc5\x16\x12\xa1/\xfc\x97o\xa3\x84\xe0\xde\xc3{\x182\xd0\xb8!xt\x88\x98\xd0\xcf\xa1$\xa6`m\x9f{LLx\x03\x92i\xca\xf6\x956\xacaN\xe4M\xa1\x0b\xd1\xbb\xf3C\x17\xa3\xc9PQ9\xbbI\xff\xd6\xc5\x95\xbfJ\xd6~\x08yg\xf6\x84\xecq\xf8;\xe1k\xe0j\x94\xfc\xa7%\x99g\xd7\x12\x0e\x0c\xfb~:\xda*\xebF$s\xc2\xd4w\xba\xaa\xa8l\xf8\xbd?\x0f\x96\x05ufg\xef\x9dd\xdf\xc6]]tp4\xd0\xf2\x94\xd9\x92\xb8A\xae\xff\xe3\x91\xdb\xc6\xfd\x90\xe1\x80\x10\xd0\xdc\x8a\xd9\xe1\xa933\xb7\x9b\xbbF\x95\rU\x96yBy\x14\xa8W\xf0\x83\x1c\r\xd2\xbeO\x9e\xa8\xebb\x03k\xd8t\x9cG\xa5\xff\xdcl\xf2\xdad\x8e\xdf+\xa5\xe5f\x93\x11g\xbf\x89B\xd7\x03\xea\xf0u^\x05\xb9W\x17\n\xdeK\x95\xc3\x0fR\x8e\\\x8f\xe7\t\x02gF3\xd5\xce:\xab8\x08\xc8\xe2\x9e\xa7\x8e\r\xf1\xce\xe3\x91\xda\x1e\x00\xff]\xa1)\x8bMc\xfc\xdb\xfa9\xa0\xacdYSR\x9e\xb5D\xc3R]\xe8\xf74vUb\xb8\xc9dT\xe2\xae\xe0\x8el\xa2\xb8\xe3\xa5$\xb5\xb2\xcdAl.\xdf\xc1\x02*E\x8f\xa84sW\x1a_wv\xac\x1f\xfd\xc1*\xef\xfc\xa2\xe7H\x92f\xbd\xabT\x15\x96V8,\x1c\xd3\x92\x06\xcbll\xa1\xc0\xfc\xaf#)\x05\x08\x03\x9ed\xe1\x98$\xda\xd1\xd2\x85.\xb9\x81O\x85\x08\xa4\x02w3:\x10wD(U\x12\xb5\x95\xd2\x81Mz[\xcdW\x1e\xac\xfb\x88P\xa5\xd3J\x8d=\xdc\xa0.\x0eoT%\xb7\xb93\xc7\xfa\xe4?\xea*\xf1\x8a\xceP\xb4\x06=j\xc3\xb3\'\x1f\r{O\xa6\x1c\x81c\x16\xf9wy\xe6\x10\x1c\t\xb5\xa7S\xf1\xa3\xecq\xfd\xdd\xc8\xa37:.\xee\xad\xf1\xfezm\x15\x14\x0ez\xef\x01o\xf3\x90<\xb4l\xc0\xfeG\xaf\xff\xc0\xfc\xd7\xcf3K\xb1\x90h\x9fOP\xf98\x13\xad\xbdb\x17\xb4\xa8\xa02h[h=Od_\n\xc7\xacm6a,\x7f{q#u\xb7D\xdf\xa1\x86\x8fu\xda\xfbz\x011\xdc\x93\xbb\xcdv-\x19\xb2VQ<W\x15\xb9\x96\xa0H\x9f\xde\x04\x1d\xd9\xd5>\xb7PN\xd9|\x82\xa6j\x9c\x90\x1f\xac,\x0f\xbb\xf8\xd1\xce\xe1\xa3\xd9&R\xe7A\x8c\x12\x93\'\x97\xcdM\xaa\xa50\xce\xee\xec\xde\xd8\xeb\xb7(w=V\xb2\x0f\xf4\xb8\xcb\x0f\x93\xc6%j\xa4\x01t\xd9.W\x17(\xda\xad\x93)OTeIi\x8f\x07\xc5\xfa\xce\xd3N\xa0$=c=\xa2J\x8e\xe2\xc4f\x7f\xac\xc7\xef\xdbT\x05\xdd\xe8\xd3\x9a$\xb9\xa9l\xce\x1f-V\x1e\x8c\xa0\xbb\xdbj?e\x85,\x0f\xd7A\xc6\x9a\x06W\x89\xaa\xb1\xca[\xcdT\x8b\xf9\x88\xd1\xf3X\x1f\xca\xf3\xb0\xac\\\t\x84\xcbbi.R\xad\xdc\xb7\xde\xcb\x83\xfdf)jkUp?\xb4\xc3\xcb\xff.x>w\x032\xc84]m\xa782\xdb\xb1-4\x97\x83\xbd\xda\xfby\xb2\x87\x9e\xdc\xae\x92\xd4\xd0.\x1b\xd0)\xa8\x99\xb6\x8ab\x8b\xd8\x0f\xae\xda\x19M\x91\xd1\xcc\t\xd1\xdd5\xedn\xa4G\xb8s\x8d\x8e]i\xaaoQ\xc36E\x9d\xcd\xd8\xe94\x8f\x8a\xcaTE<\xc7\r\xa1\x1d1\r\xc1\xa9\x94\x9d\xab:\xea\xa6t\xd9\xb7\x14\xb4c\xaf\xb3vAf\x94\x14F\xc8|\xbbJ\x828Vi\xcb=*\x89\x98D{\xa4\xd1u\x9c\x8b\xb6\xdf\xe7\x8d\'\xce\xf6\xd84k\x95g\xa7E\xb0\x92d\x1b\x03;\x96\xc2\xbc\xdc\x8e\xb8\xaa\xb5\xce\x88\x9a\xea\xf4\x86\xcc\xcfX=\x19s\xe7\x11t\xec\xc3\xf9R\xcb\xa3\xe8h\xcdSimO\x1c\xe7\xc38\xfc\x96\xfb\x8e\xee\xe5\xa6W\xdaf\xa0\x90\xe4\x8b\x0b\xfb\xba\xcc1\x00\x0f\x95\xa0T\x00\x80j\x7f\xdac\xc2\x86Wwr\x08\xb5\x92\xb5/C\xaa\x18f\x17\xd9\xe1\xca\xe6\xd6\xae\xa8\x91\xb9\x93[\xffD\xc6\'\x8b\xcb\xfd\xafr\xbe\xeb\xd6%\xe7\xac\x9eB!\rvcK\x0ern\x8bV\xfd}\xfeWs\xe8o?\x1bX\xa1\xfc\xf2\x95yV\x1b\xdf?\xce&\xe3\x97\xa6\x8f\xbd{\x9d\x1a]\xf1\xdfZ}\x8e#\xd7\xbdw\x7f\xad\xb7\x92q\xebE\x89\xc1\x19\x03\rV\x8b&\x84\xbd\xa0d\xc9\x05\x87\xcf\xb2\x0en\x0f\x84\xb3k]\x8bS\xd2\xdfe\x0b\x9f\xcf\t\x82\xc9\x9d\x1c\xc7\xac\xfc\xb4\x88\xec\x08~\xe0\xf3YD\xac>\xf1\x96\xc5\xf9d\'\x9e\x8a]\xd7\x80\xe4\xd7\nYW\xc81R[\x1d\xae\xb7>\x90\xc9\xe9*\x19\xa4\xdb\x0e\xf5L\x8dc6\x81-\xf6\xf4\xd3\n=\xec\xef\x9d8^8\xf3\x13\xbf\x9aj\xdd\xc1_\x0fC\xc77{,\xe8\'\xe0\xb8\x06\xd3\xf5e\xce\xf7\x057\t`=\xb4\xb1\xed\x0f/\xe2U\x85\x8bQ\xbcx\xce\x14\xb86\xa9\x12\nX*\xd5dK\x84\x05\x0084\xda}t\xe6\x04\x1a\x1c\xafq?D_}?o\x02\xde\x1aX\xb4\xdb\xb3qm\x1d8\xfa\xd2AV\xd5oS\x8ft\xaf\x96\xfd\x9e\xf6\x87\xc1\x82\x91\xc1\xce\x9f\x85N\x9db=\x92\xf6{C+\xc96S#$U\x0b\xc4\xc9\xd6\xde\xcb\x02\rw\xc6\xd8\x9e\xf7\xc9i!\x84j\xbf\xa69k\x8c\\\xea,D\xd7\xce/%hI\x9a~\xbfy\x10I\xda\xef\xfe\x0e\x95\xba\xc9\x16\x82\xadv\xd3\xe8\xd7\xe8v\xfc\x14\xc7\xdag\xd3/\x94\x90H\xd1/\x8a~9\xddO\xc2\x0e\x04u_k`\x0b\x18\x0f\xa4\x99-\x9f\x8b~T\xf0c\xd8\xd5\x9cd\xde\xed\xf12\x82\xc99\xa83\x9cN}+?\x8e\x9fr\xe5\xf3\x9d\x94\xeb\xb4\xfd\xa1\xf1\x81\xc9\xac\xf7\xe7\x17\xf3\xb5\xfda\x8ad\x85\xd9\x92\xcd\xca\x9d\xeb\t\xe1\xd9K\xcc\xefW\x05\xbd\xbf\xb5\xe6\xecW\xda\xcd~\x96\x82\x05\xc9\xa0\xa9\xa6\xf1\xa3&\xc3\xba\xc2MO8\x87\x1a\xb7\xd2\xca~\xe12\xe4\x88\x1e\xfe\x8d_<\x10\xb0\xce\x1b\x17\x1c\xcf\xa1\x02\x9f\xb9\x91\xb5^\x7f<\x12i\x0c\x9c\xab\xd1%IBC\xe4j\xcd\x90\x8b\x91\xc8\x17\x01sT\xf6]\xf9o\xb7\xce\xaf^\x1c+\x0e\xd5\x1f4\x98h\x98\\\xae\x8ew\xde\xfef\xd0\xdcC\xe8\xd7\x8b\\[\x18\xe2(k\xce\xd99u}Z\x16L\x9c\xb5\xdf\x96F\x94J#\xfd\x97\x1c\xc6Ra\x1f4\x9e\xd1+rvz\x14\xd1\x84\xd0g\x1f\x07\xc5\xe4-7\xc30\x99\xf5a=\x9e8\x11\xf3S\x06\xed\x93\xbd\x1fs\x8b\xdc\xea\xf2\xb3\xc8\xa8\xe9S\xb55\xfaT\xfb\xa9J\xb4\xab\xfd\x9a\x9d\xec7\xb0\xac\xc8\x9a\xd0\x03\x8c\xf8\x05\xd8|\'\xd8\xcc\x90p\xf1\xbb4l7\xbd\xb2\x9d\xad\xed\xe1\x88\xe2\xa5+\xb3\xb7\xd2\x0b\xb7\xf3K\x15\xf9_oH\x906+\x8a\xd2\xf2*\x08\x81\xc3\x1e\xf2\x9fK\x9f\x03\x12\xd8q\x97\x85J\xfb\xb0\x9c\xc5\x82\xf2y\x0b\xa5\x8e\x08!\xf3\xad\xe6\xf9\x87Y\xd0\xb89_-\x8c\xbc\xf6a\xcd\xce\xcb\xbaT\xe42\xbdge\xa2I<i\x98\xbf\x03\xd3\xa8\xdb-\x13\xd0\xf2\xedEY\xeaH\xa7\xef\xa3a\xc4_\xc4K%\x07q\xd1\xfcS^\xb8\r\xa2g\x9ar\t\xe1\xdb\x90v\xacN.\x85\xe6\xdf"JD\x159J\x89o:\xdd\xeb\r(\x00\x8f@\xabLY\xb0b\xef\x1a\xbd\x9aOoV\xe4\x9a\x87E\x82\x8b\x05\x9b\xcb={g\xca^\xb4\xe7\xe3\xfc\xc4fz}D"\xfby\n\xa3\xdd\x1f]m\xb5\x13\xfa*:\xb16\x1fFx\xb1\xa7\xa7\xd8\x17\xee\xaeD:\xdc\x8b\xfe\xd2\xebtb{U\xfb\x8f@P\xf5t\xfaC[\x10)\xf0\xcd*\xd1Z\xd3\xb1\x9co5\xe3\xab\xc2\xfb\xf8v\xc5/\x9b\x11\xd3\xfb&S%]\xb2\xe1\xd4\xd47\xef\x0c@l\xa2\xaa\x1d\x87\x7fq\x0bc\xd79\xd0O\xb7\xc9\n\xe3\x14\xcdC=\x1d{\x89\xae\xc8\xd2 \xcb;\x81\xb7\x9d\x98\xc9\xb2\x9b\xbc\xf3t\xcf\x94\x89\x10\xdeY\xda\xab\xf2\x1b\x13W\xac\xb8:B\xd0\xf33\xa8\xfd0\xad\x02\x8b\xf8\x1b6/\xbf\x89\xbf\x86\x12\xa7\\rdO\x86\xf6\x16q-RH\xa0X\xf9\xac\xf3\xfa\x87\xd6\x1d\'\x82&J>]\xa9\xd48^2\xc5\xc2\xa5\xa3^o\x95\xbce\xe6W\xe99\x0c\xea=\x84z\r\xd2J\xca\x84\xbd\xf3l\xd3\x1d@,\x1d\x05K\xcfG\x8d>j\xed\x9f\xf4\xe1\x81\xd4d\xd3\x1f\xdcnx\xd4\xabhRzv\xc3\xd8L \xd9U"\x113n\xc4\xd4\x81\xbbDK\xf0!\xdd|\x97\xd4\x1a\xef\xdd\x01\xe2\x893+\xef\xb0\x1c\x1c\x17\x8d\xb9\xb3{\x03_\xe2\x13\x97Q\xf1uz5\x12\xd5I\xf1\xbb\x9f\xffI\xbd,\xe3.j\xd1\xd9\xd0\xb7\xba\x83\xfb\xf4Z\x8b\xd8\xc6\t\xa2\xcd\x95\xb5&\xb0\xa6\xbc\x97\xea\xd1\xf5\x0b\xf7E\xfe8\xd3\x92\xb5\xed\x97\x96\xe6\xfb\nY8\xcc;\xe8\x94\xf7\xa4\xcaa\xb0\x81\x16\xc1\xf3c\xb3\xb8\xf6\xc7i\x16~\xa1\x99\xb4k\xef\xf0\x87>\xec\x0f\x10z\x129]\xb56-B.\xc5\x11\xbd\xe1,4W\x8f/\xc0\x99N\xdf\xa5\x08\xdb\xe7\xfb\xdc\xde\x0e"\x85g\xf8\x07*\x8f&\xeeV\'aL]\xc9\x8a\xa2,yS3\x8f\xc0<\xeb\xa5\xa1\xec\xcdF\xcf\x83\xb5LW\xc0/=:\x99\xbd\x9e\xd8\xd8w\x8a\xb8\x7fzv\x13\xb3\xcc\xf2\xe6\xc3F\x8d\x06o\xd8\xb6\xbbu\xef\xc1\x08d\xe6\x9aT`s\xae"\xe8\xd4\xa7\xbe\x98\xf6g8\xe9\xb2\x1c\xd05\xd7\xa1\x8c-\x9a\xaah\xe7\xcc/\x1f\x14y9\xca?\xbf\xfe\xde\xf7\xc3\xf7~\x05\x11y\t\xdf9G)\xa6\x01\xaa?1:.\x9d\xf7w\xe2\xdc[\x1d$!\xb9n$Yh\x81\x0f\xf9n\xc8\x05\xa1\x81U\x9ax\x16o\xcd\xdd\xeb\xe4\xa4\x19\x91\xfb\xc5\x1c\xec\xce\xf7\x031Q\xe2\x18I\xe3Q;^\x81\xc7\x93\xa5\xd5\xbb\xf4\x0b\xb3.\x91\xfe\xc9\xaf&\xc9\x89\x1e\xfc\x8f\xf8\x0b8iK\x89;V\x15\xbbP\xdb\xa5bk[\x01S-\x0efz(\x89\xa95\xf5R\xab\xc4\xe2\xdb[1\xdd\xee\xd3\x16g\x1d\xba\x8b\x91\xad\xb2\x83\xa2\xc8\x16\xe4\x89\xfe_\xb8\x97\xbbO\xfd\x0c5D\xe1u\x93\xe4Zo9\xcb\xa7\xe1\xe7\nI\x07aU\xc2\xb0\n\xb9\xb2\xc3\xfb\x01\xb5\n\xbfd\x07\xd8I\x1bJ\xa8\xc5\x1b\xa0dR\xf5\xe3[\x03^\xf2\x1b\xe6\x06\x82\x91-\x12J\xd7f\x82\xf6\xe1{\x94k\x07\x85\x9b\xce\n\n\x92\x16}\xc3\xca^+\x0b\xce\xc1\x15j\xf8\xd1"\x1d\xef&\xdcA\xfe\xc61\x885\xfe\xd6\xd0\xeem\xa27\x8e\xb9\xa3,\x03]\xb3;\xb14\x0eM\xe6.\xb2fuk\xbdq\xf9O\xea\xf5\xf2W\xc1\xfa\x0e\xaeY}n\xd9r.\xd7%\xde%\xbe\x18\xd4C\xc8\xaf\xee<\x0e}\x89\xcd\x93\xdeh|\xb5X\x1e\xfc\xca%\xcb&W\xed\x8dp\xdek\x9aR\xde\x05\xf5\xcb\'(\xca\x8d\xae\xf7?d\r\x16\xa9\x8d\\\xca\x1b\x9d\xba\xb2\xd7\xd6\x9c\xbaw\x97\xc6\x02\xb3\x9dU\xf1\x1b\xa9\x1bg\xab\x1a\xf0\xb4F\x0eE\x80\xd4\xcf\x1f\xd2L4\xed\xabE7\xed\xc5\xa9\xc9?G1\tM\xfc\xa9\x03?\x0f\xb1SR?\xdb\xa6\xbc}\xac\x1bZ\x0c\xde=\x96\xd9r\x8e67\x97\x7f\xec\x95\xcd\x1c\xee=\xdd\xb5\xb7\xe0ft\x18\x1e\x90?:\x90\x97\x9eqp<l\xd2\xf6\x92$\xbd\xa3\x9b.\xb4\xc0\x8a\x90\x0fi\xd8\x13\x9e<F\xffbzj\x05\x88\x07\x00\xcc\xdd\xc2\xc4\x82=]\xbc\xdd\x82\x01\x97-m\x8c\xf4\xad\x8cPbJ\x8aP\xd8o=c\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\x18\xfe\x13\x00\x01\xff\xfe\xb1\xef\xdfX[X\xc3\xcd\xcc\xec\xcd\x8c\x8c/[#M\xe0P\x138\xd2\xe4\xff8\xc6t\xfc7\x00 \xe6\xf8\x9f\x8d\x95\xbf\x7f\xb0\xbc\xc15\x03\xb8\xe2?A\x15/\xfd\xdd\xfc\xab\x84*\xfe\xd64\xed]3\xd2\x93_\x83YK3)j\x9cm\xe2\x88\x95Q4P\xc2\x08{\x8f\x93\x8b\x9b\x87\x97\x0f\xc4\x0f\x16\x10\x83\x88KH\x9e\x93\x92\x969\xaf\x08URVQUS\xbf\x04\xd3\x83\xeb\x1b\x18\x1a!\x8cM._\xb3\xb4BZ\xdb\xd8\xa2\xec\xec\x9d0\xce.\xaen\xeeX\x0f\xcf\x80\xc0 \\pHhXxD,\xe1\xf6\x9d\xb8\xbb\xf1\t\x89\xf7\xd232\xefge\xe7<\xc8\xcd\xe3\x04\x029!\xcc\x9cpVN\xcc\tN\xc2). \x17\x17\x84\x87\x0b\xce\xc7\x85\xe1\xe7"\x08p\x03!\xdc\x10\tn\xf89n\x8c47\xe1<\x0f\x10\xca\x03Q\xe6\x81\xab\xf2`\xd4y\x080^ \x9c\x17b\xc0\x0b7\xe2\xc5\x18\xf3\x12.\xf3\x01-\xf9 H>\xb8\r\x1f\x06\xc5G\xb0\x07\x011 \x88\x0b\x08\xee\x06\xc2`A\x04O~` ?\x04\xc7\x0f\x0f\xe1\xc7\x84\xf1\x13"\xc0@\x02\x18r\x07\x0c\xbf\x0b\xc6$\x80\t\xf7\x04\x80\x19\x02\x90\xfb\x02\xf0l\x01\xcc\x03\x01B\x9e\x18\x13PL\x9cYL\x9fU\xcc\x19P5L\xfb\xff\x86\xfb;\xfe+3;\xe4\xffd\xa6\xfew\xf3\xdf\xa5\xf3\xef\xdc\xffO\xcf\xe7\x1fx\x9e"\x91')

		self.widgets = []

		self.setupWidgets()
		
		self.help = None
		self.ticketIDWindow = None
		self.skCallsWindow = None

		if len(argv) > 1:
			self.openFile(path = argv[1])
		
		self.changeLang(self.lang)

	def openFile(self, event = None, path = None):
		if not path:
			temp = askopenfilename(title = self.textvars[28].get(), filetypes = [(self.textvars[29].get(), (".sys")), (self.textvars[30].get(), (".*"))])
			if not temp:
				return
			path = temp
		self.savePath = path		
		self.srcPath = path
		if self.processTicketFile(self.srcPath):
			return
		self.filemenu.entryconfig(2, state = "normal")
		self.filemenu.entryconfig(3, state = "normal")
		
		self.bind_all("<Control-s>", self.saveFile)		
		self.bind_all("<Control-Shift-S>", self.saveFileAs)	
		
		self.populateOptions(index = 0)
		self.changeSettings("lastFile", path)

	def reloadFile(self, event = None):
		self.openFile(path = self.srcPath)

	def processTicketFile(self, path):
		self.tikBinData = []
		self.numTickets = None
		self.lastTikIndex = None

		if self.ticketSysToList(path):
			return 1
		self.reloadNames(delete = True)
		return None

	def hexListToInt(self, hexList):
		joinedList = "".join(hexList)
		toInt = int(joinedList, 16)
		return toInt

	def byteArrayToInt(self, bArr):
		total = 0
		for index, data in enumerate(bArr): # loop through bytearray
			total |= data << 8 * (len(bArr) - index - 1) # add each number, shifting left the correct amount
		return total

	def byteArrayToHexInt(self, bArr, digits = None):
		total = 0
		for index, data in enumerate(bArr): # loop through bytearray
			total |= data << 8 * (len(bArr) - index - 1) # add each number, shifting left the correct amount
		if not digits:
			return hex(total).lstrip("0x").upper()
		return hex(total).lstrip("0x").zfill(digits)[digits * -1:].upper()

	def byteArrayToBinInt(self, bArr, digits = None):
		total = 0
		for index, data in enumerate(bArr): # loop through bytearray
			total |= data << 8 * (len(bArr) - index - 1) # add each number, shifting left the correct amount
		if not digits:
			return bin(total).lstrip("0b")
		return bin(total).lstrip("0b").zfill(digits)[digits * -1:]

	def ticketSysToList(self, path):
		binaryData = bytearray(open(path, "rb").read())
		if binaryData[0x44:0x47] != b'CAM':
			showerror(self.textvars[0].get(), self.textvars[31].get().format(self.byteArrayToHexInt(binaryData[0x44:0x47], digits = 6)))
			return 1
		self.numTickets = self.byteArrayToInt(binaryData[:4])
		for i in range(self.numTickets): # loop through tickets
			self.tikBinData.append(binaryData[i * 0x2B4C + 4:(i + 1) * 0x2B4C + 4]) # pull out ticket data
		return None

	def tikListToNames(self, tikList):
		for i in tikList:
			offsets = [self.byteArrayToInt(i[0x44:0x46]), self.byteArrayToInt(i[0x46:0x48])] # thumb and title image lengths
			titleISBN = bytearray(i[0x48 + offsets[0] + offsets[1]:0x2800]) # add these to base to get actual title/ISBN start
			while titleISBN[-1] == 0:
				del titleISBN[-1] # remove 0s from the end of the title/ISBN
			titleISBNSplit = titleISBN.split(b'\x00') # split ones that have more than just the title into the parts
			data = []
			for i in titleISBNSplit: # loop through the parts
				data.append(i.decode("gb2312", "ignore").rstrip("\n").lstrip("锘")) # decode each one, ignoring errors, and clean
			self.tikNamesUnicode.append(data)
		self.newmenu.entryconfig(0, state = "normal")
		self.newmenu.entryconfig(3, state = "normal")
		self.newmenu.entryconfig(5, state = "normal")
		
		self.bind_all("<Control-i>", self.importTicket)
		self.bind_all("<Control-n>", self.newTicket)
		
		return self.tikNamesUnicode # return to be inserted into listbox

	def populateOptions(self, ticketListEvent = None, index = None, noUpdate = False):
		if ticketListEvent:
			event = ticketListEvent.widget
			tup = event.curselection()
			if tup == ():
				return
			index = int(tup[0])

		if self.lastTikIndex != None and not noUpdate:
			if self.updateTicket(self.lastTikIndex):
				return

		curTicket = self.tikBinData[index]

		curNameInfo = self.tikNamesUnicode[index]
		curNameInfo.extend([self.textvars[32].get()] * (4 - len(curNameInfo)))

		self.titleBox.entry.config(state = "normal")
		self.ISBNBox.entry.config(state = "normal")
		self.otherValue1.entry.config(state = "normal")
		self.otherValue2.entry.config(state = "normal")		

		self.titleBox.delete(0, END)
		self.titleBox.insert(END, curNameInfo[0])

		self.ISBNBox.delete(0, END)
		self.ISBNBox.insert(END, curNameInfo[1])

		self.otherValue1.delete(0, END)
		self.otherValue1.insert(END, curNameInfo[2])
		self.otherValue2.delete(0, END)
		self.otherValue2.insert(END, curNameInfo[3])

		workingTik = self.ticketBinToList(curTicket)

		for i, j in enumerate(workingTik):
			if i not in [20, 21, 22]:
				self.widgets[i].set(self.byteArrayToHexInt(j, len(j) * 2))

		self.widgets[16].set(workingTik[16].decode())

		curThumb = self.deflatedToPNG(workingTik[20])
		curTitle = self.deflatedToPNG(workingTik[21], isTitle = True)
		self.widgets[20].img.config(image = curThumb)
		self.widgets[20].img.image = curThumb
		self.widgets[21].img.config(image = curTitle)
		self.widgets[21].img.image = curTitle	

		if self.widgets[40].get() == "7FFF": # if this is iQue Club (would break the editor somewhat)
			self.widgets[40].button.config(state = "disabled")
		else:
			self.widgets[40].button.config(state = "normal")

		self.curImagesBytes = workingTik[20:22]
		self.lastTikIndex = index
		for i in range(1, 4):
			self.nb.tab(i, state = "normal")
		self.exportTikButton.config(state = "normal")
		self.replaceTikDataButton.config(state = "normal")
		self.delTikButton.config(state = "normal")
		
		self.bind_all("<Delete>", self.deleteTicket)
		
		self.reloadNames()

	def ticketBinToList(self, binaryData):
		offsets = [self.byteArrayToInt(binaryData[0x44:0x46]), self.byteArrayToInt(binaryData[0x46:0x48])] # thumb and title image lengths
		splitList = self.ticketSplitOffsets
		splitList[21:23] = [0x48 + offsets[0], 0x48 + offsets[0] + offsets[1]]
		ticketDataList = [] # ↑ insert thumb/title image offsets and stuff
		for i, j in enumerate(splitList[:-1]): # loop through list except last element
			ticketDataList.append(binaryData[j:splitList[i + 1]]) # append offset n:offset n + 1 to ticketDataList
		return ticketDataList

	def deflatedToPNG(self, data, isTitle = False):
		dec = iter(decompress(data, -15))
		dtex = bytearray()
		if isTitle: # if this is a title image
			imgSize = (184, 24) # set image size to 184x24
			for i in dec:
				grey = i # it's literally just IA8... *screams*
				alpha = next(dec)				
				dtex.extend([grey, grey, grey, alpha])
		else: # otherwise
			imgSize = (56, 56) # set image size to 56x56
			for i in dec:
				pixel = self.byteArrayToInt([i, next(dec)])

				if self.settings["accColours"]:
					r = round((((pixel & 0xF800) >> 11) / 31) * 255) # this does a more complex mapping,
					g = round((((pixel & 0x07C0) >> 6) / 31) * 255) # the end result is only slightly more accurate but the code is
					b = round((((pixel & 0x003E) >> 1) / 31) * 255) # a lot more confusing

				else:
					r = (pixel & 0xF800) >> 8 # this code directly converts RGBA5551 to RGBA8888,
					g = (pixel & 0x7C0) >> 3 # it's ever-so-slightly inaccurate
					b = (pixel & 0x3E) << 2					

				a = (pixel & 1) * 0xFF
				dtex.extend([r, g, b, a])			

		img = frombytes("RGBA", imgSize, bytes(dtex))
		return PhotoImage(img)			

	def setupWidgets(self):

		for i in range(len(self.ticketSplitNames["en"])):
			if self.ticketSplitOffsets[i + 1] != None and self.ticketSplitOffsets[i] != None:
				sectionLength = (self.ticketSplitOffsets[i + 1] - self.ticketSplitOffsets[i]) * 2
			else:
				self.widgets.append(None)
				continue
			if i < 18:
				self.widgets.append(LabelledEntry(self.miscLeft, textvariable = self.splitnamevars[i], length = sectionLength))
			elif i < 39:
				self.widgets.append(LabelledEntry(self.miscRight, textvariable = self.splitnamevars[i], length = sectionLength))
			else:
				self.widgets.append(LabelledEntry(self.ticket, textvariable = self.splitnamevars[i], length = sectionLength))				

		self.widgets[16] = LabelledEntry(self.miscLeft, textvariable = self.textvars[33], state = "disabled", isHex = False, length = 3)

		self.widgets[18:20] = [LabelledEntry(self.miscRight, textvariable = self.textvars[34], state = "disabled"), LabelledEntry(self.miscRight, textvariable = self.textvars[35], state = "disabled")]

		self.widgets[20:22] = [ButtonImage(self.appInfo, textvariable = self.textvars[36], command = self.selectImage, bg = "#333366"), ButtonImage(self.appInfo, textvariable = self.textvars[37], command = lambda: self.selectImage(isTitle = True), bg = "#333366")]

		self.widgets[22] = Label(self.miscRight)

		self.widgets[33] = ButtonEntry(self.miscRight, textvariable = self.textvars[38], command = self.editSKCalls, state = "readonly")

		self.widgets[36] = LabelledEntry(self.appInfo, textvariable = self.textvars[39])

		self.widgets[40] = ButtonEntry(self.ticket, textvariable = self.textvars[40], command = self.editTicketID, state = "readonly")

		for i in self.widgets:
			i.pack()

	def pngToDeflated(self, img, isTitle = False):
		imgConverted = img.convert("RGBA")
		data = imgConverted.tobytes()
		
		image = iter(data)

		firstTime = True

		new = bytearray()

		if isTitle:

			for i in image:

				grey0 = i
				grey1 = next(image)
				grey2 = next(image)
				avg = (grey0 + grey1 + grey2) // 3
				alpha = next(image)
				if alpha:
					intensity = avg
				else:
					intensity = 0
				new.extend([intensity, alpha]) # it's literally just IA8... thanks Cuyler

		else:
			for i in image:

				if self.settings["accColours"]:
					r = round((i / 255) * 31) # this code does a more complex mapping; see self.deflatedToPNG for more info
					g = round((next(image) / 255) * 31)
					b = round((next(image) / 255) * 31)

				else:
					r = i // 8 # this code directly converts RGBA8888 to RGBA5551
					g = next(image) // 8
					b = next(image) // 8					

				a = next(image) // 255
				pixel = (r << 11) + (g << 6) + (b << 1) + a
				new.extend([pixel >> 8, pixel & 0xFF])	

		comp = compressobj(method = DEFLATED)
		comp.compress(new)		
		return comp.flush()

	def saveFileAs(self, event = None):
		temp = asksaveasfilename(title = self.textvars[42].get(), defaultextension = ".sys", filetypes = [(self.textvars[29].get(), (".sys")), (self.textvars[30].get(), (".*"))])
		if not temp:
			return
		self.savePath = temp
		self.saveTicketFile(self.savePath)

	def saveFile(self, event = None):
		if self.savePath:
			self.saveTicketFile(self.savePath)
			return
		self.saveFileAs()

	def updateTicket(self, index):
		newTikList = []
		for i, j in enumerate(self.widgets):
			if i not in [16, 20, 21, 22]:
				try:
					newData = bytearray.fromhex(j.get())
					if len(newData) != self.ticketSplitOffsets[i + 1] - self.ticketSplitOffsets[i]:
						raise Exception
					newTikList.append(newData)
				except:
					showerror(self.textvars[0].get(), (self.textvars[43].get()).format(self.splitnamevars[i].get(), j.get(), self.ticketSplitOffsets[i + 1] - self.ticketSplitOffsets[i]))						
					return 1
			else:
				newTikList.append(None)

		newTikList[16] = bytearray(b'CAM')

		newTikList[20:22] = self.curImagesBytes

		offsets = [self.byteArrayToInt(newTikList[18]), self.byteArrayToInt(newTikList[19])]

		if offsets[0] != len(newTikList[20]) or offsets[1] != len(newTikList[21]):
			showerror(self.textvars[0].get(), self.textvars[44].get())
			return 1

		newTikList[22] = self.titleISBNToByteArray(index, offsets)

		self.tikBinData[index] = b''.join(newTikList)

	def titleISBNToByteArray(self, index, offsets):
		self.tikNamesUnicode[index] = [self.titleBox.get(), self.ISBNBox.get(), self.otherValue1.get(), self.otherValue2.get()]

		curTitleData = self.tikNamesUnicode[index]
		while curTitleData[-1] in [self.strings[i][32] for i in self.strings]:
			del curTitleData[-1]

		joined = bytearray(b'\x00'.join([i.encode("gb2312") for i in curTitleData]))
		joined.extend(b'\x00' * (0x27B8 - offsets[0] - offsets[1] - len(joined)))
		return joined

	def saveTicketFile(self, path):
		if self.lastTikIndex != None:
			if self.updateTicket(self.lastTikIndex):
				return

		if len(self.tikBinData) != self.numTickets:
			showerror(self.textvars[0].get(), self.textvars[45].get())
			return

		tikDataJoined = bytearray(b''.join(self.tikBinData))

		newTikBin = bytearray.fromhex(hex(self.numTickets).lstrip("0x").zfill(8)) + tikDataJoined

		paddingBytes = bytearray(b'\x00' * (0x4000 - len(newTikBin) % 0x4000))

		paddedBin = newTikBin + paddingBytes

		with open(path, "wb") as file:
			file.write(paddedBin)

		self.srcPath = self.savePath

	def selectImage(self, isTitle = False):

		path = askopenfilename(title = self.textvars[46].get().format(self.textvars[47].get() if isTitle else self.textvars[48].get()), filetypes = [(self.textvars[49].get(), (".png")), (self.textvars[30].get(), (".*"))])
		if not path:
			return		
		
		newSize = (56, 56)
		
		if isTitle:
			newSize = (184, 24)
		
		img = imageopen(path)
		
		if img.size != newSize:
			img = img.resize(newSize)

		data = self.pngToDeflated(img, isTitle = isTitle)

		if isTitle:
			self.curImagesBytes[1] = data + b'\x00' * 2
			self.widgets[19].set(hex(len(data) + 2).lstrip("0x").zfill(4))
		else:
			self.curImagesBytes[0] = data + b'\x00' * 2
			self.widgets[18].set(hex(len(data) + 2).lstrip("0x").zfill(4))

		self.populateOptions(index = self.lastTikIndex)

	def newTicketSys(self, event = None):
		self.tikBinData = [bytearray(decompress(self.defaultTik, -15))]

		self.numTickets = 1
		self.lastTikIndex = None
		self.srcPath = None
		self.savePath = None
		self.reloadNames(delete = True)
		self.filemenu.entryconfig(2, state = "normal")
		self.filemenu.entryconfig(3, state = "normal")
		self.populateOptions(index = 0)

	def newTicket(self, event = None):
		self.tikBinData.append(bytearray(decompress(self.defaultTik, -15)))
		self.numTickets += 1
		self.reloadNames()
		self.populateOptions(index = len(self.tikBinData) - 1)		

	def reloadNames(self, delete = False):
		self.tikNamesUnicode = []
		new = self.tikListToNames(self.tikBinData)
		if delete:
			self.ticketListbox.delete(0, END)			
		for i, j in enumerate(new):
			if self.ticketListbox.size() <= i or self.ticketListbox.get(i) != j[0]:
				self.ticketListbox.delete(i)
				self.ticketListbox.insert(i, j[0])
		self.textvars[64].set(self.strings[self.lang][64].format(VERSION, self.numTickets))	# about window			

	def deleteTicket(self, event = None):
		if self.lastTikIndex is None:
			showerror(self.textvars[0].get(), self.textvars[50].get())
			return
		if not askyesno(self.textvars[0].get(), self.textvars[51].get().format(self.tikNamesUnicode[self.lastTikIndex][0])):
			return
		del self.tikBinData[self.lastTikIndex]
		self.numTickets -= 1
		self.reloadNames(delete = True)
		if self.numTickets and self.numTickets > self.lastTikIndex:
			self.populateOptions(index = self.lastTikIndex, noUpdate = True)
		elif self.numTickets == 1:
			self.populateOptions(index = 0, noUpdate = True)
		self.lastTikIndex = None

	def importTicket(self, event = None):
		temp = askopenfilename(title = self.textvars[52].get(), filetypes = [(self.textvars[53].get(), (".dat")), (self.textvars[30].get(), (".*"))])
		if not temp:
			return
		tikData = bytearray(open(temp, "rb").read())
		if tikData[0x40:0x43] != b'CAM':
			showerror(self.textvars[0].get(), self.textvars[54].get().format(self.byteArrayToHexInt(tikData[0x40:0x43], digits = 6)))			
			return
		if len(tikData) != 0x2B4C:
			showerror(self.textvars[0].get(), self.textvars[55].get())
			return
		self.tikBinData.append(tikData)
		self.numTickets += 1
		self.reloadNames()
		self.populateOptions(index = len(self.tikBinData) - 1)
		if self.settings["overwriteKeys"]:
			self.widgets[28].set("00000000000000000000000000000000")
			self.widgets[30].set("00000000000000000000000000000000")
			self.widgets[37].set("27DAE07405A192C63610BA2246EACF5C")
			self.widgets[39].set("00ABCDEF")
			self.widgets[45].set("00000000000000000000000000000000")
			self.widgets[46].set("00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")		

	def exportTicket(self):
		if self.lastTikIndex is None:
			return
		temp = asksaveasfilename(title = self.textvars[42].get(), defaultextension = ".dat", filetypes = [(self.textvars[53].get(), (".dat")), (self.textvars[56].get(), (".cdesc")), (self.textvars[57].get(), (".cmd")), (self.textvars[30].get(), (".*"))])
		if not temp:
			return
		extension = splitext(temp)[1]
		if extension == ".cdesc":
			toExportData = self.tikBinData[self.lastTikIndex][:0x2800]
		elif extension == ".cmd":
			toExportData = self.tikBinData[self.lastTikIndex][:0x29AC]
		else:
			toExportData = self.tikBinData[self.lastTikIndex]
		with open(temp, "wb") as file:
			file.write(toExportData)

	def replaceTikData(self):
		if self.lastTikIndex is None:
			return
		temp = askopenfilename(title = self.textvars[58].get(), filetypes = [(self.textvars[57].get(), (".cmd")), (self.textvars[56].get(), (".cdesc")), (self.textvars[59].get(), (".bin")), (self.textvars[30].get(), (".*"))])
		if not temp:
			return
		newData = bytearray(open(temp, "rb").read())
		if newData[0x40:0x43] != b'CAM':
			showerror(self.textvars[0].get(), self.textvars[54].get().format(self.byteArrayToHexInt(newData[0x40:0x43], digits = 6)))			
			return		
		if len(newData) not in [0x2800, 0x29AC, 0x2B4C]:
			if not askyesno(self.textvars[0].get(), self.textvars[60].get().format(hex(len(newData)))):
				return
		if len(newData) == 0x2B4C:
			if askyesno(self.textvars[0].get(), self.textvars[61].get()):
				self.tikBinData.append(newData)
				self.numTickets += 1
				self.reloadNames()
				self.populateOptions(index = len(self.tikBinData) - 1)
		else:
			self.tikBinData[self.lastTikIndex] = newData + self.tikBinData[self.lastTikIndex][len(newData):]
			self.reloadNames()
			self.populateOptions(index = self.lastTikIndex, noUpdate = True)
		if self.settings["overwriteKeys"]:
			self.widgets[28].set("00000000000000000000000000000000")
			self.widgets[30].set("00000000000000000000000000000000")
			self.widgets[37].set("27DAE07405A192C63610BA2246EACF5C")
			self.widgets[39].set("00ABCDEF")
			self.widgets[45].set("00000000000000000000000000000000")
			self.widgets[46].set("00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")

	def editTicketID(self):
		if self.ticketIDWindow:
			return
		
		self.ticketIDWindow = Toplevel(self)

		self.checkVar = IntVar()

		self.checkFrame = Frame(self.ticketIDWindow)
		self.checkFrame.pack()

		self.checkLabel = Label(self.checkFrame, textvariable = self.textvars[62])
		self.checkLabel.pack(side = "left")

		self.isTrial = Checkbutton(self.checkFrame, onvalue = 0x80, offvalue = 0x00, variable = self.checkVar)
		self.isTrial.pack(side = "right")

		self.spinboxFrame = Frame(self.ticketIDWindow)
		self.spinboxFrame.pack()

		self.spinboxLabel = Label(self.spinboxFrame, textvariable = self.textvars[63])
		self.spinboxLabel.pack(side = "left")

		self.idSpinbox = Spinbox(self.spinboxFrame, values = [hex(i).lstrip("0x").zfill(2).upper() for i in range(256)], state = "readonly")
		self.idSpinbox.pack(side = "right")

		data = bytearray.fromhex(self.widgets[40].get())

		if data[0]:
			self.isTrial.select()
		else:
			self.isTrial.deselect()

		for i in range(data[1]):
			self.idSpinbox.invoke("buttonup")

		self.ticketIDWindow.protocol("WM_DELETE_WINDOW", self.saveTicketID)

	def saveTicketID(self):
		isTrialTicket = self.checkVar.get()
		newID = int(self.idSpinbox.get(), 16)
		tempBytes = bytearray([isTrialTicket, newID])
		self.widgets[40].set(self.byteArrayToHexInt(tempBytes, digits = 4))
		self.ticketIDWindow.destroy()
		self.ticketIDWindow = None

	def editSKCalls(self):
		if self.skCallsWindow:
			return
		
		self.skCallsWindow = Toplevel(self)

		self.skCheckVars = []

		self.skCheckFrames = []

		self.skCheckBoxes = []

		for i in self.skCalls:
			self.skCheckFrames.append(Frame(self.skCallsWindow))
			self.skCheckFrames[-1].pack()

			self.skCheckVars.append(IntVar())

			self.skCheckBoxes.append([Label(self.skCheckFrames[-1], text = i), Checkbutton(self.skCheckFrames[-1], variable = self.skCheckVars[-1])])
			self.skCheckBoxes[-1][0].pack(side = "left")
			self.skCheckBoxes[-1][1].pack(side = "right")

		data = self.byteArrayToBinInt(bytearray.fromhex(self.widgets[33].get()), digits = 15)
		for i, j in enumerate(data[::-1]):
			if j == "1":
				self.skCheckBoxes[i][1].select()
			else:
				self.skCheckBoxes[i][1].deselect()

		self.skCallsWindow.protocol("WM_DELETE_WINDOW", self.saveSKCalls)

	def saveSKCalls(self):
		tempBits = 0
		for i, j in enumerate(self.skCheckVars):
			tempBits += j.get() << i
		tempBytes = bytearray([tempBits >> 8, tempBits & 0xFF])
		self.widgets[33].set(self.byteArrayToHexInt(tempBytes, digits = 8))
		self.skCallsWindow.destroy()
		self.skCallsWindow = None

	def displayAbout(self):
		if self.help:
			return
		self.help = Toplevel(self)
		self.textvars[64].set(self.strings[self.lang][64].format(VERSION, self.numTickets))		
		self.about = Label(self.help, textvariable = self.textvars[64])
		self.about.pack()
		self.help.protocol("WM_DELETE_WINDOW", self.closeAboutWindow)		
	
	def closeAboutWindow(self):
		self.help.destroy()
		self.help = None

	def changeSettings(self, toChange = None, value = None):
		if toChange or value != None:
			self.settings[toChange] = value
		dump(self.settings, open(self.saveDataPath, "w"))

	def settingsChanged(self, key, index):
		self.changeSettings(key, index)

	def sortTickets(self):
		if self.updateTicket(self.lastTikIndex):
			return
		self.tikBinData = sorted(self.tikBinData, key = lambda x: self.tikNamesUnicode[self.tikBinData.index(x)])
		self.lastTikIndex = None
		self.reloadNames()
	
	def changeLang(self, lang):
		self.lang = lang
		for i, j in enumerate(self.strings[self.lang]):
			self.textvars[i].set(j)
		
		self.textvars[64].set(self.textvars[64].get().format(VERSION, self.numTickets))
		
		for i, j in enumerate(self.ticketSplitNames[self.lang]):
			self.splitnamevars[i].set(j)
		
		self.title(self.textvars[0].get())
		
		if self.help:
			self.help.title(self.textvars[0].get())
			
		if self.ticketIDWindow:
			self.ticketIDWindow.title(self.textvars[0].get())
			
		if self.skCallsWindow:
			self.skCallsWindow.title(self.textvars[0].get())
		
		self.filemenu.entryconfig(0, label = self.textvars[1].get())
		self.filemenu.entryconfig(1, label = self.textvars[2].get())
		self.filemenu.entryconfig(2, label = self.textvars[3].get())
		self.filemenu.entryconfig(3, label = self.textvars[4].get())
		self.filemenu.entryconfig(5, label = self.textvars[5].get())
		
		self.newmenu.entryconfig(0, label = self.textvars[7].get())
		self.newmenu.entryconfig(1, label = self.textvars[8].get())
		self.newmenu.entryconfig(3, label = self.textvars[9].get())
		self.newmenu.entryconfig(5, label = self.textvars[65].get())
		
		self.optionsmenu.entryconfig(0, label = self.textvars[11].get())
		self.optionsmenu.entryconfig(1, label = self.textvars[12].get())
		
		self.langmenu.entryconfig(0, label = self.textvars[66].get())
		self.langmenu.entryconfig(1, label = self.textvars[67].get())
		self.langmenu.entryconfig(2, label = self.textvars[73].get())
		self.langmenu.entryconfig(3, label = self.textvars[69].get())
		self.langmenu.entryconfig(4, label = self.textvars[70].get())
		self.langmenu.entryconfig(5, label = self.textvars[71].get())
		self.langmenu.entryconfig(6, label = self.textvars[72].get())
		
		self.helpmenu.entryconfig(0, label = self.textvars[14].get())
		
		self.menubar.entryconfig(1, label = self.textvars[6].get())
		self.menubar.entryconfig(2, label = self.textvars[10].get())
		self.menubar.entryconfig(3, label = self.textvars[13].get())
		self.menubar.entryconfig(4, label = self.textvars[68].get())
		self.menubar.entryconfig(5, label = self.textvars[15].get())
		
		self.editor.config(text = self.textvars[16].get())
		
		for i in range(0, 4):
			self.nb.tab(i, text = self.textvars[i + 17].get())
		
		for i in [self.titleBox, self.ISBNBox, self.otherValue1, self.otherValue2]:
			if i.get() in [self.strings[i][32] for i in self.strings]:
				i.set(self.strings[self.lang][32])
	
	def langButtonClicked(self, event = None):
		if event:
			if self.lang != self.langs[-1]:
				self.changeLang(self.langs[self.langs.index(self.lang) + 1])
			else:
				self.changeLang("en")
		else:
			self.changeLang(self.langButtonVar.get())
		self.changeSettings("lang", self.lang)
		self.langButtonVar.set(self.lang)		

if __name__ == "__main__":
	OwO_UwU().mainloop() # Just a random name choice, no reason behind it at all