import unittest
from app.models import User

class UserModelTest(unittest.TestCase):
  def test_password_setter(self):
    u = User(password = 'test')
    self.assertTrue(u.password_hash is not None)

  def test_password_encrypt(self):
    u = User(password = 'test')
    with self.assertRaises(AttributeError):
      u.password

  def test_password_verify(self):
    u = User(password = 'test')
    self.assertTrue(u.verify_password('test'))
    self.assertFalse(u.verify_password('dog'))

  def test_hash_generation(self):
    u = User(password = 'test')
    next_u = User(password = 'test')
    self.assertTrue(u.password_hash != next_u.password_hash)
