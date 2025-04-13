# Global job ID counter  -- this resets in every run, so doesn't work
#job_id_counter = {
#    'talent': 0,
#    'monster': 0
#}

import json
import os

COUNTER_FILE = "job_id_counter.json"

# Load counter from file or create default
def load_job_id_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as file:
            return json.load(file)
    else:
        return {'talent': 0, 'monster': 0}

# Save updated counter
def save_job_id_counter(counter):
    with open(COUNTER_FILE, "w") as file:
        json.dump(counter, file)

job_id_counter = load_job_id_counter()