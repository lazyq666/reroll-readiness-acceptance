import sys,unittest
class SyntheticPlatform(unittest.TestCase):
 def test_linux_gate(self): self.assertNotEqual(sys.platform, 'linux', 'synthetic Linux-only failure')
