"""
api_server.py — a small local web API that serves the Northbridge Bank data.

It uses only Python's standard library, so there is nothing to install.
Start it in its own terminal window and leave that window open:

    python code/00_setup/api_server.py

It listens on http://127.0.0.1:8000 and answers these requests:

    GET /health                          -> {"status": "ok"}
    GET /fx-rates?currency=EUR           -> daily EUR rates for 2025
    GET /fx-rates?currency=USD&month=2025-03
    GET /loans?product=Mortgage&page=1   -> 100 loans per page, with paging info
    GET /customers/C0001                 -> one customer and their accounts

Requests to /loans and /customers need the header  X-API-Key: northbridge-demo
so that you practise sending an API key, as you will with real bank APIs.
Press Ctrl+C in the terminal window to stop the server.
"""

import csv
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

DATA = Path(__file__).resolve().parents[2] / "data"
API_KEY = "northbridge-demo"
PAGE_SIZE = 100


def load(name):
    with open(DATA / "csv" / f"{name}.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


FX = load("fx_rates")
LOANS = load("loans")
CUSTOMERS = json.loads((DATA / "json" / "customers.json").read_text())


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(url.query).items()}

        if url.path == "/health":
            return self.send_json(200, {"status": "ok"})

        if url.path == "/fx-rates":
            ccy = q.get("currency", "EUR").upper()
            rows = [r for r in FX if r["currency"] == ccy]
            if "month" in q:
                rows = [r for r in rows if r["rate_date"].startswith(q["month"])]
            rows = [{"date": r["rate_date"], "currency": ccy,
                     "rate_per_gbp": float(r["rate_per_gbp"])} for r in rows]
            return self.send_json(200, {"base": "GBP", "count": len(rows), "rates": rows})

        if self.headers.get("X-API-Key") != API_KEY:
            return self.send_json(401, {"error": "missing or invalid X-API-Key header"})

        if url.path == "/loans":
            rows = LOANS
            if "product" in q:
                rows = [r for r in rows if r["product"] == q["product"]]
            page = int(q.get("page", 1))
            pages = max(1, -(-len(rows) // PAGE_SIZE))
            chunk = rows[(page - 1) * PAGE_SIZE: page * PAGE_SIZE]
            return self.send_json(200, {"page": page, "pages": pages,
                                        "total": len(rows), "loans": chunk})

        if url.path.startswith("/customers/"):
            cid = url.path.rsplit("/", 1)[-1]
            for c in CUSTOMERS:
                if c["customer_id"] == cid:
                    return self.send_json(200, c)
            return self.send_json(404, {"error": f"customer {cid} not found"})

        return self.send_json(404, {"error": "unknown endpoint"})

    def log_message(self, fmt, *args):
        print("request:", getattr(self, "path", "(malformed request)"))


if __name__ == "__main__":
    print("Northbridge API running on http://127.0.0.1:8000  (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
