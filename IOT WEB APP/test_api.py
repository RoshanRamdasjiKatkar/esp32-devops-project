import urllib.request
import json
import time

BASE_URL = "http://localhost:5000/api/device"

def test_api():
    print("--- Step 1: Checking initial device status ---")
    req = urllib.request.Request(BASE_URL, method="GET")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode())
        print(f">> Initial state verified: {data}")

    print("--- Step 2: Sending ON command with 75% brightness ---")
    payload = json.dumps({"status": "ON", "brightness": 75}).encode('utf-8')
    req = urllib.request.Request(BASE_URL, data=payload, headers={'Content-Type': 'application/json'}, method="POST")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode())
        assert data["current_state"]["brightness"] == 75
        assert data["current_state"]["status"] == "ON"
        print(">> [PASS] Dimmer set to 75% verified")

    print("--- Step 3: Negative Test (Invalid brightness 150) ---")
    bad_payload = json.dumps({"brightness": 150}).encode('utf-8')
    bad_req = urllib.request.Request(BASE_URL, data=bad_payload, headers={'Content-Type': 'application/json'}, method="POST")
    try:
        urllib.request.urlopen(bad_req)
        assert False, "API should have rejected brightness > 100!"
    except urllib.error.HTTPError as e:
        assert e.code == 400
        print(">> [PASS] API successfully rejected invalid input with 400 Bad Request")

    print("\n=======================================================")
    print(">>> ALL API INTEGRATION TESTS PASSED SUCCESSFULLY! <<<")
    print("=======================================================\n")

if __name__ == "__main__":
    test_api()