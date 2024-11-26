import unittest
import sys
sys.path.append('d:/code/twitterAuto')
from core.Timer import Timer

class TestTimer(unittest.TestCase):
    def test_get_current_task(self):
        self.assertEqual(Timer().get_current_task(),0)
    
    def test_run_timer(self):
        pass

unittest.main()