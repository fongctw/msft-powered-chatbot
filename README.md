# MSFT Powered Chatbot

A chatbot web application powered by Microsoft technologies. This project includes a Python backend and a static frontend for user interaction.

## Features
- Chatbot interface for user queries
- Login with Microsoft account (personal or organization ID)
- Docker support for easy deployment
- Specific domain knowledge: The chatbot can answer domain-specific questions via the integrated Foundry Agent

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
### How to Set Up Microsoft Integration
```
1. Azure AD App Registration (for Microsoft Login)
Go to Microsoft Entra ID > App registrations.

Register a new application (e.g., MSFTChatLogin).

Set a Redirect URI (e.g., http://localhost:3000/login/callback).

Copy Application (client) ID, Tenant ID, and generate a client secret.

Use these values in the .env section under Microsoft Login.

2. Service Principal for Foundry Agent
Create another App Registration (e.g., MSFTChatAgentAccess).

Generate a client secret and collect Client ID, Tenant ID.

Assign Cognitive Services User role to this Service Principal in Access Control (IAM) for the Azure AI Foundry resource.

3. Get Foundry Agent Info
Log into the Azure AI Foundry Portal.

Go to your agent project, find the Agent ID and Endpoint URL.

```

See further setup details in the code or Foundry Agent documentation.


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
