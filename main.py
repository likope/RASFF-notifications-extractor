from fetcher import fetch_notifications
from filter import load_config, match_filters
from summarizer import summarize_notification
from report import build_report, save_report


def main():
    print("=== RASFF Monitor ===\n")

    # 1. Fetch
    print("Fetching notifications...")
    notifications = fetch_notifications(max_pages=1, per_page=25)
    print(f"Fetched {len(notifications)} notifications.\n")

    if not notifications:
        print("No notifications found. Exiting.")
        return

    # 2. Filter
    print("Applying filters...")
    config = load_config()
    filtered = match_filters(notifications, config)
    print(f"Filtered: {len(filtered)} notifications match.\n")

    if not filtered:
        print("No notifications match the filters. Exiting.")
        return

    # 3. Summarize
    print("Generating summaries...\n")
    results = []
    for n in filtered:
        print(f"  Summarizing [{n['reference']}] {n['subject']}...")
        summary = summarize_notification(n)
        results.append((n, summary))

    # 4. Report
    report = build_report(results, total_fetched=len(notifications))
    save_report(report)

    print(f"\nDone. {len(results)} notifications summarized.")


if __name__ == "__main__":
    main()