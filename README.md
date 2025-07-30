# MSFT Powered Chatbot

A chatbot web application powered by Microsoft technologies. This project includes a Python backend and a static frontend for user interaction.

MSFT Powered Chatbot is designed to be a **personal or organizational AI agent** that can securely integrate with your Microsoft ecosystem. Whether you're an individual looking for a smart assistant, or an enterprise deploying an internal knowledge bot, this chatbot can serve as your intelligent companion — connected to your tools, documents, and domain knowledge.

Built with support for Microsoft login (Azure AD), seamless Foundry Agent integration, and customizable prompts, this solution is both **secure** and **highly extensible**. Deploy it privately or across your organization to supercharge internal search, automate support, or drive decision-making with AI-powered insights.


## Features
- Chatbot interface for user queries
- Login with Microsoft account (supports both personal Microsoft accounts and organizational accounts via Microsoft Entra ID)
- Docker support for easy deployment
- Foundry Agent integration: Supports knowledge injection via Foundry features, such as:
  - Connecting to AI Search (RAG) for retrieval-augmented responses
  - Integrating with SharePoint, local documents, and other data sources
  - Configuring system prompts to shape the chatbot's behavior and personality

## Project Structure
```
msft-powered-chatbot/
├── Dockerfile
├── main.py
├── requirements.txt
├── client/
│   ├── index.html
│   ├── style.css
│   ├── vars.css
│   ├── assets/
│   │   └── idea.png
│   └── loginpage/
│       ├── login.css
│       └── login.html
```


---

## Foundry Agent Integration

MSFT Powered Chatbot can connect to **Foundry Agent** to enhance AI capabilities such as complex question answering, data access, and service integrations.

This allows the chatbot to provide more intelligent, specific, and context-aware answers, based on external system knowledge and advanced processing.

### Required Setup

To enable this integration, you must configure credentials in a `.env` file or as system environment variables:

### 🔐 `.env` Configuration

```env
# Microsoft Login (Azure AD App Registration)
AZURE_AD_CLIENT_ID=              # Application (client) ID of the app registration used for login
AZURE_AD_CLIENT_SECRET=          # Client secret generated in the app registration
AZURE_AD_TENANT_ID=              # Directory (tenant) ID from your Entra ID
AZURE_AD_REDIRECT_URI=           # Redirect URI set in app registration (e.g., http://localhost:5000/login/callback)

# Service Principal for Agent access
AZURE_CLIENT_ID=                 # Client ID of the Service Principal for accessing Foundry Agent
AZURE_CLIENT_SECRET=             # Secret for the Service Principal
AZURE_TENANT_ID=                 # Tenant ID (same as above if same directory is used)

# Foundry Agent
AGENT_PROJECT_URL=https://<your-agent-url>   # Foundry Agent endpoint (get this from Azure AI Foundry Portal)
AGENT_ID=<your_agent_id_here>                # Foundry Agent ID (also from the portal)
```
## 🔧 How to Set Up Microsoft Integration

To enable Microsoft login and connect to Azure AI Foundry Agent, follow these setup steps:

---

### 1. 🔐 Azure AD App Registration (for Microsoft Login)

This is used to allow users to log in with their Microsoft account.

- Go to **App registrations** > **New registration**
- Enter a name (e.g., `MSFTChatLoginAccess`)
- Set a **Redirect URI** (e.g., `http://localhost:3000/login/callback`)
- After registration:
  - Copy the **Application (client) ID**
  - Copy the **Directory (tenant) ID**
  - Go to **Certificates & secrets** and generate a **Client Secret**
- Use these values in the `.env` file under the **Microsoft Login** section

---

### 2. 🛠️ Service Principal for Foundry Agent Access

This service principal will be used to authenticate your chatbot to Azure AI Foundry.

- Go to **App registrations** > **New registration**
- Enter a name (e.g., `MSFTChatAgentAccess`)
- Register and generate a **Client Secret**
- Copy the **Client ID** and **Tenant ID**
- Go to your **Azure AI Foundry** resource > **Access Control (IAM)**
  - Click **Add role assignment**
  - Assign the **Cognitive Services User** role to this app registration

---

### 3. 🌐 Get Foundry Agent Information

To connect your chatbot with the correct Foundry Agent:

- Go to the [Azure AI Foundry Portal](https://portal.azure.com)
- Navigate to your **Agent Project**
- Copy the **Agent Endpoint URL**
-  Copy the **Agent ID**
- Add both values to the `.env` file under **Foundry Agent**

---

💡 For full integration, make sure all the corresponding values are set correctly in the `.env` file. See the `.env` section above for details.


## Getting Started

### Prerequisites
- Python 3.8+
- Docker (optional)

### Installation
1. Clone the repository:
   ```powershell
   git clone <repo-url>
   cd msft-powered-chatbot
   ```
2. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

### Running the Application
#### Using Python
```powershell
python main.py
```

#### Using Docker
Build and run the Docker container:
```powershell
docker build -t msft-powered-chatbot .
docker run -p 5000:5000 msft-powered-chatbot
```

### Accessing the Frontend
Open `client/index.html` in your browser or configure the backend to serve static files.

## File Descriptions
- `main.py`: Python backend server (Flask or FastAPI recommended)
- `requirements.txt`: Python dependencies
- `Dockerfile`: Container setup for deployment
- `client/index.html`: Main chatbot UI
- `client/style.css`, `client/vars.css`: Stylesheets
- `client/assets/idea.png`: Image asset
- `client/loginpage/login.html`, `client/loginpage/login.css`: Login page and styles

## Customization
- Update chatbot logic in `main.py`
- Modify UI in `client/index.html` and CSS files

## License
MIT License

## Author
Fong Chaitawat Boonkitticharoen
