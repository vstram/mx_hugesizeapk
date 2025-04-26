import psutil
import base64
import requests
import json

# Used to get the process ID
# https://psutil.readthedocs.io/en/latest/index.html#find-process-by-name
def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    ls = []
    for p in psutil.process_iter(['name']):
        if p.info['name'] == name:
            ls.append(p)
    return ls

# Get the M2EE password from the environment variables of the javaw process
def get_m2ee_password():
    pid = find_procs_by_name("javaw.exe")
    len_pid = len(pid)
    if len_pid == 0:
        print("No processes found")
        exit(1)
    elif len_pid > 1:
        print("More than one process found")
        exit(1)

    javaw_pid = pid[0].pid
    m2ee_admin_pass = psutil.Process(pid=javaw_pid).environ()["M2EE_ADMIN_PASS"]
    m2ee_admin_pass_b64 = base64.b64encode(m2ee_admin_pass.encode("ascii")).decode("ascii")

    print(f"Javaw Process ID: {javaw_pid}")
    print(f"Password: {m2ee_admin_pass}")
    print(f"Base64 encoded password: {m2ee_admin_pass_b64}")

    return m2ee_admin_pass_b64

# Get the runtime statistics from the M2EE admin API
def get_runtime_statistics():
    m2ee_admin_pass_b64 = get_m2ee_password()

    url = "http://localhost:8090/admin"

    payload = json.dumps({
    "action": "runtime_statistics",
    "params": {}
    })
    headers = {
    'Content-Type': 'application/json',
    'X-M2EE-Authentication': m2ee_admin_pass_b64
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text

runtime_statistics = get_runtime_statistics()
#print(f"Runtime statistics: {runtime_statistics}")
used_heap = json.loads(runtime_statistics)["feedback"]["memory"]["used_heap"]

print(f"Used heap: {used_heap / 1024 / 1024} MB")