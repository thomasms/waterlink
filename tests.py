import unittest
from datetime import date

from compute import compute_total_cost


class ComputeUnitTest(unittest.TestCase):

    # Real case: 2019-2020 bill (exc VAT)
    def test_case1(self):
        result = compute_total_cost(
            reading=449,
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
        expected = 2689.10
        self.assertAlmostEqual(result, expected, places=2)

    # Real case: 2019-2020 bill (inc VAT)
    def test_case1_vat(self):
        result = compute_total_cost(
            reading=449,
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
        expected = 2850.44
        self.assertAlmostEqual(result, expected, places=2)

    def test_case2(self):
        result = compute_total_cost(
            reading=449,
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
        expected = 2454.50
        self.assertAlmostEqual(result, expected, places=2)

    def test_case2_vat(self):
        result = compute_total_cost(
            reading=449,
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
            vat=0.06,
        )
        expected = 2601.77
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

    # Real case: 2020-2021 bill (exc VAT)
    def test_case5(self):
        result = compute_total_cost(
            reading=292,
            data=[
                {
                    "start": date(2020, 2, 19),
                    "end": date(2020, 12, 31),
                    "we": 3,
                    "dom": 5,
                },
                {"start": date(2021, 1, 1), "end": date(2021, 2, 4), "we": 3, "dom": 6},
            ],
            vat=0.0,
        )
        expected = 1409.30
        self.assertAlmostEqual(result, expected, places=2)

    # Real case: 2020-2021 bill (inc VAT)
    def test_case5_vat(self):
        result = compute_total_cost(
            reading=292,
            data=[
                {
                    "start": date(2020, 2, 19),
                    "end": date(2020, 12, 31),
                    "we": 3,
                    "dom": 5,
                },
                {"start": date(2021, 1, 1), "end": date(2021, 2, 4), "we": 3, "dom": 6},
            ],
            vat=0.06,
        )
        expected = 1493.86
        self.assertAlmostEqual(result, expected, places=2)

    def test_case6(self):
        result = compute_total_cost(
            reading=365,
            data=[
                {
                    "start": date(2020, 2, 19),
                    "end": date(2020, 12, 31),
                    "we": 3,
                    "dom": 6,
                },
                {
                    "start": date(2021, 1, 1),
                    "end": date(2021, 2, 18),
                    "we": 3,
                    "dom": 6,
                },
            ],
            vat=0.0,
        )
        expected = 1780.87
        self.assertAlmostEqual(result, expected, places=2)

    def test_case6_vat(self):
        result = compute_total_cost(
            reading=365,
            data=[
                {
                    "start": date(2020, 2, 19),
                    "end": date(2020, 12, 31),
                    "we": 3,
                    "dom": 6,
                },
                {
                    "start": date(2021, 1, 1),
                    "end": date(2021, 2, 18),
                    "we": 3,
                    "dom": 6,
                },
            ],
            vat=0.06,
        )
        expected = 1887.73
        self.assertAlmostEqual(result, expected, places=2)
