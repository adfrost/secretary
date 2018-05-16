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

		self.db = create_engine('sqlite:///testdb.db', echo=False)
		Base.metadata.create_all(self.db)
		
		try:
			self.db.connect()
			Session = sessionmaker(bind=self.db)
			self.session = Session()
			print 'connected and session object created!!!'
		except:
			print 'something didnt work :( \n\n\n'
		

		#adds new fields to the tables every time,
		#should make it only add if no data is present or update
		#self.populate_tables()	

	def populate_officers(self):
		self.a = Officer(position='Treasurer')
		self.b = Officer(position='Recruitment Director')
		self.c = Officer(position='Member Educator')
		self.d = Officer(position='Scholarship')
		self.e = Officer(position='Alumni Director')
		self.f = Officer(position='Secretary')
		self.g = Officer(position='Marshal')
		self.h = Officer(position='Sergeant-at-Arms')
		self.i = Officer(position='President')
		self.j = Officer(position='Vice President')
		
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
		self.populate_directors()
		self.populate_officers()

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


	

		
	