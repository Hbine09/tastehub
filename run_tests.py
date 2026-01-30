import unittest
import sys
import os

# Discover and run all tests
if __name__ == '__main__':
    # 1. Get the absolute path to the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Define the absolute path to the 'tests' folder
    tests_dir = os.path.join(current_dir, 'app', 'tests')    
    # 3. Force current_dir into sys.path so the tests can find your 'app' folder
    sys.path.insert(0, current_dir)

    # Create test loader
    loader = unittest.TestLoader()
    
    try:
        # 4. Use the absolute path for discovery
        suite = loader.discover(start_dir=tests_dir, pattern='test_*.py')
        
        # Run tests with verbosity
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Exit with appropriate code
        sys.exit(0 if result.wasSuccessful() else 1)
        
    except Exception as e:
        print(f"❌ Error during test discovery: {e}")
        sys.exit(1)