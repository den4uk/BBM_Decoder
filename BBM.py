#!/usr/bin/env python3

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Copyright (C) 2012-2014  Denis Sazonov  http://android.saz.lt
#
# This program is free software: you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

from tkinter import Tk,StringVar,Menu,Button,Label,N,E,W,S
from tkinter import PhotoImage
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
import sqlite3 as sq
from datetime import datetime
from datetime import timedelta
from webbrowser import open_new_tab

__version__ = '0.1'
__author__ = 'Denis Sazonov'

def unix_to_utc(unix_stamp):
	return datetime.utcfromtimestamp(int(str(unix_stamp)[:10])).strftime('%Y-%m-%d %H:%M:%S UTC')

def decode_masterdb():
        try:
                con = sq.connect(Input.get())
                c = con.cursor()
                bbm_data = c.execute("SELECT TextMessageId, UserPins.Pin, IsInbound, TextMessages.Timestamp, Content, PictureTransferId, Users.DisplayName, Type, TextMessages.ConversationId FROM TextMessages JOIN Participants ON (TextMessages.ParticipantId=Participants.ParticipantId) JOIN UserPins ON (Participants.UserId=UserPins.UserId) JOIN Users ON (Participants.UserId=Users.UserId) ORDER BY TextMessages.Timestamp DESC").fetchall()
                bbm_convs = c.execute("SELECT UserPins.Pin,ConversationId FROM Participants JOIN UserPins ON (Participants.UserId=UserPins.UserId)").fetchall()
                fileh = open(Output.get(), 'w', encoding='UTF-8')
                fileh.write('<!DOCTYPE html>\n<html><head><meta charset="UTF-8">\n<title>Blackberry Messenger Chat</title>\n<style>body,td,tr {font-family: Vernada, Arial, sans-serif; font-size: 12px;}</style></head>\n<body>\n<p align="center"><i># This report was generated using Andriller #</i></p>\n<h3 align="center">Blackberry Messenger</h3>\n<table border="1" cellpadding="2" cellspacing="0" align="center">\n<tr bgcolor="#72A0C1">\n\
            <th>#</th>\
                <th>Sender Name</th>\
            <th nowrap>Sender PIN</th>\
                <th>Recipient PIN</th>\
                <th width="300">Message</th>\
                <th nowrap>Type</th>\
                <th nowrap>Time</th>\
                </tr>\n')
                for bbm_item in bbm_data:
                        bbm_msgid = str(bbm_item[0])
                        bbm_msgpin = str(bbm_item[1])
                        if bbm_item[2] == 1:
                                bbm_msgtype = 'Inbox'
                        else:
                                bbm_msgtype = 'Sent'
                        bbm_msgtime = unix_to_utc(bbm_item[3])
                        bbm_msgtxt = str(bbm_item[4])
                        if bbm_item[5] != None:
                                bbm_msgimg = str('<i>Image #')+str(bbm_item[5])+str('</i>')
                        else:
                                bbm_msgimg = ''
                        bbm_namepin = bbm_item[6]
                        if bbm_item[7] == 1:
                                bbm_mtype = 'PING!'
                        else:
                                bbm_mtype = ''
                        bbm_parts = []
                        for bbm_conv in bbm_convs:
                                if bbm_conv[1] == bbm_item[8]:
                                        bbm_parts.append(bbm_conv[0])
                        bbm_parts.remove(bbm_msgpin)
                        bbm_parts = '<br/>'.join(bbm_parts)
                        fileh.write('<tr>\
                <td>{0}</td>\
                <td nowrap>{5}</td>\
                <td>{1}</td>\
                <td>{8}</td>\
                <td width="300">{2}{6}{7}</td>\
                <td nowrap>{3}</td>\
                <td nowrap>{4}</td>\
                </tr>\n'.format(
                bbm_msgid,		#0
                bbm_msgpin,		#1
                bbm_msgtxt,		#2
                bbm_msgtype,	#3
                bbm_msgtime,	#4
                bbm_namepin,	#5
                bbm_msgimg,		#6
                bbm_mtype,		#7
                bbm_parts,		#8
                ))
                fileh.write('</table>\n<p align="center"><i># <a href="http://android.saz.lt" target="_blank">http://android.saz.lt</a> #</i></p>\n</body></html>')
                fileh.close()
                Result.set('Decoded {0} messages'.format(len(bbm_data)))
                try:
                        open_new_tab(Output.get())
                except:
                        pass
        except:
                Result.set('ERROR!')


androidlogo = '''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'''
applelogo = '''R0lGODlhJwAwAIABAJCYoP///yH5BAEKAAEALAAAAAAnADAAAAKDjI+pCrAPY2hN2kjp3SlrznkVGIrkJjrnla6s51pmLGX0fbZPOmL8Z/jZdsLib2FM8jrK5jDojDKjyinVyLgms1oht3u0gnWIsVdsfh7SSzRbVX7D3OyvvLe+A/N6/KS/9wfYMzhUCHQYN0iXZieHpAdx5/NWUydjVjKjuKkJR+SHUAAAOw=='''
bbmlogo = '''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'''

root = Tk()
root.title('BBM Decoder {0} \u00A9 2014'.format(__version__))
#root.geometry("450x150")
root.resizable(0,0)

def aboutmsg():
	messagebox.showinfo('\
Forensic BBM Decoder version: {0} \u00A9 2014'.format(__version__), '\
Forensic BBM Decoder version: {0}\n\
Decodes \'master.db\' files into a single HTML report.\n\
\'master.db\' file from Android or iPhone Blackberry Messenger.\n\
\u00A9 2014 Copyright\n\
http://android.saz.lt\n\
Author: Denis Sazonov\n\
E-mail: den@saz.lt'.format(__version__))

Input = StringVar()
Output = StringVar()
Result = StringVar()

def dir_com():
	Input.set(filedialog.askopenfilename(initialfile='master.db'))

def out_file():
	Output.set(filedialog.asksaveasfilename(initialfile='BBM_Chat.html'))              

menubar = Menu(root)
root['menu'] = menubar
menubar.add_command(label='Exit', underline=1, command=root.destroy)
menubar.add_command(label='About', underline=0, command=aboutmsg)

mainframe = ttk.Frame(root, padding="5 5 15 15")
mainframe.grid(row=0, column=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

inframe = ttk.Frame(mainframe)
inframe.grid(row=0, column=0, sticky=(N, W, E, S))

downframe = ttk.Frame(mainframe)
downframe.grid(row=1, sticky=(N, W, E, S))

Font1 = font.Font(weight='bold', size=9)

ttk.Label(inframe, font=Font1, text='\
1. For \'Input\': Choose the \'master.db\' file\n\
2. For \'Output\': Choose the reporting file\n\
3. Press \'Decode\' to proceed\
').grid(row=0, column=0, sticky=W)

ImageBBM = PhotoImage(data=bbmlogo)
ImageAND = PhotoImage(data=androidlogo)
ImageIOS = PhotoImage(data=applelogo)
ttk.Label(inframe, image=ImageBBM).grid(row=0, column=1, sticky=W+S)
ttk.Label(inframe, image=ImageAND).grid(row=0, column=2, sticky=W+S)
ttk.Label(inframe, image=ImageIOS).grid(row=0, column=3, sticky=W+N)

ttk.Button(downframe, text='Input', command=dir_com).grid(row=0, column=0, sticky=W)
ttk.Label(downframe, textvariable=Input).grid(row=0, column=1, sticky=W)
ttk.Button(downframe, text='Output', command=out_file).grid(row=1, column=0, sticky=W)
ttk.Label(downframe, textvariable=Output).grid(row=1, column=1, sticky=W)

ttk.Button(downframe, text='DECODE', command=decode_masterdb).grid(row=2, column=0, sticky=W)
ttk.Label(downframe, font=Font1, textvariable=Result).grid(row=2, column=1, sticky=(W,E))

root.mainloop()
