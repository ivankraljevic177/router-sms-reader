# Router SMS Reader

A Flask web application for reading SMS messages from your router.

## 🌐 Live Demo

[![Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/ivankraljevic177/router-sms-reader)

## 📋 Features

- Read SMS messages from your router
- Simple web interface with IP and password input
- Secure (passwords not stored)
- Responsive design

## 🚀 Quick Start

### Local Development

```bash
# Clone the repo
git clone https://github.com/ivankraljevic177/router-sms-reader.git
cd router-sms-reader

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open browser
http://localhost:5000
```

### Usage

1. Enter your router's IP address (e.g., 192.168.8.1)
2. Enter your router admin password
3. Click "Get SMS Messages"
4. View messages in the table

## 📦 Requirements

- Python 3.7+
- Flask 3.0+
- requests 2.31+

## 🔒 Security

- Passwords are NOT stored
- Each request requires re-authentication
- Uses HTTPS in production

## 📱 Screenshots

![Router SMS Reader Screenshot](https://via.placeholder.com/800x500.png?text=Router+SMS+Reader+Screenshot)

## 🎯 Deployment

### Render.com (Recommended)

1. Go to [Render.com](https://render.com/)
2. Click "New Web Service"
3. Connect your GitHub account
4. Select this repository
5. Configure:
   - **Name:** router-sms-reader
   - **Region:** Frankfurt (or closest)
   - **Branch:** main
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. Click "Create Web Service"
7. Wait for deployment (~2-5 minutes)
8. Your app will be live at: `https://router-sms-reader.onrender.com`

### PythonAnywhere

1. Go to [PythonAnywhere](https://www.pythonanywhere.com/)
2. Create a free account
3. Go to "Files" tab and upload all files
4. Open "Bash" console and run:
   ```bash
   pip install -r requirements.txt
   ```
5. Go to "Web" tab and configure:
   - **Source code:** `/home/yourusername/router-sms-reader`
   - **WSGI configuration file:** `/var/www/yourusername_pythonanywhere_com_wsgi.py`
   - **Virtualenv:** `/home/yourusername/.virtualenvs/yourvirtualenv`
6. Reload your web app
7. Your app will be live at: `https://yourusername.pythonanywhere.com`

## 📝 License

MIT License

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

## 📞 Support

For issues or questions, please open a GitHub issue.

---

**Created by:** Ivan Kraljević
**GitHub:** https://github.com/ivankraljevic177/router-sms-reader