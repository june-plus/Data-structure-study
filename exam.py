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
		self.ssn, self.ssn_sensored = self.make_ssn()
		self.allergies = random.choice(["none", "single", "multiple"])
		self.medical_conditions = random.choice(["none", "single", "multiple"])
		self.claim_count = 0
		self.claim_list = []

		self.properties = (self.account_number, self.sex, self.dob, self.ssn_sensored, self.allergies, self.medical_conditions)
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
		@return: tuple of (social security number in format ###-##-####, randomized ssn)
		'''
		first = random.randint(100,999)
		second = random.randint(10,99)
		third = random.randint(1000,9999)
		ssn = "{}-{}-{}".format(first, second, third)
		ssn_sensored = "xxx-xx-{}".format(third)
		if ssn in SSN_LIST:
			self.make_ssn()
		else:
			return (ssn, ssn_sensored)

	def make_claim(self):
		'''
		make a claim and link to policyholder.
		@return: tuple of (claim number, loss date, loss type, billed amount, covered amount)
		'''
		claim_number = str(self.claim_count + 1 ).zfill(6)
		# print(self.claim_list)
		if claim_number in self.claim_list:
			self.make_claim()
		else:
			lossdate = make_date((self.dob.year + 24, self.dob.month, self.dob.day), VALUATION_DATE.split("-")) #claims made after turning 24 .. for reality aspect
			losstype = random.choice(["surgery", "medication", "emergency", "hospital"])
			billed_amt = round(random.uniform(0, 30000),2)
			covered_amt = round(random.uniform(0, billed_amt),2)
			clm = Claim(lossdate, losstype, billed_amt, covered_amt)
			self.claim_count += 1
			self.claim_list.append(claim_number)

			return (claim_number, lossdate, losstype, billed_amt, covered_amt)

	def __str__(self):
		return '\nAcct No.: {} \nSex: {} \nDate of Birth: {} \nSSN: {} \nAllergies: {} \
		\nMedical Conditions: {}\n'.format(self.account_number,self.sex,self.dob,self.ssn_sensored,self.allergies,self.medical_conditions)
	

class Claim():
	'''
	Claim Object containing claim information
	'''
	def __init__(self, lossdate = None , losstype = None, billed_amt=0, covered_amt=0):
		self.lossdate = lossdate
		self.losstype = losstype
		self.billed_amt = billed_amt
		self.covered_amt = covered_amt


class InsuranceDB():
	def __init__(self, db_name):
		self.db_name = '{}.db'.format(db_name)
		self.metrics = {}

		try:
			self.conn = sqlite3.connect(self.db_name)
			self.cursor = self.conn.cursor()
			print('connnected to database {}'.format(db_name))
		except:
			print('database connection error; try again.')

	def return_query(self, query):
		self.cursor.execute(query)
		rows = self.cursor.fetchall()
		return rows


	def make_tables(self):
		'''
		Drops three tables if already exists, then creates Accounts, Claims, and SSN_LIST tables in DB
		'''
		query = '''
		DROP TABLE IF EXISTS 'Accounts';
		'''
		self.cursor.execute(query)

		query = '''
		DROP TABLE IF EXISTS 'Claims';
		'''
		self.cursor.execute(query)

		query = '''
		DROP TABLE IF EXISTS 'SSN_KEY';
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

		query = '''create table 'SSN_KEY'(
									Id INTEGER PRIMARY KEY AUTOINCREMENT,
									AccountNumber INTEGER NOT NULL ,
									SSN TEXT ,
									FOREIGN KEY(AccountNumber)
										REFERENCES Accounts(AccountNumber)
									)
									'''
		self.cursor.execute(query)
		self.conn.commit()


	def insert_account(self, policyholder):
		'''
		Inserts into DB account information and SSN information
		'''
		inputs = policyholder.properties
		query = '''insert into Accounts Values (Null,?,?,?,?,?,?)'''

		self.cursor.execute(query, inputs)
		self.conn.commit()

		inputs = (policyholder.account_number, policyholder.ssn,)
		query = '''insert into SSN_KEY Values (Null,?,?)'''

		self.cursor.execute(query, inputs)
		self.conn.commit()




	def insert_claim(self, policyholder):
		'''
		Inserts into DB claim
		'''
		new_claim_inputs = (policyholder.account_number,) + policyholder.make_claim()
		query = '''insert into Claims Values (Null,?,?,?,?,?,?)'''

		self.cursor.execute(query, new_claim_inputs)
		self.conn.commit()


	def run_metrics(self):
		'''
		Runs queries for the below three metrics and saves to the dictionary class variable 'metrics'
		- Total covered amount for all claims
		- Claims per year
		- Average age of insured
		'''

		# Total covered $ for all claims
		query1 = '''select sum(CoveredAmount) from Claims'''
		self.cursor.execute(query1)
		row = self.cursor.fetchone()
		self.metrics["covered_amt"] = round(row[0],2)
		#print(" total covered amount in dollars: $", self.metrics["covered_amt"])


		# Claims per year
		query2 = '''select strftime('%Y', LossDate) as LossYear , count(*) from Claims 
						group by LossYear order by LossYear desc'''


		self.cursor.execute(query2)
		rows = self.cursor.fetchall()
		self.metrics["year_summary"]=[]
		# print('yearly claim count:')
		for row in rows:
			# print('{}: {} claims'.format(row[0], row[1]))
			self.metrics["year_summary"].append(row)


		# Average age of insured
		query3 = '''select cast(strftime('%Y.%m%d', '{}') - strftime('%Y.%m%d', DOB) as int) from Accounts'''.format(VALUATION_DATE)
		self.cursor.execute(query3)
		row = self.cursor.fetchone()
		self.metrics["average_age"] = row[0]

		# print("Average age of policyholders:", row[0])

if __name__ == "__main__":

	testdb = InsuranceDB(DB_NAME)
	testdb.make_tables()
	'''
	# randomly create data entries
	for x in range(random.randint(1,10)):
		acct1 = Policyholder()
		# acct1.make_claim()
		print(acct1)


		testdb.insert_account(acct1)

		for y in range(random.randint(1,10)):
			testdb.insert_claim(acct1)

	testdb.run_metrics()
	'''
	query = '''SELECT name FROM sqlite_master 
	WHERE type ='table' AND name NOT LIKE 'sqlite_%';'''

	for x in testdb.return_query(query):
		print(x, "\n")