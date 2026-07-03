<div align="center">

# ⚡ Nexcord Tools v1.0 Beta
**The Ultimate All-in-One Discord Utility Suite**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.3+-purple.svg)](https://discordpy.readthedocs.io/)
[![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-ff69b4.svg)](https://customtkinter.tomschimansky.com/)
[![Version](https://img.shields.io/badge/Version-1.0_Beta-orange.svg)]()
[![Status](https://img.shields.io/badge/Status-Working-brightgreen.svg)]()
[![Made by Amir48_0](https://img.shields.io/badge/Made%20by-Amir48__0-9cf.svg)](https://github.com/Amir48Zero)

Nexcord Tools is a modern, fast, and feature-rich Discord management tool. Featuring a sleek dark-mode UI, it handles everything from Custom Rich Presence (RPC), server administration, and account management to high-speed webhooks and deep server cloning.

</div>

---

## 🌟 Features

### 🎮 Discord Custom RPC (Standalone)
*   **No Bot Required:** Works independently using your Application Client ID.
*   **Full Customization:** Set Details, State, and Timestamps.
*   **Assets Support:** Add Large and Small images (uploaded via Discord Developer Portal).
*   **Interactive Buttons:** Add up to 2 fully clickable custom buttons with URLs.

### 💣 Server Management (Bot Token Required)
*   **Channel Actions:** Nuke, Spam (Bulk Create), Rename all channels.
*   **Role Actions:** Nuke, Spam (Bulk Create) roles with custom names.
*   **Member Actions:** Mass Kick, Mass Ban, Mass Nickname.
*   **Admin Utilities:** Lock/Unlock server, Purge messages, Delete all emojis, Change server name.

### 👤 Account Tools (Bot Token Required)
*   Edit Bot profile (Username & Avatar).
*   Create new servers instantly.
*   Join servers via Invite URL or Leave servers via ID.
*   Send direct messages to specific User IDs.

### 🔗 Webhook Spammer (No Token Needed)
*   Send single or bulk messages (10x rapid fire).
*   Custom webhook username override.
*   Bypasses standard bot rate-limits.

### 🔄 Advanced Server Cloner (User Token Required)
*   **Deep Clone Engine:** Uses raw Discord API requests to bypass standard library visibility limits.
*   Clones hidden/private channels seamlessly.
*   Perfectly copies Roles (Colors, Permissions, Hoist status).
*   Perfectly copies Categories, Text Channels, and Voice Channels with exact permissions and positions.

---

## 🛠️ Installation

### Prerequisites
*   Python 3.8 or higher.
*   A Discord Bot Token (from [Discord Developer Portal](https://discord.com/developers/applications)).
*   Your personal User Token (for the Cloner tab).
*   An Application Client ID (for the RPC tab).

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Amir48Zero/NexcordTools.git
   cd NexcordTools
   ```

2. **Run the Auto-Installer:**
   *   Just double-click the `Run.bat` file!
   *   It will automatically check for Python, install all required libraries, and launch the tool for you.

---

## ⚙️ Configuration & Usage

### 1. RPC Setup
*   Go to [Discord Developer Portal](https://discord.com/developers/applications), create an application, and copy the **Client ID**.
*   To use images, go to **Rich Presence** -> **Art Assets** and upload your images. Use the exact "Asset Name" in the tool (not image URLs).

### 2. Bot Setup (For Server & Account Tabs)
To use the bot features, you must enable specific privileges in the [Discord Developer Portal](https://discord.com/developers/applications):
1. Go to your Bot application -> **Bot** tab.
2. Scroll down to **Privileged Gateway Intents**.
3. Turn **ON**:
   *   `Message Content Intent`
   *   `Server Members Intent`
4. Copy the Bot Token and paste it into the main UI.

### 3. Cloner Setup (For Cloner Tab)
The cloner does *not* use the discord.py library. It requires your **Personal User Token** to interact directly with the Discord API.
*   **Source Server ID:** The server you want to copy.
*   **Destination Server ID:** Your empty server where everything will be copied to.
*   *Note: Your user account must have "Manage Channels" and "Manage Roles" permissions in BOTH servers.*

---

## 📸 UI Preview

![Nexcord UI](https://i.imgur.com/oIM5mNE.png)

---

## ⚠️ Disclaimer

**Educational Purpose Only.** 
This tool interacts with Discord in ways that violate their [Terms of Service](https://discord.com/terms) (specifically self-botting and automated nuking/raiding). I am not responsible for any account terminations, IP bans, or legal actions taken against you for using this software improperly. Use it at your own risk on servers you own or have explicit permission to test on.

---

## 📜 Credits
*   Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
*   Powered by [discord.py](https://github.com/Rapptz/discord.py), [pypresence](https://github.com/qwertyquerty/pypresence) & [Requests](https://github.com/psf/requests)
*   Developed by **Amir48_0**

<div align="center">
Made with ❤️ & Python
</div>
