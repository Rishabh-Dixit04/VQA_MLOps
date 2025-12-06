# import requests
# import json
# import time
# import sys

# # --- CONFIGURATION ---
# ES_URL = "http://localhost:9200"
# INDEX_PATTERN = "filebeat-*"
# THRESHOLD = 0.75
# JENKINS_URL = "http://localhost:8080"
# JOB_NAME = "vqa-pipeline"
# # USER/TOKEN if needed (leave empty for local anonymous)
# JENKINS_USER = "Rishabh_6181142168662382697"
# JENKINS_TOKEN = "admin" 

# def check_and_trigger():
#     print(f"\n[{time.strftime('%H:%M:%S')}] 🔍 Watchdog: Checking Model Health...")
    
#     # 1. Query Last 1 Hour (Widened window to fix Timezone issues)
#     query = {
#         "size": 1,
#         "sort": [{"@timestamp": {"order": "desc"}}], # Get the LATEST log
#         "query": {
#             "bool": {
#                 "must": [
#                     {"match_phrase": {"message": "LOG_METRIC"}}, 
#                     {"range": {"@timestamp": {"gte": "now-1h", "lt": "now"}}}
#                 ]
#             }
#         }
#     }

#     try:
#         response = requests.get(f"{ES_URL}/{INDEX_PATTERN}/_search", json=query)
#         data = response.json()
        
#         hits = data.get('hits', {}).get('hits', [])
        
#         if not hits:
#             print("   -> No recent inference logs found. System idle.")
#             return

#         # Parse the most recent log
#         latest_log = hits[0]['_source']['message']
#         # Extract the dictionary string from the log message
#         # Format is "LOG_METRIC: { ... }"
#         try:
#             json_str = latest_log.split("LOG_METRIC: ")[1].replace("'", '"')
#             metrics = json.loads(json_str)
#             quality = metrics.get('quality_score', 1.0)
            
#             print(f"   -> Latest Request: '{metrics.get('question')}'")
#             print(f"   -> Quality Score: {quality}")

#             if quality < THRESHOLD:
#                 print(f"   ⚠️ ALERT: Score {quality} is below threshold {THRESHOLD}!")
#                 trigger_jenkins()
#             else:
#                 print("   ✅ System Healthy.")
                
#         except Exception as parse_err:
#             print(f"   -> parsing error (ignoring): {parse_err}")

#     except Exception as e:
#         print(f"   -> Connection Error: {e}")

# def trigger_jenkins():
#     print("   🚀 TRIGGERING RETRAINING PIPELINE...")
#     # Add crumbtrail or auth if needed, but for local demo simple POST often works
#     trigger_url = f"{JENKINS_URL}/job/{JOB_NAME}/build"
#     try:
#         # Use simple auth if you set it up, otherwise try basic
#         # res = requests.post(trigger_url, auth=(JENKINS_USER, JENKINS_TOKEN))
#         res = requests.post(trigger_url)
        
#         if res.status_code in [200, 201]:
#             print("   ✅ Pipeline Triggered Successfully!")
#             # Sleep to prevent spamming triggers for the same bad log
#             print("   💤 Cooling down for 30 seconds...")
#             time.sleep(30) 
#         else:
#             print(f"   ❌ Jenkins Trigger Failed: {res.status_code}")
#     except Exception as e:
#         print(f"   ❌ Jenkins Call Error: {e}")

# if __name__ == "__main__":
#     print("--- MLOps Watchdog Service Started ---")
#     print("Press Ctrl+C to stop.")
#     while True:
#         check_and_trigger()
#         time.sleep(10) # Run check every 10 seconds

import requests
import json
import time
import sys

# --- CONFIGURATION ---
ES_URL = "http://localhost:9200"
INDEX_PATTERN = "filebeat-*"
THRESHOLD = 0.75

# JENKINS CONFIG
JENKINS_URL = "http://localhost:8080"
JOB_NAME = "VQA_MLOps"  # Ensure this matches your job name EXACTLY
JENKINS_USER = "Rishabh_6181142168662382697"  # <--- PUT YOUR USERNAME HERE
JENKINS_PASS = "admin" # <--- PUT YOUR PASSWORD HERE

def check_and_trigger():
    print(f"\n[{time.strftime('%H:%M:%S')}] 🔍 Watchdog: Checking Model Health...")
    
    # 1. Query Last 24 Hours (To ensure we find your recent test)
    query = {
        "size": 1,
        "sort": [{"@timestamp": {"order": "desc"}}], 
        "query": {
            "bool": {
                "must": [
                    {"match_phrase": {"message": "LOG_METRIC"}}, 
                    {"range": {"@timestamp": {"gte": "now-24h", "lt": "now"}}}
                ]
            }
        }
    }

    try:
        response = requests.get(f"{ES_URL}/{INDEX_PATTERN}/_search", json=query)
        data = response.json()
        hits = data.get('hits', {}).get('hits', [])
        
        if not hits:
            print("   -> No inference logs found.")
            return

        # Parse Log
        latest_log = hits[0]['_source']['message']
        json_str = latest_log.split("LOG_METRIC: ")[1].replace("'", '"')
        metrics = json.loads(json_str)
        quality = metrics.get('quality_score', 1.0)
        
        print(f"   -> Latest Score: {quality}")

        if quality < THRESHOLD:
            print(f"   ⚠️ ALERT: Score {quality} < {THRESHOLD}")
            trigger_jenkins()
        else:
            print("   ✅ System Healthy.")

    except Exception as e:
        print(f"   -> Check Error: {e}")

def trigger_jenkins():
    print("   🚀 TRIGGERING RETRAINING PIPELINE...")
    
    session = requests.Session()
    session.auth = (JENKINS_USER, JENKINS_PASS)

    try:
        # 1. Get CSRF Crumb (The Key to fixing 403)
        crumb_url = f"{JENKINS_URL}/crumbIssuer/api/json"
        crumb_resp = session.get(crumb_url)
        
        headers = {}
        if crumb_resp.status_code == 200:
            crumb_data = crumb_resp.json()
            headers[crumb_data['crumbRequestField']] = crumb_data['crumb']
            print("   -> CSRF Crumb obtained.")
        else:
            print("   -> Warning: Could not get CSRF crumb (might be disabled).")

        # 2. Trigger Build
        build_url = f"{JENKINS_URL}/job/{JOB_NAME}/build"
        res = session.post(build_url, headers=headers)
        
        if res.status_code in [200, 201]:
            print("   ✅ Pipeline Triggered Successfully!")
            print("   💤 Cooling down for 30 seconds...")
            time.sleep(30) 
        else:
            print(f"   ❌ Trigger Failed: {res.status_code} - {res.reason}")
            
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")

if __name__ == "__main__":
    print("--- Watchdog Started ---")
    while True:
        check_and_trigger()
        time.sleep(10)