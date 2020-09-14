import unittest
import os
from exam import *

class TestPolicyholder(unittest.TestCase):
	'''
	Unit Test cases for Policyholder object
	'''
	def setUp(self):
		self.test_account = Policyholder()
		

	def test_policyholder_properties(self):
		self.assertEqual(len(self.test_account.properties), 6)

	def test_account_number(self):
		acctnum = self.test_account.make_account_number()
		self.assertTrue(len(acctnum) == 10)

	def test_ssn(self):
		self.assertFalse(self.test_account.ssn == self.test_account.ssn_sensored)
		self.assertTrue(self.test_account.ssn_sensored[:6] == "xxx-xx")

	def test_make_claim(self):
		test_claim = self.test_account.make_claim()
		self.assertTrue(len(test_claim) == 5)



class TestDB(unittest.TestCase):
	'''
	Unit Test cases for TestDB object
	'''
	def setUp(self):
		self.test_db = InsuranceDB("TEST DB")
		self.test_db.make_tables()

	def test_db_make_tables(self):
		
		query = '''SELECT name FROM sqlite_master 
					WHERE type ='table' AND name NOT LIKE 'sqlite_%';'''
		results = [x[0] for x in self.test_db.return_query(query)]

		self.assertTrue("Accounts" in results)
		self.assertTrue("Claims" in results)
		self.assertTrue("SSN_KEY" in results)

	def test_db_insert_account(self):
		self.test_account = Policyholder()
		self.test_db.insert_account(self.test_account)
		query = '''SELECT count(*) from Accounts'''
		results = [x[0] for x in self.test_db.return_query(query)]
		self.assertTrue(results[0] == 1)


		query = '''SELECT count(*) from SSN_KEY'''
		results = [x[0] for x in self.test_db.return_query(query)]
		self.assertTrue(results[0] == 1)

	def test_db_insert_claim(self):
		self.test_account = Policyholder()
		self.test_db.insert_account(self.test_account)
		self.test_db.insert_claim(self.test_account)

		query = ''' SELECT count(*) from Claims'''
		results = [x[0] for x in self.test_db.return_query(query)]
		self.assertTrue(results[0] == 1)
		

	def test_db_metrics(self):
		random_pol_cnt = random.randint(1,5)
		random_clm_cnt = random.randint(1,5)

		for p in range(random_pol_cnt): 
			ph = Policyholder()
			self.test_db.insert_account(ph)
			for c in range(random_clm_cnt):
				self.test_db.insert_claim(ph)
		self.test_db.run_metrics()

		# test metrics property of sample DB
		self.assertTrue(type(self.test_db.metrics) == dict)
		self.assertTrue(len(self.test_db.metrics.keys()) == 3)

		# test if # of policies match up
		query = '''SELECT count(*) from Accounts'''
		results = [x[0] for x in self.test_db.return_query(query)]
		self.assertTrue(results[0] == random_pol_cnt)

		# test if # of claims match up
		query = ''' SELECT count(*) from Claims'''
		results = [x[0] for x in self.test_db.return_query(query)]
		self.assertTrue(results[0] == random_clm_cnt * random_pol_cnt)


if __name__ == '__main__':
	unittest.main()
