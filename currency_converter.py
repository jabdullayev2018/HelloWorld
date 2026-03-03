#!/usr/bin/env python3
"""Currency rates viewer for Azerbaijani Manat (AZN) conversion rates."""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

DEFAULT_RATES_URL = "https://www.cbar.az/currencies/03.03.2026.xml"


def fetch_xml(url: str) -> str:
    """Fetch XML data from the provided URL."""
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            return response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not fetch rates from {url}: {exc}") from exc


def parse_rates(xml_data: str) -> dict[str, str]:
    """Parse exchange rates and return a dictionary of currency code -> AZN value."""
    root = ET.fromstring(xml_data)
    rates: dict[str, str] = {}

    for valute in root.iter("Valute"):
        code = valute.attrib.get("Code", "").strip().upper()
        value_node = valute.find("Value")
        if not code or value_node is None or value_node.text is None:
            continue
        rates[code] = value_node.text.strip()

    if not rates:
        raise RuntimeError("No currency rates found in XML response.")

    return rates


def filter_rates(rates: dict[str, str], search: str | None) -> dict[str, str]:
    """Filter rates by valute code (case-insensitive, substring match)."""
    if not search:
        return rates

    term = search.strip().upper()
    return {code: value for code, value in rates.items() if term in code}


def print_rates(rates: dict[str, str]) -> None:
    """Print rates in a readable table format."""
    if not rates:
        print("No matching currency codes found.")
        return

    code_width = max(len("Code"), max(len(code) for code in rates))
    value_width = max(len("Value (AZN)"), max(len(value) for value in rates.values()))

    print(f"{'Code':<{code_width}}  {'Value (AZN)':>{value_width}}")
    print(f"{'-' * code_width}  {'-' * value_width}")

    for code in sorted(rates):
        print(f"{code:<{code_width}}  {rates[code]:>{value_width}}")


def run_interactive(rates: dict[str, str]) -> None:
    """Run an interactive search prompt for valute codes."""
    print("Interactive search is enabled. Enter a valute code (or part of it).")
    print("Press Enter on an empty line to exit.")

    while True:
        query = input("Search code: ").strip()
        if not query:
            print("Goodbye!")
            return

        print_rates(filter_rates(rates, query))
        print()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Display currency rates in AZN terms and search by valute code."
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_RATES_URL,
        help=f"XML source URL (default: {DEFAULT_RATES_URL})",
    )
    parser.add_argument(
        "--search",
        help="Valute code search term (e.g., USD, EUR). Case-insensitive substring match.",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Start interactive search mode after fetching rates.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    try:
        xml_data = fetch_xml(args.url)
        rates = parse_rates(xml_data)
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        return 1
    except ET.ParseError as exc:
        print(f"Failed to parse XML response: {exc}", file=sys.stderr)
        return 1

    filtered = filter_rates(rates, args.search)
    print_rates(filtered)

    if args.interactive:
        print()
        run_interactive(rates)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
