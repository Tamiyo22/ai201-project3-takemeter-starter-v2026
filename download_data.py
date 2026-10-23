import json
import csv
import urllib.request

# The standard browser endpoint you were natively using to get data
target_url = "https://reddit.com"

print("📡 Connecting directly to the live subreddit JSON grid endpoint...")

try:
    # Set a native browser User-Agent to bypass standard automated request blocks
    req = urllib.request.Request(
        target_url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )

    with urllib.request.urlopen(req) as response:
        # Load the raw buffer straight as an independent JSON tree layout
        raw_data = json.loads(response.read().decode('utf-8'))

    # Isolate the core listing children array from the root response payload
    posts_pool = raw_data['data']['children']
    print(f"📊 Captured {len(posts_pool)} live posts from the community index.")

    # Open your local project schema output file directly
    with open("reddit_archive.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Your exact TakeMeter columns
        writer.writerow(["text", "label", "note"])

        for entry in posts_pool:
            post_data = entry['data']

            # Combine the title and the selftext body string cleanly
            title = post_data.get('title', '')
            body = post_data.get('selftext', '')
            full_text = f"{title} {body}".strip()

            # Write row directly, letting the csv library safely escape quotes/commas
            writer.writerow([full_text, "", "Live Reddit API Feed"])

    print("\n✅ Success! File saved to your repository as 'reddit_archive.csv'")
    print("📁 Ready for your taxonomy label labs.")

except Exception as e:
    print(f"\n❌ Pipeline collection loop failed: {e}")
