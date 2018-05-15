from secretary import Meeting_generator
import subprocess
from officer import get_quarter
from datetime import datetime
import sys
import os


'''
	- if first keyword is 'make', the program creates a word document from 
		secretary.py and opens it
	- if second keyword is a date in the format '2018.04.20' (zero padded, YYYY/MM/DD) it will 
		instead open that file if it exists
	- if no second keyword is given, it will create the word document with today's attendance 

	ex: "python main.py make 2018.04.20"
	assuming today isn't 4/20, this will open the document 2018.04.20.docx

	ex: "python main.py make today"
	- if a word document was previously created today, it will open that document
	- if no word document exists for today, this will create a document with today's date, 
	and with attendance info for today from the google sheets API

	== is value equality operator, while 'is' is reference equality (if it points to the same object)

'''



'''
	- sys.argv[2] is a string following the format YYYY.MM.DD
	- meeting_date is a datetime object to be used in secretary/meeting_generator file
	- if a date is passed into sys.argv[2] it should be used as file_name, but if 'today' is passed in 
	we need to pass in a string formatted version of today's date as a datetime object in the syntax the 
	program expects
'''


#this just checks if its in YYYY.MM.DD format so i don't have to do it with regex
'''
	if the date is in another quarter, directory changes
	if it is 'today', it doesn't
	if sys.argv[2] == 'today' then try block wouldn't work
'''

path_to_folder = ''
file_name = sys.argv[2]

if sys.argv[1] == 'make':

	if sys.argv[2] == 'today':
		meeting_date = datetime.now()
		#change file_name, as it was previously == sys.argv[2], which was 'today', which isn't valid file name
		file_name = meeting_date.strftime('%Y.%m.%d')
		path_to_folder += get_quarter(meeting_date) + '/'

		#if file does not exist, create it. if file does, skip creation step and open it instead
		if not os.path.isfile(path_to_folder + file_name):
			meeting_generator = Meeting_generator(path_to_folder, meeting_date)
		else:
			print 'there is already a file created for today, opening it now...'

	else:
		#this just checks if its in YYYY.MM.DD format so i don't have to do it with regex
		#and updates path_to_file
		try: 
			meeting_date = datetime.strptime(sys.argv[2], '%Y.%m.%d')	
			path_to_folder += get_quarter(meeting_date) + '/'
		except ValueError:
			print sys.argv[2], ' is not in the format \'YYYY.MM.DD\' (ex: 2018.04.20)'
			sys.exit(1)
		print 'there is already a file created for', file_name, 'opening it now...'

	process = subprocess.Popen(['open', path_to_folder + file_name + '.docx'])