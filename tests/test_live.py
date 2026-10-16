import urllib.request
import json

def call_endpoint(url, method="GET", data=None, token=None):
    req = urllib.request.Request(url, method=method)
    req.add_header("Accept", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    if data:
        req.add_header("Content-Type", "application/json")
        body = json.dumps(data).encode("utf-8")
    else:
        body = None
    with urllib.request.urlopen(req, data=body) as res:
        return json.loads(res.read().decode("utf-8"))

if __name__ == "__main__":
    print("1. Testing Root HTML / JSON...")
    root_data = call_endpoint("http://localhost:5000/")
    print("Root API directory endpoints:", list(root_data.get("endpoints", {}).keys()))

    print("\n2. Testing Anonymous User Creation...")
    user_data = call_endpoint("http://localhost:5000/api/v1/auth/anonymous", method="POST")
    token = user_data["data"]["access_token"]
    anon_id = user_data["data"]["anonymous_id"]
    print(f"Created Anonymous User ID: {anon_id}")

    print("\n3. Testing Goals Selection...")
    goal_res = call_endpoint("http://localhost:5000/api/v1/goals/select", method="POST", data={"goal_slugs": ["pronunciation", "interview"]}, token=token)
    print(f"Activated {len(goal_res['data'])} goals")

    print("\n4. Testing Diagnostic Assessment Query...")
    diag_res = call_endpoint("http://localhost:5000/api/v1/assessments/pronunciation/diagnostic")
    print(f"Diagnostic Title: {diag_res['data']['title']}, Questions: {len(diag_res['data']['questions'])}")

    print("\n5. Testing Recommendations Generation...")
    rec_res = call_endpoint("http://localhost:5000/api/v1/recommendations/pronunciation", token=token)
    print(f"Personalized Recommendations count: {len(rec_res['data'])}")

    print("\n6. Testing Dashboard Analytics...")
    dash_res = call_endpoint("http://localhost:5000/api/v1/dashboard", token=token)
    print("Dashboard Goals:", [g["goal_name"] for g in dash_res["data"]["goals"]])

    print("\nSUCCESS: All backend flows are working and responding properly!")
