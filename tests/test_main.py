
import unittest
import os
import random

from setenvironment import set_env_var

class MainTester(unittest.TestCase):
    def test_main(self) -> None:
        # generate a random value
        value = random.randint(0, 100)
        set_env_var("SETENVIRONMENT_TEST", value)
        self.assertEqual(value, int(os.environ["SETENVIRONMENT_TEST"]))
        # TODO add tests for getting the system path





if __name__ == "__main__":
    unittest.main()
