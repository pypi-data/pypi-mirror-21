import unittest
import numpy as np
from yhat import json_dumps
import json

class TestYhatJson(unittest.TestCase):

    def test_dumps_dict(self):
        x = { "x": 1 }
        self.assertEqual(json.dumps(x), json_dumps(x))

    def test_dumps_list(self):
        x = [ "a", "b", "c" ]
        self.assertEqual(json.dumps(x), json_dumps(x))

    def test_dumps_string(self):
        x = [ "a", "b", "c" ]
        self.assertEqual(json.dumps(x), json_dumps(x))

    def test_dumps_int(self):
        x = 10
        self.assertEqual(json.dumps(x), json_dumps(x))

    def test_dumps_float(self):
        x = 10.1
        self.assertEqual(json.dumps(x), json_dumps(x))

    def test_dumps_nan(self):
        x = np.nan
        self.assertEqual(json_dumps(x), 'null')

    def test_dumps_nan_list(self):
        x = [np.nan, np.nan, np.nan]
        self.assertEqual(json_dumps(x), '[null, null, null]')

    def test_dumps_numpy_array(self):
        x = np.arange(100)
        self.assertEqual(json_dumps(x), json.dumps(list(range(100))))

if __name__=="__main__":
    unittest.main()
