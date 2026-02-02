import requests
import base64
import json

# --- CONFIGURATION (ENTER YOUR DETAILS HERE) ---
GITHUB_TOKEN = ""  # e.g. ghp_xyz123...
REPO_FULL_NAME = Paladincode3/law-enforcement-bulletin # e.g. rschwenk/le-bulletin
BRANCH = "main" # or "master"

# --- THE CONTENT ---
# This dictionary contains the path and the HTML code for each file.
# I have pre-filled it with the SCOTUS, 6th Circuit, and placeholder State pages.

files_to_deploy = {
    
    # 1. SCOTUS PAGE
    "scotus/index.html": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SCOTUS Updates</title>
    <style>body{font-family:sans-serif;color:#333;margin:2rem;}</style>
</head>
<body>
    <h1>Supreme Court Decisions (2020-2026)</h1>
    <p>Please refer to the detailed list generated in our previous chat.</p>
    <a href="../index.html">Back to Home</a>
</body>
</html>
""",

    # 2. SIXTH CIRCUIT PAGE
    "circuits/sixth_circuit.html": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>6th Circuit Updates</title>
</head>
<body>
    <h1>6th Circuit Court of Appeals (OH, KY, MI, TN)</h1>
    <h2>Recent Decisions</h2>
    <ul>
        <li><strong>Salter v. City of Detroit (2025):</strong> Brady violations & Qualified Immunity.</li>
        <li><strong>Novak v. City of Parma (2024):</strong> First Amendment & Parody accounts.</li>
    </ul>
    <a href="../index.html">Back to Home</a>
</body>
</html>
""",

    # 3. OHIO STATE PAGE (New!)
    "states/ohio.html": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ohio Law Enforcement News</title>
</head>
<body>
    <h1>Ohio Law Enforcement Bulletin</h1>
    <h2>Legislative Updates (2025-2026)</h2>
    <ul>
        <li><strong>Marijuana (Issue 2):</strong> Continued updates on plain smell/search probable cause protocols.</li>
        <li><strong>HB 230:</strong> Increases penalties for drug trafficking (fentanyl).</li>
    </ul>
    <a href="../index.html">Back to Home</a>
</body>
</html>
""",

    # 4. PENNSYLVANIA STATE PAGE (New!)
    "states/pennsylvania.html": """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pennsylvania Law Enforcement News</title>
</head>
<body>
    <h1>Pennsylvania Law Enforcement Bulletin</h1>
    <h2>Legislative Updates (2025-2026)</h2>
    <ul>
        <li><strong>Act 57:</strong> Updates on officer background check database requirements.</li>
        <li><strong>Clean Slate 3.0:</strong> New automated sealing of criminal records affecting background checks.</li>
    </ul>
    <a href="../index.html">Back to Home</a>
</body>
</html>
"""
}

# --- THE DEPLOYMENT FUNCTION ---
def push_to_github(filename, content):
    url = f"https://api.github.com/repos/{REPO_FULL_NAME}/contents/{filename}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # 1. Check if file exists (to get its SHA for updating)
    get_response = requests.get(url, headers=headers)
    sha = None
    if get_response.status_code == 200:
        sha = get_response.json()['sha']
        print(f"Updating existing file: {filename}")
    else:
        print(f"Creating new file: {filename}")

    # 2. Prepare the payload
    message = f"Automated update of {filename}"
    content_b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    
    data = {
        "message": message,
        "content": content_b64,
        "branch": BRANCH
    }
    if sha:
        data["sha"] = sha

    # 3. Push the update
    put_response = requests.put(url, headers=headers, data=json.dumps(data))
    
    if put_response.status_code in [200, 201]:
        print(f"✅ Success: {filename}")
    else:
        print(f"❌ Error {put_response.status_code}: {put_response.text}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("Starting automated deployment...")
    for path, code in files_to_deploy.items():
        push_to_github(path, code)
    print("\nDeployment complete! Check your repository.")
