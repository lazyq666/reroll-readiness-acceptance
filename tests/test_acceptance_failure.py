import unittest
class SyntheticFailure(unittest.TestCase):
 def test_rejected_candidate(self): self.fail('synthetic acceptance failure')
