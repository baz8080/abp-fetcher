import time
from pathlib import Path

import requests

OUTPUT_DIR = Path("logs")
PROCESSED_LOG = OUTPUT_DIR / "processed.log"

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    processed = set(
        line.split(",")[0] for line in PROCESSED_LOG.read_text().splitlines()) if PROCESSED_LOG.exists() else set()

    session = requests.Session()
    session.headers.update({"User-Agent": "abp-fetcher/1.0 https://github.com/baz8080/abp-fetcher",
                            "Accept": "application/json",
                            "Accept-Encoding": "gzip",
                            "Connection": "keep-alive"})

    case_ids = range(101348, 101448)

    for case_id in case_ids:
        if str(case_id) in processed:
            print(f"Skipping {case_id}")
            continue

        print(f"Processing {case_id}")
        case_response = session.get(f"https://archive.pleanala.ie/api/cases('{case_id}')?$expand=History($orderBy=date%20desc),Participants")

        if case_response.status_code == 200:
            (OUTPUT_DIR / f"{case_id}-case.json").write_text(case_response.text)

            time.sleep(3)

            document_response = session.get(f"https://archive.pleanala.ie/api/cases('{case_id}')/Documents")
            (OUTPUT_DIR / f"{case_id}-documents.json").write_text(document_response.text)

        with PROCESSED_LOG.open("a") as f:
            f.write(f"{case_id},{case_response.status_code}\n")

        time.sleep(3)

if __name__ == "__main__":
    main()