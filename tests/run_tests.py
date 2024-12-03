import unittest
from flask_jwt_extended import get_jwt_identity


if __name__ == '__main__':
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
