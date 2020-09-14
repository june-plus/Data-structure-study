import sqlite3
import random, string, datetime



# initial set up
DB_NAME = 'INSURANCE_DATABASE'

ACCT_LIST = []
SSN_LIST = []

# date of valuation in yyyy-mm-dd; Only losses recorded previous to this date will show
VALUATION_DATE = "2020-09-13"


# helper functions
def make_date(start, end):
	'''
	make random date in format yyyy-mm-dd in between start and end dates
	@input: start date given in tuple or list format (yyyy, mm, dd)
	@input: end date given in tuple or list format (yyyy, mm, dd)
	@return: random date

	'''
	try:
		start_date = datetime.date(start[0], start[1], start[2])
		end_date = datetime.date(end[0], end[1], end[2])
	except:
		# print("Invalid date input, creating random date")
		start_date = datetime.date(1950,1,1)
		end_date = datetime.date(2003,12,31)

	time_between_dates = end_date - start_date
	days_between_dates = time_between_dates.days
	random_number_of_days = random.randrange(days_between_dates)
	random_date = start_date + datetime.timedelta(days=random_number_of_days)

	# print(random_date)

	return random_date

'''
Policy Data class
'''
class Policyholder():
	def __init__(self):
		'''
		policyholder's information
		'''
		self.account_number = self.make_account_number()
		self.sex = random.choice(["M", "F"])
		self.dob = make_date(0,0)
		self.ssn = self.make_ssn()
		self.allergies = random.choice(["none", "single", "multiple"])
		self.medical_conditions = random.choice(["none", "single", "multiple"])
		self.claim_count = 0
		self.claim_list = []

		self.properties = (self.account_number, self.sex, self.dob, self.ssn, self.allergies, self.medical_conditions)
		#print(self.properties)

	def make_account_number(self):
		''' 
		randomly generate a new account number if it does not exist in global list of account numbers yet using recursion
		@return: account number
		'''
		acctno = ''.join(random.choice(string.digits) for x in range(10))
		if acctno in ACCT_LIST:
			self.make_account_number()
		else:
			return acctno

	def make_ssn(self):
		''' 
		randomly generate a new ssn if it does not exist in global list of ssn using recursion
		@return: social security number in format ###-##-####
		'''
		first = random.randint(100,999)
		second = random.randint(10,99)
		third = random.randint(1000,9999)
		ssn = "{}-{}-{}".format(first, second, third)
		if ssn in SSN_LIST:
			self.make_ssn()
		else:
			return ssn

	def make_claim(self):
		'''
		make a claim and link to policyholder
		'''
		claim_number = self.claim_count
		# print(self.claim_list)
		if claim_number in self.claim_list:
			self.make_claim()
		else:
			lossdate = make_date((self.dob.year, self.dob.month, self.dob.day), VALUATION_DATE.split("-"))
			losstype = random.choice(["surgery", "medication", "emergency", "hospital"])
			billed_amt = round(random.uniform(0, 30000),2)
			covered_amt = round(random.uniform(0, billed_amt),2)
			clm = Claim(lossdate, losstype, billed_amt, covered_amt)
			self.claim_count += 1
			self.claim_list.append(claim_number)

			return (claim_number, lossdate, losstype, billed_amt, covered_amt)

	def __str__(self):
		return '\nAcct No.: {} \nSex: {} \nDate of Birth: {} \nSSN: {} \nAllergies: {} \
		\nMedical Conditions: {}\n'.format(self.account_number,self.sex,self.dob,self.ssn,self.allergies,self.medical_conditions)
	

class Claim():
	def __init__(self, lossdate = None , losstype = None, billed_amt=0, covered_amt=0):
		self.lossdate = lossdate
		self.losstype = losstype
		self.billed_amt = billed_amt
		self.covered_amt = covered_amt


class InsuranceDB():
	def __init__(self, db_name):
		self.db_name = '{}.db'.format(db_name)

		try:
			self.conn = sqlite3.connect(self.db_name)
			self.cursor = self.conn.cursor()
			print('connnected to database {}'.format(db_name))
		except:
			print('database connection error; try again.')

	def make_tables(self):

		query = '''
		DROP TABLE IF EXISTS 'Accounts';
		'''
		self.cursor.execute(query)

		query = '''
		DROP TABLE IF EXISTS 'Claims';
		'''
		self.cursor.execute(query)

		# create Accounts table
		query = '''create table 'Accounts'(
							Id INTEGER PRIMARY KEY AUTOINCREMENT,
							AccountNumber INTEGER NOT NULL ,
							Sex TEXT ,
							DOB DATE ,
							SSN TEXT ,
							Allergies TEXT ,
							MedicalConditions TEXT
							)
							'''

		self.cursor.execute(query)
		self.conn.commit()

		# create Claims table
		query = '''create table 'Claims'(
									Id INTEGER PRIMARY KEY AUTOINCREMENT,
									AccountNumber INTEGER NOT NULL ,
									ClaimNumber TEXT ,
									LossDate DATE ,
									LossType TEXT ,
									BilledAmount REAL ,
									CoveredAmount REAL,
									FOREIGN KEY(AccountNumber)
										REFERENCES Accounts(AccountNumber)
									)
									'''
		self.cursor.execute(query)
		self.conn.commit()

	def insert_account(self, policyholder):

		inputs = policyholder.properties
		query = '''insert into Accounts Values (Null,?,?,?,?,?,?)'''

		self.cursor.execute(query, inputs)
		self.conn.commit()


	def insert_claim(self, policyholder):
		new_claim_inputs = (policyholder.account_number,) + policyholder.make_claim()
		query = '''insert into Claims Values (Null,?,?,?,?,?,?)'''

		self.cursor.execute(query, new_claim_inputs)
		self.conn.commit()


	def show_metrics(self):
		'''
		- Total covered amount for all claims
		- Claims per year
		- Average age of insured
		'''
		query1 = '''select sum(CoveredAmount) from Claims'''
		metric1 = list(self.cursor.execute(query1,()))[0]

		self.conn.commit()
		print(metric1)

		query2 = '''select strftime('%Y', LossDate) as LossYear , count(*) from Claims 
						group by LossYear order by year desc'''


		metric2 = self.cursor.execute(query2, ())

		self.conn.commit()
		print('the number of claims for each year:')
		for row in result_cn:
			print('Year %s: %s vehicle(s)'%row)

	def get_VINs(self,):
		query = '''select VIN from Motors'''

		result_cn = self.cursor.execute(query, ())

		self.conn.commit()

		print('VIN numbers:')
		for row in result_cn:
			print(row[0])

if __name__ == "__main__":

	# randomly create data entries
	acct1 = Policyholder()
	acct1.make_claim()
	print(acct1)


	#create database
	testdb = InsuranceDB(DB_NAME)
	testdb.make_tables()
	testdb.insert_account(acct1)
	testdb.insert_claim(acct1)
	testdb.insert_claim(acct1)
	testdb.insert_claim(acct1)
	testdb.insert_claim(acct1)





'''
	#standard output as requested.
	testdb.get_summary()
	#print out list of VIN numbers for the search in the interactive mode.
	testdb.get_VINs()
	#get requested VIN
	input_VIN = input('Please Type in VIN number to search a vehicle:')
	#output VIN related car information
	testcar.get_motors_data(input_VIN).
'''