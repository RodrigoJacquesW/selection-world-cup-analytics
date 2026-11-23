"""Beyond FIFA Rankings: snapshot (SofaScore + Elo) -> BigQuery -> Dataform -> team scores.

Usage (from anywhere):
    python main.py            # load the committed snapshot + run Dataform models and tests
    python main.py --scrape   # re-collect data/raw from SofaScore and eloratings.net first
    python main.py --flags    # download missing flags for the Power BI report
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from beyond_fifa.config import get_settings  # noqa: E402
from beyond_fifa.load import load_all  # noqa: E402
from beyond_fifa.transform import run_dataform  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scrape", action="store_true", help="refresh data/raw (overwrites the snapshot)")
    parser.add_argument("--flags", action="store_true", help="download flags for the report")
    parser.add_argument("--skip-dataform", action="store_true", help="only load the raw tables")
    args = parser.parse_args()

    settings = get_settings()
    print(f"Project {settings.gcp_project_id} ({settings.bq_location})")

    if args.scrape:
        from beyond_fifa import scrape

        print("[0] Scraping SofaScore and Elo ratings")
        scrape.scrape_sofascore()
        scrape.download_elo()

    if args.flags:
        from beyond_fifa.flags import download_flags

        download_flags()

    print("[1/2] Load raw tables")
    load_all(settings)

    if args.skip_dataform:
        print("[2/2] Dataform skipped")
    else:
        print("[2/2] Dataform run")
        run_dataform(settings)
    print("Done.")


if __name__ == "__main__":
    main()
