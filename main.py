from flask import Flask, request, jsonify, send_from_directory, session, redirect
from flask_cors import CORS
from dotenv import load_dotenv
from msal import ConfidentialClientApplication
from azure.identity import ClientSecretCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import ListSortOrder
import os, time

load_dotenv()
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

print("✅ ENV loaded.")
print("👉 CLIENT_ID:", os.getenv("AZURE_CLIENT_ID"))

app = Flask(__name__, static_folder="client", static_url_path="/")
app.secret_key = "super-secret-key"
CORS(app)

# 🔹 Azure Credential (ใช้ Service Principal)
credential = ClientSecretCredential(
   tenant_id = os.getenv("AZURE_TENANT_ID"),
    client_id=os.getenv("AZURE_CLIENT_ID"),
    client_secret=os.getenv("AZURE_CLIENT_SECRET")
)
print("🔎 Using Client ID:", os.getenv("AZURE_CLIENT_ID"))
# 🔹 Azure Foundry Agent Client (ใหม่)
agent_client = AgentsClient(
    endpoint=os.getenv("AGENT_PROJECT_URL"),
    credential=credential
    
)
AGENT_ID = os.getenv("AGENT_ID")


CLIENT_ID = os.getenv("AZURE_AD_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_AD_CLIENT_SECRET")
TENANT_ID = os.getenv("AZURE_AD_TENANT_ID")
REDIRECT_URI = os.getenv("AZURE_AD_REDIRECT_URI")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["User.Read"]

msal_app = ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)


@app.route("/")
def root():
    return send_from_directory("client/loginpage", "login.html")


@app.route("/login")
def login():
    auth_url = msal_app.get_authorization_request_url(
        scopes=SCOPE,
        redirect_uri=REDIRECT_URI
    )
    return redirect(auth_url)


@app.route("/auth/callback")
def callback():
    code = request.args.get("code")
    token = msal_app.acquire_token_by_authorization_code(
        code, scopes=SCOPE, redirect_uri=REDIRECT_URI
    )
    if "id_token_claims" in token:
        session["user"] = token["id_token_claims"]
        return redirect("/index.html")
    return "Login failed", 401


@app.route("/index.html")
def index_page():
    if "user" in session:
        return send_from_directory("client", "index.html")
    return redirect("/")


@app.route("/me")
def me():
    if "user" in session:
        return jsonify(session["user"])
    return jsonify({"error": "unauthorized"}), 401

# 🟢 Ask the agent
# @app.route("/ask", methods=["POST"])
# def ask():
#     if "user" not in session:
#         return jsonify({"error": "not authenticated"}), 401

#     user_input = request.json.get("message", "")
#     if not user_input:
#         return jsonify({"error": "No input"}), 400

#     try:
#         # ✅ Create thread if not exist
#         if "thread_id" not in session:
#             thread = agent_client.threads.create()
#             session["thread_id"] = thread.id
#         else:
#             thread = agent_client.threads.get(session["thread_id"])

#         # ✅ Send user message
#         agent_client.messages.create(thread_id=thread.id, role="user", content=user_input)

#         # ✅ Run agent
#         run = agent_client.runs.create_and_process(thread_id=thread.id, agent_id=AGENT_ID)

#         # ✅ Wait for run to complete
#         while run.status in ("queued", "in_progress"):
#             time.sleep(1)
#             run = agent_client.runs.get(thread_id=thread.id, run_id=run.id)

#         # ✅ Get latest assistant message
#         messages = agent_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
#         for m in messages:
#             if m.role == "assistant" and m.text_messages:
#                 return jsonify({"reply": m.text_messages[-1].text.value})

#         return jsonify({"reply": "❌ ไม่มีข้อความตอบกลับ"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
@app.route("/ask", methods=["POST"])
def ask():
    if "user" not in session:
        return jsonify({"error": "not authenticated"}), 401

    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "No input"}), 400

    try:
    
        if "thread_id" not in session:
            thread = agent_client.threads.create()
            session["thread_id"] = thread.id
            print("✅ Created new thread:", thread.id)
        else:
            thread = agent_client.threads.get(session["thread_id"])
            print("✅ Using existing thread:", thread.id)

       
        agent_client.messages.create(thread_id=thread.id, role="user", content=user_input)

      
        run = agent_client.runs.create_and_process(thread_id=thread.id, agent_id=AGENT_ID)

     
        while run.status in ("queued", "in_progress"):
            time.sleep(1)
            run = agent_client.runs.get(thread_id=thread.id, run_id=run.id)

       

        # --- โค้ดเดิม ---
        # messages = agent_client.messages.list(thread_id=thread.id, order=ListSortOrder.DESCENDING)
        # for m in messages:
        #     if m.role == "assistant" and m.text_messages:
        #         return jsonify({"reply": m.text_messages[0].text.value})
        # return jsonify({"reply": "❌ ไม่มีข้อความตอบกลับ"})

        # --- โค้ดใหม่: ตรวจสอบคำตอบซ้ำ/ใหม่ ---
        messages = agent_client.messages.list(thread_id=thread.id, order=ListSortOrder.DESCENDING)
        last_reply = None
        last_status = ""
        for m in messages:
            if m.role == "assistant" and m.text_messages:
                last_reply = m.text_messages[0].text.value
                break

        prev_reply = session.get("last_reply")
        if last_reply:
            if prev_reply == last_reply:
                last_status = "duplicate"
                reply_text = f"(ตอบซ้ำ) {last_reply}"
            else:
                last_status = "new"
                reply_text = last_reply
            session["last_reply"] = last_reply
            return jsonify({"reply": reply_text, "status": last_status})
        else:
            return jsonify({"reply": "❌ ไม่มีข้อความตอบกลับ", "status": "no_response"})

    except Exception as e:
        print("🔥 ERROR:", e)  
        return jsonify({"error": str(e)}), 500



@app.route("/logout")
def logout():
    session.clear()
   
    logout_url = (
        "https://login.microsoftonline.com/common/oauth2/v2.0/logout"
        f"?post_logout_redirect_uri=http://localhost:3000/"
    )
    return redirect(logout_url)




@app.route("/loginpage/<path:path>")
def login_assets(path):
    return send_from_directory(os.path.join(app.static_folder, "loginpage"), path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)


@app.route("/test-agent")
def test_agent():
    try:
        thread = agent_client.threads.create()
        print(f"✅ Created thread: {thread.id}")
        return jsonify({"status": "connected", "thread_id": thread.id})
    except Exception as e:
        print("🔥 Error in /test-agent:", e)
        return jsonify({"error": str(e)}), 500
