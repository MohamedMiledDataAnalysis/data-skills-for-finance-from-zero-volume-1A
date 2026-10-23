# Volume 1A — companion code for *Data Skills for Finance from Zero, Volume 1A: SQL, Python and PySpark*

Every query and script from the book, organised by chapter, the Northbridge Bank data, and the generator of those data.

## Getting the files onto your computer

- **Without Git:** click **Code** › **Download ZIP** on this page, extract `data-skills-for-finance-from-zero-volume-1A-main.zip`,
  move the folder `data-skills-for-finance-from-zero-volume-1A-main` into your `Documents` folder and rename it `northbridge`.
  Chapter 1 of the book shows every click for Windows, macOS and Ubuntu.
- **With Git** (Volume 2, Chapter 4), clone it into a folder named `northbridge`:

  ```
  git clone https://github.com/mohamedmileddataanalysis/data-skills-for-finance-from-zero-volume-1A.git northbridge
  ```

Northbridge Bank is fictional; all data are synthetic and generated with a fixed random seed.

## Order of the book

1. Chapter 1 — Welcome to Northbridge Bank.
2. Part I, SQL (Chapters 2–7) — install SQL Server, load `data/sql/northbridge_sqlserver.sql`, and query it in T-SQL.
3. Part II, Python (Chapters 8–21) — install Python and VS Code, then pandas, files, SQL Server from Python, the API, charts, the portfolio project, the loan tape, statistics and regression.
4. Part III, PySpark (Chapters 22–24) — install Java and PySpark, then Spark DataFrames, aggregations and Spark SQL.

Appendix A covers installation errors; Appendix B is the glossary.

## Start here

1. The data are already in `data/` when you unzip the download. Part I needs only SQL Server
   and `data/sql/northbridge_sqlserver.sql` (Chapter 2).

2. From Chapter 8 on, run every script from this `northbridge` folder, for example
   `python code/13_files/check_loans.py`. Scripts save their results in `output/`, which is
   not in the download: the scripts create it.

3. `code/00_setup/generate_data.py` (Chapter 8) rebuilds every file in `data/` from a fixed
   random seed (2026), identical to the files of the download; only the creation date stored
   inside `northbridge.xlsx` changes. Run it whenever you need to restore the data:

   ```
   python code/00_setup/generate_data.py
   ```

4. Start the local practice API in Chapter 8; Chapters 16 and 18 use it again:

   ```
   python code/00_setup/api_server.py
   ```

5. Type each query and script yourself into a new file whose name starts with `my_`, in the
   same chapter folder (for example `code/03_first_select/my_01_select_star.sql` or
   `code/08_python/my_hello.py`), and run it under that name. The book's file stays next to
   it as the answer key.

## Layout

| Folder | Contents |
|---|---|
| `data/csv/` | customers, accounts, transactions, loans, fx_rates, market_prices |
| `data/excel/` | `northbridge.xlsx`, one sheet per table |
| `data/json/` | `loans.json` (flat), `customers.json` (nested) |
| `data/sql/` | `northbridge_sqlserver.sql` — creates the Northbridge database in SQL Server (Chapter 2) |
| `data/loan_tape/` | `loan_tape.csv` (2,005 rows: 2,000 mortgages plus planted duplicates and other defects) and `loan_tape_control.csv` — Chapter 19 |
| `code/00_setup/` | data generator and local API |
| `code/NN_name/` | the queries and scripts of chapter NN (`.sql` and `.py`) |
| `output/` | created by the scripts; where they save their results and charts |

Northbridge Bank is fictional; all data are synthetic.

## Install the Python packages in one step

Inside the activated `.venv` (Chapter 8):

```
pip install -r requirements.txt
```

`requirements.txt` pins the exact versions the book was tested with, so your results match
the book's to the penny.

## Check that every example runs

```
python run_all.py          # all chapters
python run_all.py 12 13    # only Chapters 12 and 13
```

The script runs the book's Python files (never your `my_` files) and prints one line per
failure, then a total. Scripts that need SQL Server, the local API, internet access or Java
are skipped, with the reason, when that service is not available. The SQL queries of
Chapters 2 to 7 run in SSMS or VS Code against your SQL Server, as the book shows.

## Git

`.gitignore` keeps `output/`, `.venv/`, Python caches and your own `my_` practice files out
of the repository. Remove the `my_*` line if you want to keep your practice files in your
own copy on GitHub.

## The series

Each book has its own companion repository; each one is self-contained, with its own `data/` folder.

| Book | Repository |
|---|---|
| Volume 1A — SQL, Python and PySpark | [`data-skills-for-finance-from-zero-volume-1A`](https://github.com/mohamedmileddataanalysis/data-skills-for-finance-from-zero-volume-1A) |
| Volume 1B — R and R Shiny | [`data-skills-for-finance-from-zero-volume-1B`](https://github.com/mohamedmileddataanalysis/data-skills-for-finance-from-zero-volume-1B) |
| Volume 2 — Git, GitHub, AWS, Azure and Google Cloud | [`data-skills-for-finance-from-zero-volume-2`](https://github.com/mohamedmileddataanalysis/data-skills-for-finance-from-zero-volume-2) |
| Volume 3 — AI for Structured Finance (Ollama, Python and R) | [`data-skills-for-finance-from-zero-volume-3`](https://github.com/mohamedmileddataanalysis/data-skills-for-finance-from-zero-volume-3) |

## Licence

The code and data in this repository are released under the [MIT licence](LICENSE):
you may use, copy, adapt and share them, including at work, provided you keep the
copyright notice. The books' text and figures remain © Mohamed Miled, all rights reserved.
