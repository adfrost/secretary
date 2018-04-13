"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime


class Attendance_API:


	def __init__(self):
		# Setup the Sheets API
		SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
		store = file.Storage('credentials.json')
		creds = store.get()
		if not creds or creds.invalid:
			flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
			creds = tools.run_flow(flow, store)
		self.service = build('sheets', 'v4', http=creds.authorize(Http()))
		self.SPREADSHEET_ID = '1pi9vYiuaffClEK2TrIwg1N-HtcL4uU-S9nP8RcJ1IqM'


#returns the exact string to match the column of the meeting today
#used to easily grab column of the day
	def get_today_string(self, date=None):
		if date:
			return 'Meeting - ' + date
		else:
			return 'Meeting - ' + datetime.now().strftime('%m/%d')


	#date is a list where first element is the date of the meeting as a string
	#followed by attendance
	def get_today_column(self, attendance, prev_date):
		for date in attendance['values']:
			if date[0] == self.get_today_string(prev_date):
				date.remove('')		#the 'pledges' row has a blank in this space, want it to match up with the members tuple
				return date

#returns list of tuples with first,last name of all current members
	def build_member_tuple(self):
		test = self.service.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID, majorDimension='ROWS',range='A2:B').execute()
		test['values'].remove(['Pledges'])	#all other entries in 'test' were 2d lists except this row in the spreadsheet. was causing issues
		return [(first,last) for last,first in test['values'] if first[0] != 'Pledges']



#setting majorDimension as COLUMNS groups each meeting as a list, so no chance the order is disrupted, like in a dictionary
#optionally passing a date of type string in day/month zero padded format grabs it for that day
	def get_today_attendance(self, date=None):
		attendance = self.service.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID, majorDimension='COLUMNS',range='C1:AA').execute()
		today_column = self.get_today_column(attendance,date)
		current_members = self.build_member_tuple()

		attendance_list = []
		for (member, status) in zip(current_members,today_column[1:]):
			if status == 'X':
				attendance_list.append(member)
		return attendance_list