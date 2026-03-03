# AZN Currency Rates App

Simple Python app that fetches currency rates from the Central Bank of Azerbaijan XML feed and shows each **valute code** with its **value in AZN terms**.

Source XML used by default:
- https://www.cbar.az/currencies/03.03.2026.xml

## Requirements

- Python 3.10+

## Usage

Show all rates:

```bash
python3 currency_converter.py
```

Search by valute code:

```bash
python3 currency_converter.py --search USD
```

You can also search by partial code:

```bash
python3 currency_converter.py --search U
```

Interactive search mode:

```bash
python3 currency_converter.py --interactive
```

Use another XML source URL (optional):

```bash
python3 currency_converter.py --url "https://www.cbar.az/currencies/03.03.2026.xml"
```
