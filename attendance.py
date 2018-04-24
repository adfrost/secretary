"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime
from SheetsClass import Spreadsheet

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

		#also need the sheetID, which relies on the current quarter
		self.SPREADSHEET_ID = '1pi9vYiuaffClEK2TrIwg1N-HtcL4uU-S9nP8RcJ1IqM'
		self.quarter = self.get_current_quarter()
		
		sheet_metadata = self.service.spreadsheets().get(spreadsheetId=self.SPREADSHEET_ID).execute()
		
		#sheets = sheet_metadata.get('sheets', '')
		#title = sheets[0].get("properties", {}).get("title", "Sheet1")
		#sheet_id = sheets[0].get("properties", {}).get("sheetId", 0)
		self.API_response = self.service.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID, majorDimension='COLUMNS',range=self.quarter + '!A:AA').execute()
		#self.API_current_members = self.service.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID, majorDimension='COLUMNS',range=self.quarter + '!A:B').execute()
		a = Spreadsheet(self.API_response)
		

	def get_current_quarter(self):
		date = datetime.now()
		quarter = ""
		if date.month >= 9:
			quarter = "Fall "
		elif date.month <= 3:
			quarter = "Winter "
		elif 4 <= date.month <= 7:
			quarter = "Spring "
		else:
			print("error, current date is in summer")
			quarter = "ERROR "

		return quarter + str(date.year)


#returns the exact string to match the column of the meeting today
#used to easily grab column of the day
	def get_today_as_string(self, date=None):		
		if date:
			return 'Meeting - ' + date
		else:
			return 'Meeting - ' + datetime.now().strftime('%m/%d')


	#date is a list where first element is the date of the meeting as a string
	#followed by attendance
	def get_today_column(self, attendance, prev_date):
		for date in attendance['values']:
			if date[0] == self.get_today_as_string(prev_date):
				'''
					current issue is there is a row titled 'pledges' that i have to hard code to get around
				'''
				#should probably make every cell an object
				#date.remove('')		#the 'pledges' row has a blank in this space, want it to match up with the members tuple
				return date

#returns list of tuples with first,last name of all current members
	def build_member_tuple(self):
		test = self.service.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID, majorDimension='ROWS',range=self.quarter + '!A2:B').execute()
		test['values'].remove(['Pledges'])	#all other entries in 'test' were 2d lists except this row in the spreadsheet. was causing issues
		return [(first,last) for last,first in test['values'] if first[0] != 'Pledges']


#setting majorDimension as COLUMNS groups each meeting as a list, so no chance the order is disrupted, like in a dictionary
#optionally passing a date of type string in day/month zero padded format grabs it for that day
	def get_today_attendance(self, date=None):

	

		today_column = self.get_today_column(self.API_response,date)
		current_members = self.build_member_tuple()
		


		attendance_list = []
		for (member, status) in zip(current_members,today_column[1:]):
			if status == 'X':
				attendance_list.append(member)
		return attendance_list