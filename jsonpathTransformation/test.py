import jsonpathTransformation
import unittest


class TestCase(unittest.TestCase):

    def test_transfo(self):
        jsonpathTransformation.main('../sample/sample.json','../sample/transformation.json','../sample/out.json')

if __name__ == "__main__":
    unittest.main()