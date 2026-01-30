import unittest
import sys

# Discover and run all tests
if __name__ == '__main__':
    # Create test loader
    loader = unittest.TestLoader()
    
    # Discover all tests in the tests directory
    suite = loader.discover('tests', pattern='test_*.py')
    
    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)