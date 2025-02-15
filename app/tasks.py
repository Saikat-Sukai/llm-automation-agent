import subprocess
import os
import json
from datetime import datetime
from utils import resolve_data_path

def execute_steps(steps):
    for step in steps:
        action = step.get('action')
        try:
            if action == 'install_tool':
                install_tool(step.get('name'), step.get('version'))
            elif action == 'run_script':
                run_script(step.get('command'))
            elif action == 'process_dates':
                process_dates(step['input'], step['output'], step['weekday'])
            elif action == 'sort_json':
                sort_json(step['input'], step['output'])
            # Add other actions here
        except Exception as e:
            raise RuntimeError(f"Error executing step {action}: {str(e)}")

def install_tool(name, version=None):
    if name == 'prettier':
        pass  # Handled via npx
    else:
        subprocess.run(f"pip install {name}{'=='+version if version else ''}", shell=True, check=True)

def run_script(command):
    expanded_command = os.path.expandvars(command)
    subprocess.run(expanded_command, shell=True, check=True)

def process_dates(input_path, output_path, weekday):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    target = weekdays.index(weekday)
    input_file = resolve_data_path(input_path)
    output_file = resolve_data_path(output_path)
    with open(input_file, 'r') as f:
        dates = [line.strip() for line in f]
    count = 0
    for date_str in dates:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if date.weekday() == target:
            count +=1
    with open(output_file, 'w') as f:
        f.write(str(count))

def sort_json(input_path, output_path):
    input_file = resolve_data_path(input_path)
    output_file = resolve_data_path(output_path)
    with open(input_file, 'r') as f:
        data = json.load(f)
    data.sort(key=lambda x: (x['last_name'], x['first_name']))
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)