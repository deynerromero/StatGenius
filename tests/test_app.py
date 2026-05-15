import unittest

from app import create_app


class CreateAppTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app()
        self.client = self.app.test_client()

    def test_home_route_returns_expected_content(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Inicio | StatGenius", response.data)
        self.assertIn(b"Convierte datos en decisiones inteligentes", response.data)


if __name__ == "__main__":
    unittest.main()
