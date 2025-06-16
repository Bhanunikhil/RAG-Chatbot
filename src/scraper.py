# src/scraper.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

BASE_URL = "https://www.angelone.in"
START_PATH = "/support"

# Compute the project root and data directory
ROOT = Path(__file__).parent.parent  # rag-chatbot/
SUPPORT_DIR = ROOT / "data" / "support"
SUPPORT_DIR.mkdir(parents=True, exist_ok=True)


def get_support_links():
    resp = requests.get(urljoin(BASE_URL, START_PATH))
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    links = {
        urljoin(BASE_URL, a["href"].split("#")[0])
        for a in soup.find_all("a", href=True)
        if a["href"].startswith("/knowledge-center/")
    }
    return sorted(links)


def fetch_page_text(url):
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())


def main():
    links = get_support_links()
    print(f"Found {len(links)} pages:")
    for link in links:
        slug = link.rstrip("/").split("/")[-1]
        text = fetch_page_text(link)
        out_path = SUPPORT_DIR / f"{slug}.txt"
        out_path.write_text(text, encoding="utf-8")
        print("  →", out_path.name)
    print("Done.")


if __name__ == "__main__":
    main()
