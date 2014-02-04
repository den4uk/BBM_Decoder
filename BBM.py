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
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
import sqlite3 as sq
from datetime import datetime
from datetime import timedelta

root = Tk()
version = '0.1'
root.title('BBM Decoder {0}'.format(version))

def aboutmsg():
	messagebox.showinfo('BBM Decoder version: {0}'.format(version), 'Decodes Android and Apple BBM \'master.db\' files into a single HTML report.\nhttp://android.saz.lt\nCopyright 2012-14')

Input = StringVar()
Output = StringVar()
Result = StringVar()

def dir_com():
	Input.set(filedialog.askopenfilename(initialfile='master.db'))

def out_file():
	Output.set(filedialog.asksaveasfilename(initialfile='BlackberryMessenger.html'))

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
        except:
                Result.set('Error! No Input or Output selected!')

menubar = Menu(root)
root['menu'] = menubar
menubar.add_command(label='Exit', underline=1, command=root.destroy)
menubar.add_command(label='About', underline=0, command=aboutmsg)

mainframe = ttk.Frame(root, padding="5 5 15 15")
mainframe.grid(row=0, column=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

Font1 = font.Font(weight='bold', size=10)
Font2 = font.Font(weight='bold', size=8)
ttk.Label(mainframe, font=Font1, text='\
1. For \'Input\': Choose the \'master.db\' file\n\
2. For \'Output\': Choose the reporting file\n\
3. Press \'Decode\' to proceed\
').grid(row=0, columnspan=2, sticky=W)

ttk.Button(mainframe, text='Input', command=dir_com).grid(row=1, column=0, sticky=W)
ttk.Label(mainframe, textvariable=Input).grid(row=1, column=1, sticky=W)
ttk.Button(mainframe, text='Output', command=out_file).grid(row=2, column=0, sticky=W)
ttk.Label(mainframe, textvariable=Output).grid(row=2, column=1, sticky=W)

ttk.Button(mainframe, text='DECODE!', command=decode_masterdb).grid(row=3, column=0, sticky=W)
ttk.Label(mainframe, font=Font2, textvariable=Result).grid(row=3, column=1, sticky=(W,E))

root.mainloop()
