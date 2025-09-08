from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def fetch_latest_match_news():
    news_links = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # headless for server
        page = browser.new_page()

        # Google News search
        query = "India latest match"
        page.goto(f"https://news.google.com/search?q={query}")

        # Wait for news links to load
        page.wait_for_selector("a.WwrzSb")

        # Grab first 5 news links
        articles = page.locator("a.WwrzSb").all()[:5]

        for article in articles:
            link = article.get_attribute("href")
            if link and link.startswith("./"):  # convert relative to absolute
                link = "https://news.google.com" + link[1:]
            if link:
                news_links.append(link)

        browser.close()
    return news_links

@app.route("/latest-news", methods=["GET"])
def latest_news():
    try:
        news = fetch_latest_match_news()
        if not news:
            return jsonify({"message": "No news found"}), 404
        return jsonify({"latest_news": news})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
