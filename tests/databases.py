import secrets
import unittest
from configparser import ConfigParser

unittest.TestLoader.sortTestMethodsUsing = None

from databases import grouper

config = ConfigParser()
config.read('../config.ini')
TESTKEY = 'MmEKhQlTGCQSEDzBJQRqNg' #secrets.token_urlsafe(16)
TESTVALUE = "test value"


class PostGreSQL(unittest.TestCase):
    def setUp(self):
        self.main()

    def main(self):
        self.TESTKEY = TESTKEY
        if config[self.__class__.__name__.lower()]['Uri'] is None:  # the __class__.__name__ is the name of the class
            raise self.skipTest("PostgreSQL Uri not found in config.ini")
        self.PostGreDB = grouper.Database((config['setup']['DatabaseChoice']), 'tests').db
        if self.PostGreDB.get_value(self.TESTKEY) is None:  # if the key doesn't exit in the database
            self.test_a_insert()
            self.test_delete()
        else:  # if the key does exist in the database, pick a new key
            self.TESTKEY = secrets.token_urlsafe(16)

    def tearDown(self):  # delete the test values
        self.PostGreDB.delete(self.TESTKEY)

    def test_a_insert(self):
        """Tests if the database can insert a value"""
        self.PostGreDB.insert((self.TESTKEY, TESTVALUE))
        self.assertEqual(self.PostGreDB.get_value(self.TESTKEY),
                         TESTVALUE)  # get_value is a method of the Database class

    def test_delete(self):
        """tests if the database can delete a value"""
        print(self.PostGreDB.exists(self.TESTKEY))
        if self.PostGreDB.exists(self.TESTKEY):
            self.PostGreDB.delete(self.TESTKEY)
            self.assertFalse(self.PostGreDB.get_value(self.TESTKEY))
        else:
            return self.skipTest("The key doesn't exist in the database")


class MongoDB(unittest.TestCase):
    def setUp(self):
        self.main()

    def main(self):
        self.TESTKEY = TESTKEY
        if config[self.__class__.__name__.lower()]['Uri'] is None:  # the __class__.__name__ is the name of the class
            raise self.skipTest("MongoDB Uri not found in config.ini")
        self.MongoDB = grouper.Database((config['setup']['DatabaseChoice']), 'tests').db
        if self.MongoDB.get_value(self.TESTKEY) is None:  # if the key doesn't exit in the database
            self.test_a_insert()
            self.test_delete()
        else:  # if the key does exist in the database, pick a new key
            self.TESTKEY = secrets.token_urlsafe(16)

    def tearDown(self):  # delete the test values
        self.MongoDB.delete(self.TESTKEY)

    def test_a_insert(self):
        """Tests if the database can insert a value"""
        self.MongoDB.insert((self.TESTKEY, TESTVALUE))
        self.assertEqual(self.MongoDB.get_value(self.TESTKEY), TESTVALUE)  # get_value is a method of the Database class

    def test_delete(self):
        """tests if the database can delete a value"""
        if self.MongoDB.exists(self.TESTKEY):
            self.MongoDB.delete(self.TESTKEY)
            self.assertFalse(self.MongoDB.get_value(self.TESTKEY))
        else:
            pass  # TODO add a exists method to the database class


if __name__ == '__main__':
    unittest.main()
