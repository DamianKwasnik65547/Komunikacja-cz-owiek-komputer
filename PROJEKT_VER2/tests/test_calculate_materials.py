# tests/test_calculate_materials.py
import unittest
from models import calculate_materials

class TestCalculateMaterials(unittest.TestCase):

    def test_calculate_materials_valid(self):
        result = calculate_materials(
            100, 30, 30, 10, 15, 5, 20, 2, 2, 50, 5, 5
        )
        expected = (1111.111111111111, 0.4, 1.0, 1.5, 0.5, 2.0)  # Ustaw oczekiwane wartości zgodnie z funkcją
        self.assertEqual(result, expected)

    def test_calculate_materials_invalid(self):
        with self.assertRaises(ValueError):
            calculate_materials(
                -100, 30, 30, 10, 15, 5, 20, 2, 2, 50, 5, 5
            )

if __name__ == "__main__":
    unittest.main()
