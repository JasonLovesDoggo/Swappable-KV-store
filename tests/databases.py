import secrets
import unittest
from configparser import ConfigParser

from databases import grouper

config = ConfigParser()
config.read('./config.ini')
TESTKEY = secrets.token_urlsafe(16)
TESTVALUE = "test value"


class PostGreSQL(unittest.TestCase):
    def setUp(self):
        self.main()

    def main(self):
        self.TESTKEY = TESTKEY
        self.db_name = self.__class__.__name__
        if config[self.db_name.lower()]['Uri'] is None:  # the __class__.__name__ is the name of the class
            raise self.skipTest(f"{self.db_name} Uri not found in config.ini")
        self.db = grouper.Database('PostgreSQL', 'tests').db
        if self.db.get(self.TESTKEY) is None:  # if the key doesn't exit in the database
            self.test_a_insert()
            self.test_delete()
        else:  # if the key does exist in the database, pick a new key
            self.TESTKEY = secrets.token_urlsafe(16)

    def test_a_insert(self):
        """Tests if the database can insert a value"""
        self.db.insert((self.TESTKEY, TESTVALUE))
        self.assertEqual(self.db.get(self.TESTKEY),
                         TESTVALUE)  # get is a method of the Database class

    def test_delete(self):
        """tests if the database can delete a value"""
        if self.db.exists(self.TESTKEY):
            self.db.delete(self.TESTKEY)
            self.assertFalse(self.db.get(self.TESTKEY))
        else:
            self.db.insert((self.TESTKEY, TESTVALUE))
            self.test_delete()


class MongoDB(unittest.TestCase):
    def setUp(self):
        self.main()

    def main(self):
        self.TESTKEY = TESTKEY
        self.db_name = self.__class__.__name__
        if config[self.db_name.lower()]['Uri'] is None:  # the __class__.__name__ is the name of the class.
            raise self.skipTest(f"{self.db_name} Uri not found in config.ini")
        self.db = grouper.Database('MongoDB', 'tests').db
        if self.db.get(self.TESTKEY) is None:  # if the key doesn't exit in the database
            self.test_a_insert()
            self.test_delete()
        else:  # if the key does exist in the database, pick a new key
            self.TESTKEY = secrets.token_urlsafe(16)

    def tearDown(self):  # delete the test values
        self.db.delete(self.TESTKEY)

    def test_a_insert(self):
        """Tests if the database can insert a value"""
        self.db.insert((self.TESTKEY, TESTVALUE))
        self.assertEqual(self.db.get(self.TESTKEY), TESTVALUE)  # get is a method of the Database class

    def test_delete(self):
        """tests if the database can delete a value"""
        if self.db.exists(self.TESTKEY):
            self.db.delete(self.TESTKEY)
            self.assertFalse(self.db.get(self.TESTKEY))
        else:
            self.db.insert((self.TESTKEY, TESTVALUE))
            self.test_delete()


if __name__ == '__main__':
    unittest.main()
