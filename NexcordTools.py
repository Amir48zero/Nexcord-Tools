import customtkinter as ctk
import discord
import asyncio
import threading
import requests
import json
from pypresence import Presence

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NexcordBot(discord.Client):
    def __init__(self, log_func):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(intents=intents)
        self.log_func = log_func

    async def on_ready(self):
        self.log_func(f"[✅] Connected as {self.user.name} | ID: {self.user.id}")

class NexcordApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Nexcord Tools v1.0 Beta")
        self.geometry("820x780")
        self.resizable(False, False)
        
        self.bot = None
        self.loop = None
        self.rpc = None

        ctk.CTkLabel(self, text="⚡ Nexcord Tools ⚡", font=ctk.CTkFont(size=26, weight="bold"), text_color="#a855f7").pack(pady=15)

        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", padx=20)
        
        ctk.CTkLabel(input_frame, text="Bot Token:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.token_entry = ctk.CTkEntry(input_frame, width=450, show="*")
        self.token_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.start_btn = ctk.CTkButton(input_frame, text="Connect", fg_color="#22c55e", hover_color="#16a34a", width=120, command=self.start_bot_thread)
        self.start_btn.grid(row=0, column=2, padx=5, pady=5)

        self.tabview = ctk.CTkTabview(self, width=760, height=440)
        self.tabview.pack(padx=20, pady=10)

        self.tab_rpc = self.tabview.add("🎮 RPC")
        self.tab_server = self.tabview.add("💣 سرور")
        self.tab_account = self.tabview.add("👤 اکانت")
        self.tab_webhook = self.tabview.add("🔗 وب‌هوک")
        self.tab_cloner = self.tabview.add("🔄 کلونر")
        self.tab_help = self.tabview.add("📖 راهنما")

        self.setup_rpc_tab()
        self.setup_server_tab()
        self.setup_account_tab()
        self.setup_webhook_tab()
        self.setup_cloner_tab()
        self.setup_help_tab()

        ctk.CTkLabel(self, text="System Console:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20)
        self.log_box = ctk.CTkTextbox(self, height=120, state="disabled", fg_color="#0f0f0f", text_color="#d4d4d4")
        self.log_box.pack(fill="x", padx=20, pady=(0, 15))

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def start_bot_thread(self):
        if not self.token_entry.get():
            self.log("[❌] Token is empty.")
            return
        self.log("[⏳] Connecting...")
        self.start_btn.configure(state="disabled")
        threading.Thread(target=self._run_bot, daemon=True).start()

    def _run_bot(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.bot = NexcordBot(log_func=self.log)
        try:
            self.loop.run_until_complete(self.bot.start(self.token_entry.get()))
        except discord.LoginFailure:
            self.log("[❌] Invalid Token!")
            self.start_btn.configure(state="normal")

    def run_task(self, task_name, *args):
        if not self.bot or not self.bot.is_ready():
            self.log("[❌] Bot is not connected!")
            return
        asyncio.run_coroutine_threadsafe(self.execute_task(task_name, *args), self.loop)

    def setup_rpc_tab(self):
        f = ctk.CTkFrame(self.tab_rpc, fg_color="transparent")
        f.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(f, text="Client ID:").grid(row=0, column=0, padx=5, pady=3, sticky="w")
        self.rpc_id = ctk.CTkEntry(f, width=400)
        self.rpc_id.grid(row=0, column=1, padx=5, pady=3)

        ctk.CTkLabel(f, text="Details:").grid(row=1, column=0, padx=5, pady=3, sticky="w")
        self.rpc_details = ctk.CTkEntry(f, width=400)
        self.rpc_details.grid(row=1, column=1, padx=5, pady=3)

        ctk.CTkLabel(f, text="State:").grid(row=2, column=0, padx=5, pady=3, sticky="w")
        self.rpc_state = ctk.CTkEntry(f, width=400)
        self.rpc_state.grid(row=2, column=1, padx=5, pady=3)

        ctk.CTkLabel(f, text="Large Image:").grid(row=3, column=0, padx=5, pady=3, sticky="w")
        self.rpc_limg = ctk.CTkEntry(f, width=400, placeholder_text="Asset Name (Uploaded to Discord)")
        self.rpc_limg.grid(row=3, column=1, padx=5, pady=3)

        ctk.CTkLabel(f, text="Large Hover:").grid(row=4, column=0, padx=5, pady=3, sticky="w")
        self.rpc_lhover = ctk.CTkEntry(f, width=400)
        self.rpc_lhover.grid(row=4, column=1, padx=5, pady=3)

        ctk.CTkLabel(f, text="Small Image:").grid(row=5, column=0, padx=5, pady=3, sticky="w")
        self.rpc_simg = ctk.CTkEntry(f, width=400, placeholder_text="Asset Name (Uploaded to Discord)")
        self.rpc_simg.grid(row=5, column=1, padx=5, pady=3)

        ctk.CTkLabel(f, text="Small Hover:").grid(row=6, column=0, padx=5, pady=3, sticky="w")
        self.rpc_shover = ctk.CTkEntry(f, width=400)
        self.rpc_shover.grid(row=6, column=1, padx=5, pady=3)

        ctk.CTkLabel(f, text="Button 1 Text:").grid(row=7, column=0, padx=5, pady=3, sticky="w")
        self.rpc_b1t = ctk.CTkEntry(f, width=190)
        self.rpc_b1t.grid(row=7, column=1, padx=(5,2), pady=3, sticky="w")
        ctk.CTkLabel(f, text="URL:").grid(row=7, column=1, padx=(200,0), pady=3, sticky="w")
        self.rpc_b1u = ctk.CTkEntry(f, width=200)
        self.rpc_b1u.grid(row=7, column=1, padx=(220,5), pady=3, sticky="e")

        ctk.CTkLabel(f, text="Button 2 Text:").grid(row=8, column=0, padx=5, pady=3, sticky="w")
        self.rpc_b2t = ctk.CTkEntry(f, width=190)
        self.rpc_b2t.grid(row=8, column=1, padx=(5,2), pady=3, sticky="w")
        ctk.CTkLabel(f, text="URL:").grid(row=8, column=1, padx=(200,0), pady=3, sticky="w")
        self.rpc_b2u = ctk.CTkEntry(f, width=200)
        self.rpc_b2u.grid(row=8, column=1, padx=(220,5), pady=3, sticky="e")

        btn_f = ctk.CTkFrame(f, fg_color="transparent")
        btn_f.grid(row=9, column=0, columnspan=2, pady=15)
        ctk.CTkButton(btn_f, text="▶ Start RPC", fg_color="#22c55e", hover_color="#16a34a", width=200, command=self.start_rpc).pack(side="left", padx=10)
        ctk.CTkButton(btn_f, text="⏹ Stop RPC", fg_color="#dc2626", hover_color="#b91c1c", width=200, command=self.stop_rpc).pack(side="left", padx=10)

    def start_rpc(self):
        cid = self.rpc_id.get()
        if not cid:
            self.log("[❌] RPC Client ID is empty.")
            return
        try:
            self.rpc = Presence(cid)
            self.rpc.connect()
            buttons = []
            if self.rpc_b1t.get() and self.rpc_b1u.get():
                buttons.append({"label": self.rpc_b1t.get(), "url": self.rpc_b1u.get()})
            if self.rpc_b2t.get() and self.rpc_b2u.get():
                buttons.append({"label": self.rpc_b2t.get(), "url": self.rpc_b2u.get()})

            self.rpc.update(
                details=self.rpc_details.get(),
                state=self.rpc_state.get(),
                large_image=self.rpc_limg.get() if self.rpc_limg.get() else None,
                large_text=self.rpc_lhover.get() if self.rpc_lhover.get() else None,
                small_image=self.rpc_simg.get() if self.rpc_simg.get() else None,
                small_text=self.rpc_shover.get() if self.rpc_shover.get() else None,
                buttons=buttons if buttons else None
            )
            self.log("[✅] Custom RPC is now active!")
        except Exception as e:
            self.log(f"[❌] RPC Error: {e}")

    def stop_rpc(self):
        if self.rpc:
            try:
                self.rpc.close()
                self.log("[✅] RPC Closed.")
            except: pass

    def setup_server_tab(self):
        f = ctk.CTkFrame(self.tab_server, fg_color="transparent")
        f.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(f, text="Server ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.guild_entry = ctk.CTkEntry(f, width=300)
        self.guild_entry.grid(row=0, column=1, padx=5, pady=5)

        btn_data = [
            ("Nuke Channels", "nuke_ch", "#450a0a", "#dc2626"), ("Spam Channels (10x)", "spam_ch", "#450a0a", "#dc2626"), ("Rename Channels", "rename_ch", "#450a0a", "#dc2626"),
            ("Nuke Roles", "nuke_rl", "#450a0a", "#dc2626"), ("Spam Roles (10x)", "spam_rl", "#450a0a", "#dc2626"), ("Delete Emojis", "nuke_emoji", "#450a0a", "#dc2626"),
            ("Mass Kick", "kick", "#431407", "#f97316"), ("Mass Ban", "ban", "#431407", "#f97316"), ("Mass Nickname", "nick", "#431407", "#f97316"),
            ("Lock Server", "lock", "#172554", "#3b82f6"), ("Unlock Server", "unlock", "#172554", "#3b82f6"), ("Purge Messages", "purge", "#172554", "#3b82f6"),
            ("Change Server Name", "sname", "#14532d", "#22c55e")
        ]

        for i, (text, cmd, fg, hover) in enumerate(btn_data):
            row, col = divmod(i, 3)
            ctk.CTkButton(f, text=text, fg_color=fg, hover_color=hover, command=lambda c=cmd: self.run_task(c)).grid(row=row+1, column=col, padx=3, pady=3, sticky="nsew")

        for i in range(3):
            f.grid_columnconfigure(i, weight=1)

    def setup_account_tab(self):
        f = ctk.CTkFrame(self.tab_account, fg_color="transparent")
        f.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(f, text="Target ID / Invite URL:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.target_entry = ctk.CTkEntry(f, width=400)
        self.target_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(f, text="New Username:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.username_entry = ctk.CTkEntry(f, width=400)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(f, text="Image URL (for Avatar):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.avatar_entry = ctk.CTkEntry(f, width=400)
        self.avatar_entry.grid(row=2, column=1, padx=5, pady=5)

        btn_data = [
            ("Get Bot Info", "bot_info", "#1e293b", "#64748b"), ("Change Username", "change_uname", "#1e293b", "#64748b"),
            ("Change Avatar", "change_avatar", "#1e293b", "#64748b"), ("Create Server", "create_server", "#1e293b", "#64748b"),
            ("Join Server (URL)", "join_server", "#172554", "#3b82f6"), ("Leave Server (ID)", "leave_server", "#450a0a", "#dc2626"),
            ("Send DM to ID", "send_dm", "#14532d", "#22c55e")
        ]

        for i, (text, cmd, fg, hover) in enumerate(btn_data):
            row, col = divmod(i, 3)
            ctk.CTkButton(f, text=text, fg_color=fg, hover_color=hover, command=lambda c=cmd: self.run_task(c)).grid(row=row+3, column=col, padx=3, pady=3, sticky="nsew")

        for i in range(3):
            f.grid_columnconfigure(i, weight=1)

    def setup_webhook_tab(self):
        f = ctk.CTkFrame(self.tab_webhook, fg_color="transparent")
        f.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(f, text="Webhook URL:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.wh_url_entry = ctk.CTkEntry(f, width=500)
        self.wh_url_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(f, text="Message Content:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.wh_msg_entry = ctk.CTkEntry(f, width=500)
        self.wh_msg_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(f, text="Username (Optional):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.wh_name_entry = ctk.CTkEntry(f, width=500)
        self.wh_name_entry.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkButton(f, text="Send Single Message", fg_color="#172554", hover_color="#3b82f6", command=self.send_webhook).grid(row=3, column=0, padx=3, pady=15, sticky="nsew")
        ctk.CTkButton(f, text="Spam Webhook (10x)", fg_color="#450a0a", hover_color="#dc2626", command=self.spam_webhook).grid(row=3, column=1, padx=3, pady=15, sticky="nsew")
        
        for i in range(2):
            f.grid_columnconfigure(i, weight=1)

    def setup_cloner_tab(self):
        f = ctk.CTkFrame(self.tab_cloner, fg_color="transparent")
        f.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(f, text="User Token (Account):", text_color="#f87171").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.clone_user_token = ctk.CTkEntry(f, width=450, show="*")
        self.clone_user_token.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(f, text="Source Server ID:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.clone_src_id = ctk.CTkEntry(f, width=450)
        self.clone_src_id.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(f, text="Destination Server ID:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.clone_dest_id = ctk.CTkEntry(f, width=450)
        self.clone_dest_id.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkButton(f, text="🚀 Start Cloning Server", fg_color="#7c3aed", hover_color="#6d28d9", height=40, command=self.start_clone_thread).grid(row=3, column=0, columnspan=2, padx=5, pady=20, sticky="nsew")
        
        f.grid_columnconfigure(1, weight=1)

    def setup_help_tab(self):
        help_text = """
NEXCORD TOOLS v1.0 BETA - GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎮 RPC TAB:
Does NOT need Bot Token. Needs Application Client ID.
• Images: You MUST upload images to "Rich Presence" -> "Art Assets" in Discord Developer Portal and use their names here (not URLs).
• Buttons: Add up to 2 clickable buttons with custom URLs.

💣 SERVER TAB:
Uses BOT TOKEN. Enter Server ID.
Nuke/Spam/Rename Channels & Roles.
Mass Kick/Ban/Nick. Lock/Unlock/Purge.

👤 ACCOUNT TAB:
Uses BOT TOKEN. Target ID/URL for actions.
Change Bot Username, Avatar.
Join/Leave Servers. Send DMs.

🔗 WEBHOOK TAB:
Does NOT need bot connection.
Enter Webhook URL, Message, and Username.
Send or Spam messages instantly.

🔄 CLONER TAB:
Uses USER TOKEN (Your personal account token, NOT bot).
• Source ID: The server you want to copy.
• Destination ID: Your empty server where it gets copied.
Clones Roles, Categories, Text & Voice Channels.
Copies HIDDEN channels too if your user token has access.

⚠️ NOTES:
• Enable 'Message Content Intent' and 'Server Members Intent' in Discord Developer Portal for Bot features.
• Cloning requires your User Token to have Admin/Manage permissions in BOTH servers.
• Self-botting/Cloning violates Discord ToS. Use at your own risk.
        """
        txt_box = ctk.CTkTextbox(self.tab_help, width=720, height=400, fg_color="#0f0f0f", text_color="#d4d4d4")
        txt_box.pack(padx=10, pady=10)
        txt_box.insert("1.0", help_text)
        txt_box.configure(state="disabled")

    def send_webhook(self):
        url = self.wh_url_entry.get()
        msg = self.wh_msg_entry.get()
        name = self.wh_name_entry.get()
        if not url or not msg:
            self.log("[❌] Webhook URL and Message are required.")
            return
        try:
            data = {"content": msg, "username": name if name else None}
            r = requests.post(url, json=data)
            if r.status_code == 204:
                self.log("[✅] Webhook message sent.")
            else:
                self.log(f"[❌] Webhook failed: {r.text}")
        except Exception as e:
            self.log(f"[❌] Error: {e}")

    def spam_webhook(self):
        url = self.wh_url_entry.get()
        msg = self.wh_msg_entry.get()
        name = self.wh_name_entry.get()
        if not url or not msg:
            self.log("[❌] Webhook URL and Message are required.")
            return
        def spam_thread():
            for i in range(10):
                try:
                    data = {"content": f"{msg} [{i}]", "username": name if name else None}
                    requests.post(url, json=data)
                    self.log(f"[✅] Webhook spam {i+1}/10 sent.")
                except: pass
            self.log("[✅] Webhook spam finished.")
        threading.Thread(target=spam_thread, daemon=True).start()

    def start_clone_thread(self):
        user_token = self.clone_user_token.get()
        src_id = self.clone_src_id.get()
        dest_id = self.clone_dest_id.get()
        if not user_token or not src_id or not dest_id:
            self.log("[❌] Cloner: Fill all fields (User Token, Source ID, Dest ID).")
            return
        self.log("[⏳] Cloner: Starting process...")
        threading.Thread(target=self.clone_logic, args=(user_token, src_id, dest_id), daemon=True).start()

    def clone_logic(self, token, src_id, dest_id):
        headers = {"authorization": f"User {token}", "content-type": "application/json"}
        base_url = "https://discord.com/api/v10"

        try:
            r_roles = requests.get(f"{base_url}/guilds/{src_id}/roles", headers=headers)
            if r_roles.status_code != 200:
                self.log(f"[❌] Cloner: Cannot fetch roles. Check token/permissions. ({r_roles.status_code})")
                return
            src_roles = r_roles.json()

            self.log("[🔄] Cloner: Creating roles...")
            role_map = {}
            for role in reversed(src_roles):
                if role['name'] == '@everyone':
                    continue
                payload = {
                    "name": role['name'], "color": role['color'], "hoist": role['hoist'],
                    "icon": role.get('icon'), "unicode_emoji": role.get('unicode_emoji'),
                    "position": role['position'], "mentionable": role['mentionable'],
                    "permissions": str(role['permissions'])
                }
                r_create = requests.post(f"{base_url}/guilds/{dest_id}/roles", headers=headers, json=payload)
                if r_create.status_code == 200:
                    role_map[role['id']] = r_create.json()['id']
            
            self.log(f"[✅] Cloner: {len(role_map)} roles created.")

            r_channels = requests.get(f"{base_url}/guilds/{src_id}/channels", headers=headers)
            if r_channels.status_code != 200:
                self.log("[❌] Cloner: Cannot fetch channels.")
                return
            src_channels = r_channels.json()

            cats = [c for c in src_channels if c['type'] == 4]
            texts = [c for c in src_channels if c['type'] == 0]
            voices = [c for c in src_channels if c['type'] == 2]

            def fix_overwrites(overwrites):
                new_ow = []
                for ow in overwrites:
                    new_ow.append({
                        "id": role_map.get(ow['id'], ow['id']),
                        "type": ow['type'],
                        "allow": str(ow['allow']),
                        "deny": str(ow['deny'])
                    })
                return new_ow

            self.log("[🔄] Cloner: Creating categories...")
            chan_map = {}
            for cat in cats:
                payload = {
                    "name": cat['name'], "type": 4, "position": cat['position'],
                    "permission_overwrites": fix_overwrites(cat.get('permission_overwrites', []))
                }
                r_c = requests.post(f"{base_url}/guilds/{dest_id}/channels", headers=headers, json=payload)
                if r_c.status_code == 200:
                    chan_map[cat['id']] = r_c.json()['id']

            self.log("[🔄] Cloner: Creating text & voice channels...")
            count = 0
            for ch in texts + voices:
                payload = {
                    "name": ch['name'], "type": ch['type'], "position": ch['position'],
                    "parent_id": chan_map.get(ch.get('parent_id')),
                    "permission_overwrites": fix_overwrites(ch.get('permission_overwrites', [])),
                    "nsfw": ch.get('nsfw', False),
                    "rate_limit_per_user": ch.get('rate_limit_per_user', 0),
                    "bitrate": ch.get('bitrate', 64000),
                    "user_limit": ch.get('user_limit', 0)
                }
                r_c = requests.post(f"{base_url}/guilds/{dest_id}/channels", headers=headers, json=payload)
                if r_c.status_code == 200:
                    count += 1
            
            self.log(f"[✅] Cloner: Finished! {count} channels cloned.")

        except Exception as e:
            self.log(f"[❌] Cloner Error: {str(e)}")

    async def execute_task(self, task, *args):
        try:
            if task == "bot_info":
                self.log(f"[✅] Name: {self.bot.user.name} | ID: {self.bot.user.id} | Avatar: {self.bot.user.avatar.url if self.bot.user.avatar else 'None'}")

            elif task == "change_uname":
                new_name = self.username_entry.get()
                if new_name:
                    await self.bot.user.edit(username=new_name)
                    self.log(f"[✅] Username changed to {new_name}")

            elif task == "change_avatar":
                url = self.avatar_entry.get()
                if url:
                    r = requests.get(url)
                    await self.bot.user.edit(avatar=r.content)
                    self.log("[✅] Avatar changed.")

            elif task == "create_server":
                guild = await self.bot.create_guild(name="Nexcord Server")
                self.log(f"[✅] Created server: {guild.name} | ID: {guild.id}")

            elif task == "join_server":
                invite = self.target_entry.get()
                if invite:
                    await self.bot.join_invite(invite)
                    self.log("[✅] Joined server.")

            elif task == "leave_server":
                gid = int(self.target_entry.get())
                guild = self.bot.get_guild(gid)
                if guild:
                    await guild.leave()
                    self.log(f"[✅] Left server: {guild.name}")

            elif task == "send_dm":
                uid = int(self.target_entry.get())
                user = await self.bot.fetch_user(uid)
                dm = await user.create_dm()
                await dm.send("Hello from Nexcord Tools")
                self.log(f"[✅] DM sent to {user.name}")

            elif task in ["nuke_ch", "spam_ch", "rename_ch", "nuke_rl", "spam_rl", "nuke_emoji", "kick", "ban", "nick", "lock", "unlock", "purge", "sname"]:
                gid = int(self.guild_entry.get())
                guild = self.bot.get_guild(gid)
                if not guild:
                    self.log("[❌] Invalid Server ID or Bot is not in it.")
                    return

                if task == "nuke_ch":
                    for ch in guild.channels:
                        try: await ch.delete()
                        except: pass
                    self.log("[✅] Channels nuked.")

                elif task == "spam_ch":
                    for i in range(10):
                        try: await guild.create_text_channel(f"nexcord-{i}")
                        except: pass
                    self.log("[✅] 10 Channels created.")

                elif task == "rename_ch":
                    for ch in guild.text_channels:
                        try: await ch.edit(name="Nexcord On Top")
                        except: pass
                    self.log("[✅] Channels renamed.")

                elif task == "nuke_rl":
                    for rl in guild.roles:
                        if rl != guild.default_role:
                            try: await rl.delete()
                            except: pass
                    self.log("[✅] Roles nuked.")

                elif task == "spam_rl":
                    for i in range(10):
                        try: await guild.create_role(name=f"Nexcord-{i}")
                        except: pass
                    self.log("[✅] 10 Roles created.")

                elif task == "nuke_emoji":
                    for em in guild.emojis:
                        try: await em.delete()
                        except: pass
                    self.log("[✅] Emojis deleted.")

                elif task == "kick":
                    for m in guild.members:
                        if not m.bot:
                            try: await m.kick(); self.log(f"[✅] Kicked {m.name}")
                            except: pass
                            await asyncio.sleep(1)

                elif task == "ban":
                    for m in guild.members:
                        if not m.bot:
                            try: await m.ban(); self.log(f"[✅] Banned {m.name}")
                            except: pass
                            await asyncio.sleep(1)

                elif task == "nick":
                    for m in guild.members:
                        if not m.bot:
                            try: await m.edit(nick="Nexcord")
                            except: pass
                    self.log("[✅] Nicknames changed.")

                elif task == "lock":
                    for ch in guild.text_channels:
                        try: await ch.set_permissions(guild.default_role, send_messages=False)
                        except: pass
                    self.log("[✅] Server locked.")

                elif task == "unlock":
                    for ch in guild.text_channels:
                        try: await ch.set_permissions(guild.default_role, send_messages=True)
                        except: pass
                    self.log("[✅] Server unlocked.")

                elif task == "purge":
                    for ch in guild.text_channels:
                        try: await ch.purge(limit=100); self.log(f"[✅] Purged {ch.name}"); break
                        except: pass

                elif task == "sname":
                    await guild.edit(name="Nexcord Was Here")
                    self.log("[✅] Server name changed.")

        except Exception as e:
            self.log(f"[❌] Error: {str(e)}")

if __name__ == "__main__":
    app = NexcordApp()
    app.mainloop()