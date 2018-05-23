import sqlalchemy as sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

Base = declarative_base()	#used by User class, must be here or script won't run
class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	
	directorship = relationship('Director', back_populates='user')
	officer = relationship('Officer', back_populates='user')

	def __repr_(self):
		return "<User(id='%s', name='%s')>" % (
			self.id, self.name)

class Director(Base):
	__tablename__ = 'directors'
	id = Column(Integer, primary_key=True)
	position = Column(String)
	user_id = Column(Integer, ForeignKey('users.id'))

	user = relationship('User', back_populates='directorship')

	def __repr_(self):
		return "<Director(id='%s', position='%s')>" % (
			self.id, self.position)


'''
	Note: user variable was causing sqlalchemy.exc.InvalidRequestError 
	when back_populates parameter was 'officers', the name of the table.
	changing it to 'officer', which is the same name of the parameter
	in User. that fixed it i think
'''

class Officer(Base):
	__tablename__ = 'officers'
	id = Column(Integer, primary_key=True)
	position = Column(String)
	user_id = Column(Integer, ForeignKey('users.id'))

	user = relationship('User', back_populates='officer')

	def __repr_(self):
		return "<Officers(id='%s', position='%s')>" % (
			self.id, self.position)

class DB:
	def __init__(self):


		self.db = create_engine('sqlite:///testdb.db', echo=True)
		Base.metadata.create_all(self.db)
		
		try:
			self.db.connect()
			Session = sessionmaker(bind=self.db)
			self.session = Session()
			print 'connected and session object created!!!'
		except:
			print 'something didnt work :( \n\n\n'
		
		officer_dict = {
			'treasurer': 		'Treasurer',
			'recruitment_dir':	'Recruitment Director',
			'nember_ed': 		'Member Educator',
			'scholarship_dir': 	'Scholarship',
			'alumni_dir': 		'Alumni Director',
			'secretary': 		'Secretary',
			'marshal': 			'Marshal',
			'sergeant': 		'Sergeant-at-Arms',
		}

		director_dict = {
			'brotherhood_dir': 	'Brotherhood Director',
			'social_dir': 		'Social Director',
			'philo_dir': 		'Philanthropy Director',
			'athletics_dir':	'Athletics Director',
			'health_safety': 	'Health & Safety',
			'housing_manager':	'Housing Manager' ,
			'wellness_dir':		'Wellness Director',
			'communitiy_dir':	'Community Service Director',
			'fundraising_dir':	'Fundraising Director',
			'sunshine_dir':		'Sunshine Director',
		}

		'''
			want these to be separate from the officer/director minutes section
			should these be in separate tables? seems inefficient to have 2 tables 
			with only one entry in each
		'''
		president = {'president': 'President',}
		vice_president = {'vice_president':	'Vice President',}
		
	def populate_officers(self):
		self.treasurer = Officer(position='Treasurer')
		self.recruitment_dir = Officer(position='Recruitment Director')
		self.nember_ed = Officer(position='Member Educator')
		self.scholarship_dir = Officer(position='Scholarship')
		self.alumni_dir = Officer(position='Alumni Director')
		self.secretary = Officer(position='Secretary')
		self.marshal = Officer(position='Marshal')
		self.sergeant = Officer(position='Sergeant-at-Arms')
		self.president = Officer(position='President')
		self.vice_president = Officer(position='Vice President')
		
	def populate_directors(self):
		self.aa = Director(position='Brotherhood Director')
		self.bb = Director(position='Social Director')
		self.cc = Director(position='Philanthropy Director') 
		self.dd = Director(position='Athletics Director')
		self.ee = Director(position='Health & Safety')
		self.ff = Director(position='Housing Manager') 	
		self.gg = Director(position='Wellness Director')
		self.hh = Director(position='Community Service Director')
		self.ii = Director(position='Fundraising Director')
		self.jj = Director(position='Sunshine Director')


	def populate_tables(self):
		


		self.session.add_all([
			User(name = '', officer=[], director=[]),
			])
		
		self.session.commit()


	def get_officers(self):
		query = self.session.query(Officer).all()
		return [(officer.position, officer.user.name ) for  officer in query]


	def get_directors(self):
		query = self.session.query(Director).all()
		return [(director.position, director.user.name ) for  director in query]


	#set foreign key for a position and a user to nothing?
	#position is a string of the full, official title of the position
	#would make it a lot easier to find objects if i made 'position' a Officer/Director object
	def remove_link(self,position,name):
		
		usr = self.session.query(User).filter_by(name=name).all()[0]
		import ipdb;ipdb.set_trace()


		if position in officer_dict:
			query = self.session.query(Officer).filter_by(position=position).all() #should only ever be unique entries
		elif position in dir_dict:
			query = self.session.query(Director).filter_by(position=position).all() #should only ever be unique entries
		else:
			print 'ERROR THAT ISNT AN OFFICER OR DIRECTOR POSITION'

		if len(query) > 1:
			print 'ERROR THERE ARE 2 ENTRIES FOR THE SAME POSITION'
			exit(1)

		#correct way to unlink foreign key?
		query[0].user = None
		print 'successfully unlinked'



ayy = DB()
		
	