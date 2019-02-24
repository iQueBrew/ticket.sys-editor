#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import Button, Entry, Frame, Label, LabelFrame, Tk, Toplevel
from tkinter.filedialog import *
from tkinter import ttk
from tkinter import messagebox
import zlib, PIL.Image, PIL.ImageTk, os, sys, json, io

VERSION = "1.6"

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

		self.strings = {"en": ["ticket.sys editor", "Open file", "Reload current file", "Save", "Save as", "Exit", "File", "New ticket", "New ticket.sys", "Import ticket.dat", "Edit", "Overwrite keys when importing", "Use more accurate colour mapping", "Options", "About", "Help", "Ticket options", "General", "App info", "Misc.", "Ticket data", "Title:", "ISBN:", "Unknown value #1:", "Unknown value #2:", "Export ticket", "Replace ticket data", "Delete ticket", "Select ticket.sys", "iQue Player system files", "All files", "This file is not a valid ticket.sys!\nTicket #1 magic: {}", "None found", "Magic:", "Thumb image length:", "Title image length:", "Thumb image:", "Title image:", "Allowed SK calls:", "CID:", "Ticket ID:", "Warning: Title images must be monochrome only, so some data will be lost trying to directly convert your selected image to a title.", "Select file to save to", "Invalid value for {} {}\nPlease make sure it is {}-byte long hex integer!", "Title or thumb image length is incorrect! Please tell Jynji that this message appeared, or try a less complex image.", "numTickets is incorrect! Please report this to Jynji, along with what you were doing before saving the ticket file.", "Select PNG format {} image", "title", "thumb", "Portable Network Graphics file", "Please select a ticket first!", "Are you sure you want to delete the ticket for \"{}\"? This can't be undone!", "Select ticket.dat", "iQue Player ticket files", "This file is not a valid ticket!\nTicket magic: {}", "This file's length is incorrect! To import a CMD or contentDesc file, please make a new ticket and use the 'Replace data' function.", "iQue Player content description files", "iQue Player content metadata files", "Select data to import", "Binary files", "The file you selected does not appear to be a contentDesc file or content metadata file! Continue to import {} bytes?", "The file you selected appears to be a complete ticket file! Import as ticket? (Selecting 'No' will cancel the import.)", "Is trial ticket:", "ID:", "Version {} of ticket.sys editor by Jynji. Watch this space!\nCurrent numTickets: {}\n\nChinese translation: tenyuhuang, SKSA\nFrench translation: MelonSpeedruns\nGerman translation: Mr_ZG\nItalian translation: asper", "Sort tickets", "English", "中文", "Language", "Français", "Deutsch", "Italiano"], "zh": ["神游机程序数据库编辑器", "打开", "重新加载当前文件", "保存", "另存为", "退出", "文件", "新建信息表", "新建程序数据库", "导入ticket.dat", "编辑", "导入时覆盖密钥", "导入图片时使用更精准的颜色映射", "设置", "关于", "帮助", "信息表设置", "常规", "程序信息", "其他", "信息表数据", "标题：", "ISBN：", "未知数值 #1", "未知数值 #2", "导出信息表", "替换信息表数据", "删除信息表", "选择ticket.sys", "神游机系统文件", "所有文件", "这不是有效的ticket.sys！\n信息表#1的幻数：{}", "未填写", "幻数：", "缩略图文件大小：", "标题图片文件大小：", "缩略图：", "标题图片：", "允许调用的SK功能：", "程序编号：", "信息表ID：", "警告：请选择一张黑白图片作为标题图。如果选择的图片为彩色，在转换过程中可能会有损失。", "选择要保存的文件名", "{}的值“{}”无效！\n请输入长度为{}字节的16进制整数。", "图片文件大小有误！请将此问题反馈给Jynji，或者更换一张简单一些的图片。", "numTickets有误！请将此问题反馈给Jynji，描述一下错误产生之前您所做的操作。", "请选择一张PNG格式的{}", "标题图片", "缩略图", "PNG图片文件", "请先选择一张信息表！", "你确定要删除“{}”的信息表吗？本操作无法撤销！", "选择ticket.dat", "神游机程序信息表文件", "这不是一个有效的信息表！\n信息表幻数：{}", "文件大小有误！想要导入文件，请新建一个数据表并选择“替换数据”。", "神游机内容描述文件", "神游机内容元数据文件", "请选择要导入的数据", "二进制数据文件", "所选文件不像是描述文件或者元数据文件，依然要导入{}字节的数据吗？", "所选文件好像是一个完整的信息表，要作为信息表导入吗？\n（选择“否”将取消导入）", "是否为试玩版：", "ID：", "神游机程序数据库编辑器 by Jynji / 版本：{} / 静候佳音！\n当前数据库中有{}张信息表。\n\n中文版翻译：tenyuhuang、SKSA\n法语版翻译：MelonSpeedruns\n德语版翻译：Mr_ZG\n意大利语翻译：asper", "重排信息表顺序", "English", "中文", "语言", "Français", "Deutsch", "Italiano"], "fr": ["Éditeur ticket.sys", "Ouvrir un fichier", "Recharger le fichier", "Sauvegarder", "Sauvegarder sous", "Quitter", "Fichier", "Nouveau Ticket", "Nouveau ticket.sys", "Importer un ticket.dat", "Modifier", "Remplacer les clés lors de l'importation", "Utilisez des couleurs plus précises", "Paramètres", "À propos", "Aide", "Options de Ticket", "Général", "Infos de l'app", "Divers.", "Données du Ticket", "Titre:", "ISBN:", "Valeur Inconnue #1:", "Valeur Inconnue #2:", "Exporter le Ticket", "Remplacer les données", "Supprimer le Ticket", "Sélectionner un Ticket.sys", "Fichiers système du iQue Player", "Tout les fichiers", "Ce fichier n'est pas un ticket.sys valide !\nTicket #1 magie: {}", "Aucun trouvé", "Magie:", "Longueur de l'image bannière:", "Longueur de l'image titre:", "Image bannière:", "Image titre:", "Appels SK autorisés:", "CID:", "ID du Ticket:", "Attention: les images de titre ne doivent être que monochromes; certaines données seront donc perdues si vous essayez de convertir directement l'image sélectionnée en titre.", "Sélectionnez un fichier à remplacer.", "Valeur non valide pour {} {}\nVeuillez vous assurer qu'il s'agit d'une valeur longue de {} bytes.", "La longueur du titre ou de l'image de bannière est incorrecte! Merci de dire à Jynji que ce message est apparu ou d'essayer une image moins complexe.", "numTickets est incorrect! Signalez-le à Jynji, ainsi que ce que vous faisiez avant de sauvegarder le fichier de ticket.", "Sélectionez une image PNG {}", "titre", "bannière", "Fichier Portable Network Graphics", "Veuillez d'abord sélectionner un ticket!", "Êtes-vous sûr de vouloir supprimer le ticket pour \"{}\" ? Cela ne peut pas être annulé!", "Sélectionnez le ticket.dat", "Fichiers Ticket iQue Player", "Ce fichier n’est pas un ticket valide !\nTicket magie: {}", "La longueur de ce fichier est incorrecte! Pour importer un fichier CMD ou contentDesc, créez un nouveau ticket et utilisez la fonction \"Remplacer les données\".", "Fichiers de description du contenu du iQue Player", "Fichiers de métadonnées du contenu du iQue Player", "Sélectionnez les données à importer", "Fichiers binaires", "Le fichier que vous avez sélectionné ne semble pas être un fichier contentDesc ni un fichier de métadonnées ! Continuer à importer {} octets ?", "Le fichier que vous avez sélectionné semble être un fichier de ticket complet! Importer en tant que ticket? (Si vous sélectionnez 'Non', l'importation sera annulée.)", "Est un Ticket d'essai:", "ID:", "Version {} de l'éditeur de ticket.sys par Jynji. Surveillez cet endroit !\nNuméros actuels: {}\n\nTraduction en Français: tenyuhuang, SKSA\nTraduction en Français: MelonSpeedruns\nTraduction en Allemand: Mr_ZG\nTraduction en Italien: asper", "Trier les tickets", "English", "中文", "Langue", "Français", "Deutsch", "Italiano"], "de": ["ticket.sys bearbeiten", "Datei öffnen", "Aktuelle Datei neu laden", "Speichern", "Speichern unter", "Beenden", "Datei", "Neues Ticket", "Neues Ticket.sys", "Ticket.sys importieren", "Bearbeiten", "Schlüssel beim Importieren überschreiben", "Genauere Farbzuordnung benutzen", "Optionen", "Über", "Hilfe", "Ticket-Optionen", "Allgemein", "App-Infos", "Diverses", "Ticket-Daten", "Titel:", "ISBN:", "Unbekannter Wert #1:", "Unbekannter Wert #2:", "Ticket exportieren", "Ticket Daten ersetzten", "Ticket löschen", "ticket.sys auswählen", "iQue Player Systemdateien", "Alle Dateien", "Diese Date ist keine gültige ticket.sys!\nTicket #1 magic: {}", "Keine gefunden", "Magie:", "Größe des Vorschaubildes:", "Größe des Titel:", "Vorschaubild:", "Titelbild:", "SK abrufen erlauben:", "CID:", "Ticket ID:", "Warnung: Titelbilder müssen einfarbig sein, einige Daten werden verloren gehen bei dem Versuch das ausgewählte Bild in einen Titel zu konvertieren", "Datei zum Speichern auswählen", "Ungültiger Wert für {} {}\nStelle sicher das sie {}-byte lange Hexadezimalwert ist", "Titel- oder Vorschaulänge is falsch. Informiere Jynji hierüber oder wähle ein weniger kompliziertes Bild", "numTickets ist falsch! Informiere Jynji darüber was du getan hast bevor du die Ticket Datei gespeichert hast", "Wähle PNG format aus {} Bild", "Titel", "Daumen ()", "PNG-Datei", "Wähle zuerst ein Ticket aus", "Bist du sicher das du das Ticket für \"{}\" löschen willst? Dies kann nicht rückgängig gemacht werden!", "ticket.sys auswählen", "iQue Player Ticket-Dateien", "Diese Datei hat eine ungültige Größe\nTicket Magie: {}", "Diese Dateigröße ist falsch! Zum iomportieren einer CMD oder contentDesc- Datei, bitte erstelle ein neues Ticket und benutze die 'Datei ersetzen'-Funktion.", "iQue Player Inhaltsbeschreibung", "iQue player Inhaltsmetadaten", "Wähle Datei zum importiern", "Binärdateien", "Die ausgewählte Datei ist scheinbar keine contentDesc oder Inhaltsmetadateien-Datei! Mit dem Importieren von {} bytes fortfahren?", "Die ausgewählte Datei sieht wie eine komplette Ticket-Datei aus! Als Ticket importieren? ('Nein' wird den Import abbrechen)", "Ist ein Test-Ticket:", "ID:", "Version {} des ticket.sys Editor von Jynji. Achte auf diesen Bereich!\nAktuelle numTickets: {}\n\nChinesische Übersetzung: tenyuhuang, SKSA\nFranzösische Übersetzung: MelonSpeedruns\nDeutsche Übersetzung: Mr_ZG\nItalienische Übersetzung: asper", "Tickets sortieren", "English", "中文", "Sprache", "Français", "Deutsch", "Italiano"], "it": ["Editor del ticket.sys", "Apri file", "Ricarica file corrente", "Salva", "Salva con nome", "Esci", "File", "Nuovo ticket", "Nuovo ticket.sys", "Importa ticket.dat", "Modifica", "Sovrascrivi le chiavi mentre si importa", "Utilizza color mapping accurato", "Opzioni", "Informazioni", "Aiuto", "Opzioni ticket", "Generale", "Info app", "Varie", "Dati ticket", "Titolo", "ISBN:", "Valore sconosciuto #1", "Valore sconosciuto #2", "Esporta ticket", "Sostituisci dati ticket", "Cancella ticket", "Seleziona ticket.sys", "Files di sistema iQue Player", "Tutti i files", "Questo non è un ticket.sys valido!\nTicket #1 magic: {}", "Non trovato", "Magic:", "Lunghezza immagine di anteprima:", "Lunghezza titolo immagine:", "Immagine di anteprima:", "Immagine titolo:", "Calls SK permesse:", "CID:", "Ticket ID:", "Attenzione: Le immagini devono essere soltanto monocromatiche, quindi alcuni dati andranno persi cercando di convertire direttamente l'immagine selezionata in un titolo. ", "Seleziona file in cui salvare", "Valore non valido {} {}\nAssicurarsi che sia un valore hex intero lungo {}-byte", "Lunghezza immagine titolo o di anteprima non corretta! Informa Jynji della comparsa di questo messaggio oppure prova con una immagine meno complessa.", "numTickets non corretto! Informa Jynji di questo errore, assieme ad informazioni riguardo cosa stavi facendo prima di salvare il file ticket.", "Seleziona immagine {} in formato PNG", "titolo", "anteprima", "Portable Network Graphics file", "Si prega di selezionare prima un ticket", "Sicuro di voler cancellare il ticket per \"{}\"? Questa operazione non puo'essere annullata!", "Seleziona ticket.dat", "Ticket files iQue Player", "Questo non è un file ticket valido!\nTicket magic: {}", "La lunghezza del file non è corretta! Per importare un CMD o un file contentDesc, creare un nuovo ticket ed utilizzare la funzione \"Sostituisci dati\".", "Files descrizione contenuto iQue Player", "Files metadata contenuto iQue Player", "Seleziona dati da importare", "Files binari", "Il file selezionato non sembra essere un file contentDesc o metadata content! Continuare ad importare {} bytes?", "Il file selezionato sembra essere un file ticket completo! Importarlo come ticket? (Selezionando 'No' l'operazione di importazione verrà annullata.)", "E'un ticket dimostrativo:", "ID:", "Ticket.sys editor versione {} by Jynji. Controlla questo spazio!\nCurrent numTickets: {}\n\nTraduzione Cinese: tenyuhuang, SKSA\nTraduzione Francese: MelonSpeedruns\nTraduzione Tedesca: Mr_ZG\nTraduzione Italiana: asper", "Ordina tickets", "English", "中文", "Lingua", "Français", "Deutsch", "Italiano"]}
		
		self.langs = list(self.strings.keys())
		
		self.textvars = [StringVar() for i in self.strings["en"]]
		
		self.localappdata = os.getenv("localappdata")

		if not os.path.isdir("{}\\Programs\\ticket.sys editor".format(self.localappdata)):
			os.mkdir("{}\\Programs\\ticket.sys editor".format(self.localappdata))

		self.saveDataPath = "{}\\Programs\\ticket.sys editor\\config.json".format(self.localappdata)

		try:
			self.settings = json.load(open(self.saveDataPath))
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
		
		self.flags = [b"\x01!\x02\xde\xfd\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x0b\x08\x02\x00\x00\x00\xf9\x80\x9an\x00\x00\x01\xe8IDAT(Sc\x984s\xdf\x8e\xabo\xaa\xa7\x1fKi\x06\xa2\xc3\x89\x8d\x07n\xde}\xbb6\xb9qMB\x1d\x90\xe1\x99\xbd\xcd#m\x87m\xcc\x86\xa8\xc6\x9ds\x02\xf3\xab\xe7\x1eeX\xb2\xe2\xd4\xff\x8d\xab\xfe\xfd\xfb\x7f\xfb\xe1\x97E\x1bn\xcf_\x7f\x07\xc8\xfe?\xa5\xe7\x7f_+\x901i\xe1\xe5\xde\xb9\x17N\x9ex\xfc\xaf\xab\xe6\xdf\xdf\x9f\x136]`Hj9\xb8\xe7\xe4\xbb\xffK\x97\xff?\xb8\xf7\xff\xff\xffm\xd3\xae\x02\xc9\xff\xa9\x99\xff\x13\x12\x81tI\xdf\xa5/\x8b\xd6|\xef\xee\x06\xb2\xe7\xad\xba$i2\x03\xa4a\xe1\x86\xbbu\x13\xaf>\xdcw\xffOS\xfd\x7f\x08\x88\x89\xf9\x1f\x1e\x01b\xe4f\xfe\x7f\xf1\xe2\xc2\x9d\xb7\x8e\x9e\xcb\x8b\x9a\x8e\x08\xeaNd\x00:\x14\xe4\x064\x10\x1a\xfa\xdf\xcf\x0fM\x0c\xa8\xec\xcc\xb5\x97\x0ck\x12k\xffO\xee\xf8\x9f\x92\xf2?>\xfe\x7fd\xe4\xff\x90\x10\x90R\x1f\x9f\x7f\xae\xae\xbf\xec\xed\x7fZZ~71\xf9\xaa\xa7\xf7U[\xfbg\xb0[\xab\xbc\x15\x0e\x1blm\xff\x98Y@\xcc\x05\xe2\xbf\x7f\xff\xfe\xf9\xfb\xe7\xf7\x9f?'\xaf\xbe`\xb0\x8f\xdb\xd43\xe7|T\xda\x8e+W\xdf\xff\x7f\xfb\xe6gr<H\x95\x91\xc9o}C\xb0\x86\xbfO\x9d\x1c\xf7\xcf\xdc*!=+$a=\x83p6\x83y\xd8\xba\xc5\xebA!\xf3\xb9\xb1\xeeCWWL\xc91 \xfb\x8f\xb6\xee/Mm\xa0\xab\xad\xec\x97\xfc\xfc\xff\xff\xcb\xac\xb9/\x12b\x9a\xa6\x9ec\x10Lg\x98\xbc\xf9\xf2\xbf\x7f\x7f\xbf\xb7W\x1c=p\xbb\xb0\xe1`^\xc3a\xa0\x0b\xff\x86x\xfc\x0er\xfe\xf7\xf7ox\xda\xb6\xd0\xb8\xd5\xdb\x0f\xdf\xfa\xfb\xe7\xc7\xeb\x04\xdf\xec\xa2%\x0cU\xf3\x0eLqIv\xce\\$\xa83\x87Gc2\x87\xea\x84\xf3\xd7^\xb4J[\xb4\x88\x9b\x9c\xbe\xf2\x92A\xbc\x98A\xb4\x80A8W\xc4\xb0\xaew\xcfuW\xd3<\x00<Lh\xaaP\x97\x0bh\x00\x00\x00\x00IEND\xaeB`\x82\x89)\x1a\x17", b"\x01]\x01\xa2\xfe\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x0b\x08\x02\x00\x00\x00\xf9\x80\x9an\x00\x00\x01$IDAT(S]\x911JCa\x10\x84'\xc9\x8bb\x11\xb0\x12S\xa4\x10\x04/\xa0G\xf0\x18\xe6\x10\x96Zx\x1d\x0b\x91\x98\xc2\xc6RA\xbc\x80\x9e\xc0BE\x10\x13\x13\xb33\xbbk\xf1\xbf\x17\x1e\xc2\x16\xc3\xb23\xfb\xb1\xdby\x01\x02\x08\xa0\x0b\x00\xd8>\xc6\xfb\x1d\xd04\x05\x00PKW\x01\xec^\x9c\x0fN0\xbb\x8c\xfe^l\x1e\xf9\xf6\xab\xcf&\x82)\xa5$CJ\xb2\xe8\xe7\xe9\xb4\n`0\xce\xde\xce\xeb`\xec\x9fg\x1e\x0bn\x1cz\xff\x80\xf3\x1b&\x99\xc6\xa4\x85Y\x92\xd5h\xa4\x022\xbf\xca\x98\xf9\xcf\xad\xfb/;\x03O\x99\xbf1\x8da\x96\\\x85Y]\xa4\x80\n@|\xf9\xc7\xa9\x90\xda:R\xb5\xcf\xe5\x03\x97\xf7\x8cVv\x9a\x05\x99\xc5\x10@\xac\xbc\xb0.\x9f\x84-\xce&\x96d\x92%\x15M|H\xb5!])\x81\xe6\x0b}_3i\x85'\xd6\xd9\xc5@Fm(-)[\x00\xff\xa7%\xac7@*\x88A\x86Y=\xd1p\xa7Y\x88)Ow\x00\x95\x80\xa0z\xc3a\x92]y\x8au|s\xfe\x90\xe0\x1e\xee\xe9.\xa0\xf3\xd8zd[\xa8\xf5\xech\xaa\x02\xfe\x00:\xaes0\xea\xa6\xcd\x80\x00\x00\x00\x00IEND\xaeB`\x82Th\x93\xf3", b'\x01o\x01\x90\xfe\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x0b\x08\x02\x00\x00\x00\xf9\x80\x9an\x00\x00\x016IDAT\x18\x19m\xc0=\xae\x8cQ\x1c\x06\xf0\xe7\x9cy\x15W\xe26$2t\x16 \xb1\x01\x95Zb#\x1a\x8dZD\xa9\x115{\xba[\x10\x9d\xca\x9d\xc99\xff\xf3|x\x8dH\x14~\xdb\x9b\xcf7\xf8\xcb\xf4\xeb\x97\xd7\x92\xe6\x9c\x92H\xb6\xd6\x9e\xbcx\xe6[p\x82\x80\x81\r\xc0\xab\xe7\x8f\x00\xc4\xb1s<\xdeK\x02 \x89\xed$w\xde\x7f\x0c\x97\xab\xb2\xd6\x8f\xb7\xef6\xec\x82\x9f\xe7%\xc5\xf6\xe9t\xca\x85\xed\xd6\x9a\xa4\xeb\xef\xdf\\35q\xff\x01\x81\rF\x1c)\xb2\xa5\xf4\xdeI\xb6\xd6z\xef\xfe\xa3\x86g\x85\xb3U\x19\xd8H\xcb\x96,\x85V\x92\xde{\xbc\xcb\x0e\x80\xe7LM\xd7jU\x05lU\xb4#y\xd9b\x0e\x87\x83w\xc0\xd6a\xb7\x9d\xe7\xcc*W5\xd2\xc0V4\x95%S&\x9d\x7fH\xca\xae\xa6\xaaR\xabW\x15\xb0\x8d\xa2l\xd2K\xe6\x92/\x92H\xf2\x85\xaaR\xd3k\x81\xcb\xc06\x06I/\x9a\xd4\xa2\xffc\xcepy\xadF\x11\xd8\xceU\xa4\xef^\x1dD\x90\xbd\xb5\xd6{\xc7E\xbb8<<\x9alb\xb4\x0cl\xe73?|\xbd\x19\xa3\xce\x83\xb7\xa3\x1e_\x1d\xabj\x8dQRU\x8d1\x9e~\xfab\x80\x80\xf1\xdb/\x91\xffze\x89G\x1d\x1f\x00\x00\x00\x00IEND\xaeB`\x82/J\xab0', b'\x01g\x01\x98\xfe\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x0b\x08\x02\x00\x00\x00\xf9\x80\x9an\x00\x00\x01.IDAT(Su\x90=J\x04Q\x10\x84k~\x16\x8cD11pSC\x05\xd7\xc8P1\x134\xf4\x1e\x06\xde\xc2\x8b\x08{\t\x13M=\x8a \xd3\xaf\x7f\xed\x9eY4\xb2\xa7\xa7\xa8\xf7\xa6\xbei\xe8\xee\xee\xee\x066\xc1\x1d\xc3\xc8\xea,\x1a.\x80\xe3\x9f\x1aE\xa6\xa7\xa7\xe7t>\x97\x99\x9a-\xaa\xbb\x12\xd1\xf2\x92\xb5\xdd\xbe\x8e}\xdf\x03x\xff\xf8\xac\x0f\xf35g\xb5z~\x8b\x88\xf2\xbd\x7f\xb8\xae\tk\xe0\xc0}=\xa7\x95\xb9\x88\xd6\xb2\x93\x12"n\x94\x80L\x94\xfc\xb1J\x01\x8f\xd26f\x1b\x91`\x8eE[\xcbvj\xdeh6\x14Ss\xa6\x95\xe8\x98@\x08\x87\x192\xc7\x12\x99`\xf6\x1d0\xa7\xb3\xa7i\xe1+Y\x00\x00\xd3\xbf\x1f\xa7!\xca\xf4\x0e\xcb47\xcbt\xde\x9bXm\xe9\n8\x8d\x18<\xcc]\xb2m1Q\xebM\x85I\xa4z\xeaeGo9\xe1\x0cq\xe2q\x98\xa9\xeaH5\x8d\xda\xb0.k\xce\xbb\xf9\x888\xea\xfc\x16#\x18\xa1\x82\xd5E\x0f\xee\nHU\x84D\xf9T\x8dHBk\nk\xff\x8dn\xfbr\xbeg\xf0\xc4\x06\xb4\t\x0e\xc4>z\x82\x1bx\x80q\x99U\x0f\'`\xc0\x17\xe3\x078 \x87a1\x9cE\x9f\x00\x00\x00\x00IEND\xaeB`\x82\x18\xc9\x9b\xf2', b'\x01S\x01\xac\xfe\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x0b\x08\x02\x00\x00\x00\xf9\x80\x9an\x00\x00\x01\x1aIDATx\xdacd\x98\xc8\xc0\xf0\x83\x01\x04\xfe10\xfcax\x9a\xf4\xf4\x1f*\x90RU\xfd\x07\x96\x84 \x16\x86/\x0c\xd5\xae\xd5 \xf5@\xf0\xff\x9f\xa4\xa4\xe4\xff\xff@\xde\xff\xffp*&\xe6\xff\xef\xdf\xff\xff\xfc\x01\x92_6mba`\x01\x89?\xf9\xfa\xf4\xef\xbf\xbf@\x80P\x07\x07\xb7o\xff\xff\xf5\x0b\xa8\x9aQV\x16h\x03\x0b\xd0\x1a\xa0\xc9@\xd5\x7f\x80\xe8\xefot\xd5@\x00T\r\xd6\xc0\xf0\xfb7P\x03\xc8\xfc\xbf\x0c\x7f\xff\x00\xad\xfc\x07B\xff1\x01\x92\x06\xa0b\x16\xa0G\x81f\xff\xfe\xfb\xfb\xcf_B\x1a\x80\xf2\x0c\x0c \r\x7f\xc1f\xff\xfa\xf7\x0b\xa8\x07\x8f\x06F\xb0\x93\x98\x80\x1a~\xff\xff\xfd\xeb/H\xf5\xef\xbf\xbf\xb0k\x00\x1b\x0ft\xf5\x1f\x06\x06\xb0\x93@J\x7fC\x10v\r\x7f\x80\x1a\x80>\xfd\x0b\xf4\x03\x0b0\xd6~\xff\xfb#\xc9-\t\xf2\xc6\x9f\xbf\xe0(d`ddd\x80\x03%%\x90R0\x02:\x89\x91\xa1\x94\x81\xe1\x13(\x8eA\xf1\xfd\x83\xe1l\xd5Y\xa0\xcd\xc08\x84\x90@\xf5\n\xf6\xf6\x908\x86\x00\x00.Vw\x84\ry\x93x\x00\x00\x00\x00IEND\xaeB`\x82y\x8e\x99\xd8']
		
		self.flagVars = []
		for i in self.flags:
			dec = zlib.decompress(i, -15)
			fileObj = io.BytesIO(dec)
			temp = PIL.Image.open(fileObj)
			self.flagVars.append(PIL.ImageTk.PhotoImage(temp))
		
		self.langmenu = Menu(self.menubar, tearoff = 0)
		self.langmenu.add_radiobutton(variable = self.langButtonVar, command = self.langButtonClicked, value = "en", accelerator = "Ctrl+L", image = self.flagVars[0], compound = "left")
		self.langmenu.add_radiobutton(variable = self.langButtonVar, command = self.langButtonClicked, value = "zh", accelerator = "Ctrl+L", image = self.flagVars[1], compound = "left")
		self.langmenu.add_radiobutton(variable = self.langButtonVar, command = self.langButtonClicked, value = "fr", accelerator = "Ctrl+L", image = self.flagVars[2], compound = "left")
		self.langmenu.add_radiobutton(variable = self.langButtonVar, command = self.langButtonClicked, value = "de", accelerator = "Ctrl+L", image = self.flagVars[3], compound = "left")
		self.langmenu.add_radiobutton(variable = self.langButtonVar, command = self.langButtonClicked, value = "it", accelerator = "Ctrl+L", image = self.flagVars[4], compound = "left")		
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

		self.nb = ttk.Notebook(self.editor)
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

		self.ticketSplitNames = {"en": ["EEPROM RDRAM location:", "EEPROM size:",
		                                "Flash RDRAM location:", "Flash size:",
		                                "SRAM RDRAM location:", "SRAM size:",
		                                "Controller Pak 0 RDRAM location:",
		                                "Controller Pak 1 RDRAM location:",
		                                "Controller Pak 2 RDRAM location:",
		                                "Controller Pak 3 RDRAM location:",
		                                "Controller Pak size:", "osRomBase:",
		                                "osTvType:", "osMemSize:",
		                                "Unknown value #3:", "Unknown value #4:",
		                                "Magic:", "Number of .u0x files:",
		                                "Thumb image length:", "Title image length:",
		                                "Thumb image:", "Title image:", "Title/ISBN",
		                                "Padding:", "Certificate Authority CRL version:",
		                                "Content Protection CRL version:", "Size:",
		                                "Unknown value #5:", "Titlekey IV:",
		                                "SHA-1 hash of plaintext:", "Content IV:",
		                                "Exec flags:", "Hardware access rights:",
		                                "Allowed SK calls:", "CMD BBID:", "CMD certificate:",
		                                "CID:", "Titlekey:", "Signature:", "Ticket BBID:",
		                                "Ticket ID:", "Type of trial:",
		                                "Minutes or launches for trial:", "Padding:",
		                                "Ticket CRL version:", "Titlekey IV 2:",
		                                "ECC public key:", "Ticket certificate:", "Signature:"],
		                         
		                         "zh": ["EEPROM RDRAM位置：", "EEPROM大小：",
		                                "Flash RDRAM位置：", "Flash大小：",
		                                "SRAM RDRAM位置：", "SRAM大小：",
		                                "Controller Pak 0 RDRAM位置：",
		                                "Controller Pak 1 RDRAM位置：",
		                                "Controller Pak 2 RDRAM位置：",
		                                "Controller Pak 3 RDRAM位置：",
		                                "Controller Pak大小：", "osRomBase：",
		                                "osTvType：", "osMemSize：",
		                                "未知数值 #3：", "未知数值 #4：",
		                                "幻数：", ".u0x文件的个数：",
		                                "缩略图文件大小：", "标题图片文件大小：",
		                                "缩略图：", "标题图片：", "标题/ISBN",
		                                "填充：", "证书颁发机构CRL版本：",
		                                "内容保护CRL版本：", "应用程序大小：",
		                                "未知数值 #5：", "Titlekey IV：",
		                                "明文数据的SHA-1：", "内容IV：",
		                                "执行参数：", "硬件访问权限：",
		                                "允许调用的SK功能：", "内容元数据BBID：", "内容元数据证书：",
		                                "程序编号：", "Titlekey：", "签名：", "信息表BBID：",
		                                "信息表ID：", "试玩类型：",
		                                "试玩版总共可用的分钟数/次数：", "填充：",
		                                "信息表CRL版本：", "Titlekey IV 2：",
		                                "ECC公钥：", "信息表证书：", "签名："],
		                         "fr": ["EEPROM RDRAM location:", "EEPROM size:",
		                                "Flash RDRAM location:", "Flash size:",
		                                "SRAM RDRAM location:", "SRAM size:",
		                                "Controller Pak 0 RDRAM location:",
		                                "Controller Pak 1 RDRAM location:",
		                                "Controller Pak 2 RDRAM location:",
		                                "Controller Pak 3 RDRAM location:",
		                                "Controller Pak size:", "osRomBase:",
		                                "osTvType:", "osMemSize:",
		                                "Unknown value #3:", "Unknown value #4:",
		                                "Magic:", "Number of .u0x files:",
		                                "Thumb image length:", "Title image length:",
		                                "Thumb image:", "Title image:", "Title/ISBN",
		                                "Padding:", "Certificate Authority CRL version:",
		                                "Content Protection CRL version:", "Size:",
		                                "Unknown value #5:", "Titlekey IV:",
		                                "SHA-1 hash of plaintext:", "Content IV:",
		                                "Exec flags:", "Hardware access rights:",
		                                "Allowed SK calls:", "CMD BBID:", "CMD certificate:",
		                                "CID:", "Titlekey:", "Signature:", "Ticket BBID:",
		                                "Ticket ID:", "Type of trial:",
		                                "Minutes or launches for trial:", "Padding:",
		                                "Ticket CRL version:", "Titlekey IV 2:",
		                                "ECC public key:", "Ticket certificate:", "Signature:"],
		                         "de": ["EEPROM RDRAM location:", "EEPROM size:",
		                                "Flash RDRAM location:", "Flash size:",
		                                "SRAM RDRAM location:", "SRAM size:",
		                                "Controller Pak 0 RDRAM location:",
		                                "Controller Pak 1 RDRAM location:",
		                                "Controller Pak 2 RDRAM location:",
		                                "Controller Pak 3 RDRAM location:",
		                                "Controller Pak size:", "osRomBase:",
		                                "osTvType:", "osMemSize:",
		                                "Unknown value #3:", "Unknown value #4:",
		                                "Magic:", "Number of .u0x files:",
		                                "Thumb image length:", "Title image length:",
		                                "Thumb image:", "Title image:", "Title/ISBN",
		                                "Padding:", "Certificate Authority CRL version:",
		                                "Content Protection CRL version:", "Size:",
		                                "Unknown value #5:", "Titlekey IV:",
		                                "SHA-1 hash of plaintext:", "Content IV:",
		                                "Exec flags:", "Hardware access rights:",
		                                "Allowed SK calls:", "CMD BBID:", "CMD certificate:",
		                                "CID:", "Titlekey:", "Signature:", "Ticket BBID:",
		                                "Ticket ID:", "Type of trial:",
		                                "Minutes or launches for trial:", "Padding:",
		                                "Ticket CRL version:", "Titlekey IV 2:",
		                                "ECC public key:", "Ticket certificate:", "Signature:"],
		                         "it": ["EEPROM RDRAM location:", "EEPROM size:",
		                                "Flash RDRAM location:", "Flash size:",
		                                "SRAM RDRAM location:", "SRAM size:",
		                                "Controller Pak 0 RDRAM location:",
		                                "Controller Pak 1 RDRAM location:",
		                                "Controller Pak 2 RDRAM location:",
		                                "Controller Pak 3 RDRAM location:",
		                                "Controller Pak size:", "osRomBase:",
		                                "osTvType:", "osMemSize:",
		                                "Unknown value #3:", "Unknown value #4:",
		                                "Magic:", "Number of .u0x files:",
		                                "Thumb image length:", "Title image length:",
		                                "Thumb image:", "Title image:", "Title/ISBN",
		                                "Padding:", "Certificate Authority CRL version:",
		                                "Content Protection CRL version:", "Size:",
		                                "Unknown value #5:", "Titlekey IV:",
		                                "SHA-1 hash of plaintext:", "Content IV:",
		                                "Exec flags:", "Hardware access rights:",
		                                "Allowed SK calls:", "CMD BBID:", "CMD certificate:",
		                                "CID:", "Titlekey:", "Signature:", "Ticket BBID:",
		                                "Ticket ID:", "Type of trial:",
		                                "Minutes or launches for trial:", "Padding:",
		                                "Ticket CRL version:", "Titlekey IV 2:",
		                                "ECC public key:", "Ticket certificate:", "Signature:"]		                         }
		
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

		if len(sys.argv) > 1:
			self.openFile(path = sys.argv[1])
		
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
			messagebox.showerror(self.textvars[0].get(), self.textvars[31].get().format(self.byteArrayToHexInt(binaryData[0x44:0x47], digits = 6)))
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
		dec = iter(zlib.decompress(data, -15))
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

		img = PIL.Image.frombytes("RGBA", imgSize, bytes(dtex))
		return PIL.ImageTk.PhotoImage(img)			

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

	def pngToDeflated(self, data, isTitle = False):
		image = iter(data)

		firstTime = True

		new = bytearray()

		if isTitle:

			for i in image:

				grey0 = i
				grey1 = next(image)
				grey2 = next(image)
				alpha = next(image)
				if (grey1 != grey0 or grey2 != grey0) and firstTime:
					firstTime = False
					messagebox.showwarning(self.textvars[0].get(), self.textvars[41].get())
				if alpha:
					intensity = grey0
				else:
					intensity = 0
				new.extend([intensity, alpha]) # it's literally just IA16... thanks Cuyler

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

		comp = zlib.compressobj(method = zlib.DEFLATED)
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
					messagebox.showerror(self.textvars[0].get(), (self.textvars[43].get()).format(self.splitnamevars[i].get(), j.get(), self.ticketSplitOffsets[i + 1] - self.ticketSplitOffsets[i]))						
					return 1
			else:
				newTikList.append(None)

		newTikList[16] = bytearray(b'CAM')

		newTikList[20:22] = self.curImagesBytes

		offsets = [self.byteArrayToInt(newTikList[18]), self.byteArrayToInt(newTikList[19])]

		if offsets[0] != len(newTikList[20]) or offsets[1] != len(newTikList[21]):
			messagebox.showerror(self.textvars[0].get(), self.textvars[44].get())
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
			messagebox.showerror(self.textvars[0].get(), self.textvars[45].get())
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

		imageBytes = PIL.Image.open(path).convert("RGBA").tobytes()

		data = self.pngToDeflated(imageBytes, isTitle = isTitle)

		if isTitle:
			self.curImagesBytes[1] = data + b'\x00' * 2
			self.widgets[19].set(hex(len(data) + 2).lstrip("0x").zfill(4))
		else:
			self.curImagesBytes[0] = data + b'\x00' * 2
			self.widgets[18].set(hex(len(data) + 2).lstrip("0x").zfill(4))

		self.populateOptions(index = self.lastTikIndex)

	def newTicketSys(self, event = None):
		self.tikBinData = [bytearray(zlib.decompress(self.defaultTik, -15))]

		self.numTickets = 1
		self.lastTikIndex = None
		self.srcPath = None
		self.savePath = None
		self.reloadNames(delete = True)
		self.filemenu.entryconfig(2, state = "normal")
		self.filemenu.entryconfig(3, state = "normal")
		self.populateOptions(index = 0)

	def newTicket(self, event = None):
		self.tikBinData.append(bytearray(zlib.decompress(self.defaultTik, -15)))
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
			messagebox.showerror(self.textvars[0].get(), self.textvars[50].get())
			return
		if not messagebox.askyesno(self.textvars[0].get(), self.textvars[51].get().format(self.tikNamesUnicode[self.lastTikIndex][0])):
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
			messagebox.showerror(self.textvars[0].get(), self.textvars[54].get().format(self.byteArrayToHexInt(tikData[0x40:0x43], digits = 6)))			
			return
		if len(tikData) != 0x2B4C:
			messagebox.showerror(self.textvars[0].get(), self.textvars[55].get())
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
		extension = os.path.splitext(temp)[1]
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
		temp = askopenfilename(title = self.textvars[58].get(), filetypes = [(self.textvars[56].get(), (".cdesc")), (self.textvars[57].get(), (".cmd")), (self.textvars[59].get(), (".bin")), (self.textvars[30].get(), (".*"))])
		if not temp:
			return
		newData = bytearray(open(temp, "rb").read())
		if newData[0x40:0x43] != b'CAM':
			messagebox.showerror(self.textvars[0].get(), self.textvars[54].get().format(self.byteArrayToHexInt(newData[0x40:0x43], digits = 6)))			
			return		
		if len(newData) not in [0x2800, 0x29AC, 0x2B4C]:
			if not messagebox.askyesno(self.textvars[0].get(), self.textvars[60].get().format(hex(len(newData)))):
				return
		if len(newData) == 0x2B4C:
			if messagebox.askyesno(self.textvars[0].get(), self.textvars[61].get()):
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
		json.dump(self.settings, open(self.saveDataPath, "w"))

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
		self.langmenu.entryconfig(2, label = self.textvars[69].get())
		self.langmenu.entryconfig(3, label = self.textvars[70].get())
		self.langmenu.entryconfig(4, label = self.textvars[71].get())
		
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