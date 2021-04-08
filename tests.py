import unittest
from datetime import date

from compute import compute_total_cost


class ComputeUnitTest(unittest.TestCase):
    def test_case1(self):
        result = compute_total_cost(
            reading=442.936,
            data=[
                {
                    "start": date(2019, 2, 14),
                    "end": date(2019, 12, 31),
                    "we": 3,
                    "dom": 3,
                },
                {
                    "start": date(2020, 1, 1),
                    "end": date(2020, 2, 18),
                    "we": 3,
                    "dom": 5,
                },
            ],
            vat=0.0,
        )
        expected = 2689.12
        self.assertAlmostEqual(result, expected, places=2)

    def test_case1_vat(self):
        result = compute_total_cost(
            reading=442.936,
            data=[
                {
                    "start": date(2019, 2, 14),
                    "end": date(2019, 12, 31),
                    "we": 3,
                    "dom": 3,
                },
                {
                    "start": date(2020, 1, 1),
                    "end": date(2020, 2, 18),
                    "we": 3,
                    "dom": 5,
                },
            ],
            vat=0.06,
        )
        expected = 2850.47
        self.assertAlmostEqual(result, expected, places=2)

    def test_case2(self):
        result = compute_total_cost(
            reading=443,
            data=[
                {
                    "start": date(2019, 2, 14),
                    "end": date(2019, 12, 31),
                    "we": 3,
                    "dom": 5,
                },
                {
                    "start": date(2020, 1, 1),
                    "end": date(2020, 2, 18),
                    "we": 3,
                    "dom": 6,
                },
            ],
            vat=0.0,
        )
        expected = 2454.98
        self.assertAlmostEqual(result, expected, places=2)

    def test_case3(self):
        result = compute_total_cost(
            reading=160,
            data=[
                {
                    "start": date(2019, 2, 14),
                    "end": date(2019, 12, 31),
                    "we": 3,
                    "dom": 3,
                },
                {
                    "start": date(2020, 1, 1),
                    "end": date(2020, 2, 18),
                    "we": 3,
                    "dom": 3,
                },
            ],
            vat=0.0,
        )
        expected = 805.25
        self.assertAlmostEqual(result, expected, places=2)

    def test_case4(self):
        result = compute_total_cost(
            reading=180,
            data=[
                {
                    "start": date(2019, 2, 14),
                    "end": date(2019, 12, 31),
                    "we": 3,
                    "dom": 3,
                },
                {
                    "start": date(2020, 1, 1),
                    "end": date(2020, 2, 18),
                    "we": 3,
                    "dom": 3,
                },
            ],
            vat=0.0,
        )
        expected = 875.50
        self.assertAlmostEqual(result, expected, places=2)
