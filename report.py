from datetime import datetime
 
 
def build_report(results: list, total_fetched: int) -> str:
    """Build a Markdown report from filtered notifications and their summaries."""
    today = datetime.now().strftime("%d/%m/%Y %H:%M")
 
    report = f"# RASFF Monitor — Report {today}\n\n"
    report += f"**Notifiche analizzate:** {total_fetched}\n"
    report += f"**Notifiche rilevanti:** {len(results)}\n\n"
    report += "---\n\n"
 
    for notification, summary in results:
        report += f"## [{notification['reference']}] {notification['subject']}\n"
        report += f"- **Rischio:** {notification['riskDecision']['description']}\n"
        report += f"- **Classificazione:** {notification['notificationClassification']['description']}\n"
        report += f"- **Paese notificante:** {notification['notifyingCountry']['organizationName']}\n"
        report += f"- **Origine:** {', '.join(c['isoCode'] for c in notification['originCountries'])}\n\n"
        report += f"### Brief operativo\n{summary}\n\n"
        report += "---\n\n"
 
    return report
 
 
def save_report(report: str, path: str = "reports/report.md"):
    """Save the report to a Markdown file."""
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report saved to {path}")