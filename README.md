# **Sonar**  
A powerful and sleek Discord bot for playing YouTube videos in voice channels.

---

## 🎵 **Features**  
- **High-Quality Playback**: Streams music directly from YouTube into your Discord voice channels.  
- **User-Friendly Commands**: Intuitive controls for playing, pausing, skipping, and managing your queue.  
- **Seamless Experience**: Low latency, ensuring uninterrupted music playback.

---

## 🚀 **Getting Started**  

### **Invite Sonar to Your Server**  
Click [here](https://discord.com/oauth2/authorize?client_id=1311430813962862612) to invite Sonar to your Discord server!  

### **Installation (Self-Hosting)**  
1. Clone this repository:  
   ```bash
   git clone https://github.com/ProunceDev/SonarBot.git
   cd sonarbot
   ```  
2. Set up a Python virtual environment (optional but recommended):  
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```  
3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  
4. Set up the `.env` file with your bot token. ( If it doesn't exist then create it. ):  
   ```env
   discord_token=your_discord_bot_token
   ```  
5. Start the bot:  
   ```bash
   python main.py
   ```  

---

## 📜 **Commands**  

| Command          | Description                                   | Example              |
|-------------------|-----------------------------------------------|----------------------|
| `/play [url]`    | Add a youtube video / playlist to the queue.  | `/play https://youtu.be/example` |
| `/stop`          | Stop the playback and clear queue             | `/stop`              |
| `/pause`         | Pause the current playback                    | `/pause`             |
| `/resume`        | Resume playback                               | `/resume`            |
| `/skip`          | Skip the current track                        | `/skip`              |
| `/queue`         | Show the current queue                        | `/queue`             |
| `/leave`         | Disconnect the bot from the voice channel     | `/leave`             |

---

## 🛠️ **Development**  

### **Prerequisites**  
- Python (3.8 or higher)  
- Discord Developer Account

---

## ❤️ **Contributing**  
We welcome contributions to improve Sonar!  
1. Fork the repository.  
2. Create a new feature branch:  
   ```bash
   git checkout -b feature/your-feature-name
   ```  
3. Commit your changes:  
   ```bash
   git commit -m "Add your message here"
   ```  
4. Push to your branch and submit a pull request.  

---

## 📄 **License**  
This project is licensed under the [MIT License](LICENSE).  

---

## 🌐 **Connect With Us**  
Have feedback or questions? Reach out to us:  
- [Discord Support Server](https://discord.gg/caxhREJH)  
- [GitHub Issues](https://github.com/ProunceDev/SonarBot/issues)  
