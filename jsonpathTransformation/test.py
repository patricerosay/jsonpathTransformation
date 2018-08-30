import jsonpathTransformation
import unittest
import pkg_resources


class TestCase(unittest.TestCase):

    def test_transfo(self):
        jsonpathTransformation.parseJsonPathTransformationFile(pkg_resources.resource_filename(__name__, '../sample/sample.json'), pkg_resources.resource_filename(
            __name__, '../sample/transformation.json'), pkg_resources.resource_filename(__name__, '../sample/out.json'), True)


    def test_transfo(self):
        jsonpathTransformation.extractFromFileJsonPathExpression(pkg_resources.resource_filename(__name__, '../sample/sample.json'), '$.smartData.itemId')


if __name__ == "__main__":
    unittest.main()
