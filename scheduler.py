# scheduler.py
# Master scheduler for the whole daily automation
# scheduler.py
import os
from datetime import datetime
import yaml

from scraper import collect_data
from translator import detect_language, translate_text
from summarizer import summarize_text
from report_generator import generate_report
from git_manager import git_commit_and_push
from email_sender import send_email_report

def load_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

def main():
    print("🚀 Running full daily automation workflow...")

    # Step 1: Load config
    config = load_config()
    keywords = config["scraper_settings"]["keywords"]
    output_folder = config["daily_report_settings"]["output_folder"]
    repo_path = config["git_settings"]["repo_path"]

    # Step 2: Scrape content
    raw_contents = collect_data(keywords)
    print(f"✅ Collected {len(raw_contents)} items.")

    # Step 3: Translate content
    translated_contents = []
    for content in raw_contents:
        lang = detect_language(content)
        translated = translate_text(content, lang)
        translated_contents.append(translated)
    print("✅ Translation complete.")

    # Step 4: Summarize content
    summarized_contents = []
    for item in translated_contents:
        summarized = summarize_text(item)
        summarized_contents.append(summarized)
    print("✅ Summarization complete.")

    # Step 5: Generate Word Report
    today_date = datetime.now().strftime("%Y-%m-%d")
    report_path = generate_report(today_date, summarized_contents, output_folder)
    print(f"✅ Report generated at {report_path}")

    # Step 6: Git push
    git_commit_and_push(repo_path, f"Daily Report - {today_date}")

    # Step 7: Email the report (Optional)
    email_config = config["email_settings"]
    if email_config["sender_email"] and email_config["sender_password"]:
        send_email_report(
            sender_email=email_config["sender_email"],
            sender_password=email_config["sender_password"],
            receiver_email=email_config["receiver_email"],
            subject=f"Earthquake Monitoring Report - {today_date}",
            body="Attached is today's daily earthquake monitoring report.",
            attachment_path=report_path
        )

    print("🎉 All tasks completed successfully!")

if __name__ == "__main__":
    main()

print("Running full daily automation workflow...")