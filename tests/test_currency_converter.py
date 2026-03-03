import unittest

from currency_converter import filter_rates, parse_rates


SAMPLE_XML = """<?xml version='1.0' encoding='UTF-8'?>
<ValCurs Date='03.03.2026' Name='Foreign Exchange Rates'>
  <ValType Type='Xarici valyutalar'>
    <Valute Code='USD'><Value>1.7000</Value></Valute>
    <Valute Code='EUR'><Value>1.8500</Value></Valute>
    <Valute Code='GBP'><Value>2.1500</Value></Valute>
  </ValType>
</ValCurs>
"""


class CurrencyConverterTests(unittest.TestCase):
    def test_parse_rates(self):
        rates = parse_rates(SAMPLE_XML)
        self.assertEqual(rates["USD"], "1.7000")
        self.assertEqual(rates["EUR"], "1.8500")
        self.assertEqual(rates["GBP"], "2.1500")

    def test_filter_rates_case_insensitive(self):
        rates = {"USD": "1.7000", "EUR": "1.8500", "AUD": "1.1000"}
        filtered = filter_rates(rates, "u")
        self.assertEqual(filtered, {"USD": "1.7000", "EUR": "1.8500", "AUD": "1.1000"})


if __name__ == "__main__":
    unittest.main()
