import os
import requests
import json

def generate_steps(task_description):
    prompt = f"""
    Parse the task into JSON steps. Use only allowed actions. All paths must be under /data. No deletions.
    Allowed actions: install_tool, run_script, process_dates, sort_json, process_logs, extract_h1, extract_email, extract_image_text, compute_similarity, run_sql_query, fetch_api, git_clone, scrape_website, process_image, transcribe_audio, markdown_to_html, filter_csv.

    Example Task: 'Count Wednesdays in /data/dates.txt and write to /data/dates-wednesdays.txt'
    Response: [{{"action": "process_dates", "input": "/data/dates.txt", "output": "/data/dates-wednesdays.txt", "weekday": "Wednesday"}}]

    Task: {task_description}
    """
    headers = {
        "Authorization": f"Bearer {os.environ['AIPROXY_TOKEN']}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000
    }
    response = requests.post("https://api.aiproxy.io/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()
    content = response.json()['choices'][0]['message']['content']
    return json.loads(content)