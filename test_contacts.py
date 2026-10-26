import unittest
from contacts_manager import validate_phone, validate_email

class TestContactManager(unittest.TestCase):
    
    def test_validate_phone(self):
        # Test valid phone (strips symbols and spaces automatically)
        is_valid, digits = validate_phone("+1 (234) 567-8900")
        self.assertTrue(is_valid)
        self.assertEqual(digits, "12345678900")

        # Test invalid phone (too short)
        is_valid, digits = validate_phone("123")
        self.assertFalse(is_valid)

    def test_validate_email(self):
        # Test valid email
        self.assertTrue(validate_email("yahoorm@gmail.com"))
        
        # Test invalid email
        self.assertFalse(validate_email("invalid-email.com"))
        
        # Test empty email (which is allowed in our logic)
        self.assertTrue(validate_email(""))

if __name__ == '__main__':
    unittest.main()