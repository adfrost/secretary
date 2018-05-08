
'''
	base class
	

	holds an individual cell, that could contain one of the following:
	- person's first or last name
	- date of a meeting
	- attendance of a person at a meeting
'''
class Sheet_cell:
	def __init__(self, content):
		self.content = content

	def return_content():
		return self.content

'''
	holds the attendance of all members during a given meeting
	consists of a date, and a dictionary "attendance_dict" of "member_name":"attendance status"
	where member_name is a Name object, and attendance status could be a bool i guess?
'''
class Meeting:
	def __init__(self, attendance, date,):
		self.date 
		self.attendance_dict = {}



class Name:
	def __init__(self,last_name,first_name):
		self.last = last_name
		self.first = first_name
	
'''
class Last_name:
	def __init__(self, last_name):
		Sheet_cell.__init__
		pass

class First_name:
	def __init__(self):
		pass
'''

class Spreadsheet:

	def __init__(self,response):
		self.range = response['range']
		Sheet_cell
		try:
			response['values'][0].remove('Pledges')
		except:
			print("ERROR: no entry 'Pledges' in API response")
		names_list = []

		
		
		for last, first in zip(response['values'][0],response['values'][1]):
			names_list.append(Name(last,first))


