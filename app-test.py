from app import app

import unittest


class BasicTestCase(unittest.TestCase):

    """The Basic test case."""

    def test_index(self):
        """Test the index route. """
        tester = app.test_client(self)
        response = tester.get("/", content_type="html/text")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Hello, World!")


if __name__ == "__main__":
    unittest.main()
