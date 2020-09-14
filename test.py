#!/usr/bin/python

import sqlite3, random, string, datetime
# ACCT_LIST = ['aaa']
# class Policyholder_Data():
# 	def __init__(self, DB_NAME):

# 		# connect to sqlite db
# 		self.db_name = '{}.db'.format(DB_NAME)
# 		self.conn = sqlite3.connect(self.db_name)
# 		self.cursor = self.conn.cursor()

# 	def make_account_number(self):
# 		''' 
# 		randomly generate a new account number
# 		'''
		
# 		acctno = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))
# 		if acctno in ACCT_LIST:
# 			self.make_account_number()
# 		else:
# 			print(acctno)
# 			return acctno

# pol = Policyholder_Data('sample')
# pol.make_account_number()

def make_date(start, end):
	'''
	make random date in format yyyy-mm-dd in between start and end dates
	@input: start date given in tuple format (yyyy, mm, dd)
	@input: end date given in tuple format (yyyy, mm, dd)
	@return: random date

	'''
	try:
		start_date = datetime.date(start[0], start[1], start[2])
		end_date = datetime.date(end[0], end[1], end[2])
	except:
		print("Invalid date input, creating random date")
		start_date = datetime.date(1950,1,1)
		end_date = datetime.date(2003,12,31)

	time_between_dates = end_date - start_date
	days_between_dates = time_between_dates.days
	random_number_of_days = random.randrange(days_between_dates)
	random_date = start_date + datetime.timedelta(days=random_number_of_days)

	print(random_date)

	return random_date

print(tuple('a') + ('a', 'b'))