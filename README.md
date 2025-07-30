# MSFT Powered Chatbot

A simple chatbot web application powered by Microsoft technologies. This project includes a Python backend and a static frontend for user interaction.

## Features
- Chatbot interface for user queries
- Simple login page
- Responsive design
- Docker support for easy deployment

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
Fong Chaitawat Boonk
