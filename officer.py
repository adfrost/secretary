'''
	- a level of indirection to easily iterate over all officer positions and group the two paragraphs that each require
	- otherwise, there would be no differentiation between a 'paragraph' for an officer's position and name, and the report
	
'''
from docx.shared import Pt
from docx import Document


class Officer:

	def __init__(self, document, position):

		'''
			could make a scraper crawl through the portal, 
			or host everything locally and have it occasionally compare with the portal
		self.incumbent = get_officer_name(position)

		'''

		self.incumbent = position[0] + ' (' + position[1] + '):'

		self.officer = document.add_paragraph(style = 'List Paragraph')
		self.officer.paragraph_format.space_after = Pt(0)
		self.officer.add_run(self.incumbent).bold = True
		

		self.report = document.add_paragraph('Report: ', style = 'List Bullet 3')
		self.report.paragraph_format.space_after = Pt(6)
		
