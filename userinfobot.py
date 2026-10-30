import datetime
from telethon import TelegramClient, events
from telethon.tl.functions.contacts import ResolvePhoneRequest
from telethon.tl.functions.users import GetFullUserRequest

API_ID = 1234567  # Replace with your integer API ID, e.g. 1234567
API_HASH = "your_api_hash_here"  # Replace with your API hash string

client = TelegramClient("lookup_session", API_ID, API_HASH)


@client.on(events.NewMessage(pattern=r"^/lookup\s+(\+\d+)"))
async def lookup_user(event):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 1. Capture sender details
    sender = await event.get_sender()
    sender_id = sender.id if sender else "Unknown"
    sender_name = getattr(sender, "first_name", "Unknown")
    if getattr(sender, "last_name", None):
        sender_name += f" {sender.last_name}"
        
    raw_command = event.raw_text

    # 2. Log incoming command details
    incoming_log = (
        f"[{timestamp}] [COMMAND RECEIVED]\n"
        f"  • Sender Name: {sender_name}\n"
        f"  • Sender Peer ID: {sender_id}\n"
        f"  • Message Sent: {raw_command}\n"
    )
    print(incoming_log.strip())
    with open("bot_activity.log", "a", encoding="utf-8") as f:
        f.write(incoming_log + "\n")

    phone_number = event.pattern_match.group(1).strip()

    try:
        # 3. Resolve phone number to get target user entity
        result = await client(ResolvePhoneRequest(phone=phone_number))
        user = result.users[0]
        
        # 4. Fetch full user profile for bio
        full_user_info = await client(GetFullUserRequest(user))
        
        bio = "No bio available"
        if hasattr(full_user_info, "full_user") and full_user_info.full_user:
            bio = full_user_info.full_user.about or "No bio available"
        elif hasattr(full_user_info, "about"):
            bio = full_user_info.about or "No bio available"

        first_name = user.first_name or "Not Provided"
        last_name = user.last_name or ""
        target_name = f"{first_name} {last_name}".strip()
        username = f"@{user.username}" if user.username else "None"

        # 5. Format response for Telegram chat (Directly returns user info)
        response = (
            f"✅ **User Found Successfully:**\n\n"
            f"• **Peer ID (User ID):** `{user.id}`\n"
            f"• **Name:** {target_name}\n"
            f"• **Username:** {username}\n"
            f"• **Bio:** {bio}\n"
            f"• **Phone Number:** {phone_number}"
        )
        await event.respond(response)

        # 6. Log successful discovery details
        success_log = (
            f"[{timestamp}] [SUCCESS] Lookup completed for {phone_number}\n"
            f"  • Target Peer ID: {user.id}\n"
            f"  • Target Name: {target_name}\n"
            f"  • Target Username: {username}\n"
            f"  • Target Bio: {bio}\n"
            f"  • Phone Number: {phone_number}\n"
            f"{'='*50}\n"
        )
        print(success_log.strip())
        with open("bot_activity.log", "a", encoding="utf-8") as f:
            f.write(success_log)

    except Exception as e:
        error_msg = (
            f"[{timestamp}] [ERROR] Lookup failed for {phone_number}: {str(e)}\n"
            f"{'='*50}\n"
        )
        print(error_msg.strip())
        with open("bot_activity.log", "a", encoding="utf-8") as f:
            f.write(error_msg)
        await event.respond(f"❌ Error occurred or no account found: `{str(e)}`")


with client:
    print("Userbot is running and listening for commands...")
    client.run_until_disconnected()
