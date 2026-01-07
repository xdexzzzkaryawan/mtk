#!/usr/bin/env python3
import logging
import subprocess
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from datetime import datetime

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token bot Anda
TOKEN = "8550068285:AAHepdxHY5Gz31CBMWkaXWFVEjg0PZ2mzuM"
ADMIN_ID = 7799092693  # Ganti dengan ID Telegram Anda

def run_command(cmd):
    """Jalankan command dan return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result. stdout or result.stderr
    except Exception as e:
        return f"Error: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk /start"""
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("🔞")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("📊 Status", callback_data='status'),
            InlineKeyboardButton("🔋 Battery", callback_data='battery')
        ],
        [
            InlineKeyboardButton("💾 RAM", callback_data='ram'),
            InlineKeyboardButton("💿 Storage", callback_data='storage')
        ],
        [
            InlineKeyboardButton("📡 Network", callback_data='network'),
            InlineKeyboardButton("⚙️ CPU", callback_data='cpu')
        ],
        [
            InlineKeyboardButton("📶 WiFi", callback_data='wifi_menu'),
            InlineKeyboardButton("🔥 Hotspot", callback_data='hotspot_menu')
        ],
        [
            InlineKeyboardButton("📷 Camera", callback_data='camera_menu'),
            InlineKeyboardButton("💡 Flashlight", callback_data='flashlight_menu')
        ],
        [
            InlineKeyboardButton("🔄 Reboot", callback_data='reboot_confirm')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🤖 *Bot Monitoring HP Termux*\n\n"
        "Pilih menu yang ingin Anda akses:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle pesan dari user lain"""
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("🔞")
        return

# ==================== WiFi Menu ====================
async def wifi_menu(update:  Update, context: ContextTypes. DEFAULT_TYPE):
    """Menu WiFi"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("📶 ON", callback_data='wifi_on'),
            InlineKeyboardButton("📵 OFF", callback_data='wifi_off')
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "WiFi Control:",
        reply_markup=reply_markup
    )

async def wifi_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Turn ON WiFi"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text("🐵 Loading...")
    
    run_command("svc wifi enable")
    
    await asyncio.sleep(2)
    
    keyboard = [
        [
            InlineKeyboardButton("🔙 Back", callback_data='wifi_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🐵 WiFi berhasil di-ON! ",
        reply_markup=reply_markup
    )

async def wifi_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Turn OFF WiFi"""
    query = update. callback_query
    await query. answer()
    
    await query.edit_message_text("🐵 Loading...")
    
    run_command("svc wifi disable")
    
    await asyncio.sleep(2)
    
    keyboard = [
        [
            InlineKeyboardButton("🔙 Back", callback_data='wifi_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "💣 WiFi berhasil di-OFF!",
        reply_markup=reply_markup
    )

# ==================== Hotspot Menu ====================
async def hotspot_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu Hotspot"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("📶 ON", callback_data='hotspot_on'),
            InlineKeyboardButton("📵 OFF", callback_data='hotspot_off')
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "🔥 Hotspot Control:",
        reply_markup=reply_markup
    )

async def hotspot_on(update: Update, context:  ContextTypes.DEFAULT_TYPE):
    """Turn ON Hotspot"""
    query = update.callback_query
    await query.answer()
    
    await query. edit_message_text("🐵 Loading...")
    
    # Turn on WiFi first
    run_command("svc wifi enable")
    await asyncio.sleep(1)
    
    # Turn on hotspot
    run_command("svc tethering enable")
    
    await asyncio.sleep(2)
    
    keyboard = [
        [
            InlineKeyboardButton("🔙 Back", callback_data='hotspot_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🐵 Hotspot berhasil di-ON!",
        reply_markup=reply_markup
    )

async def hotspot_off(update: Update, context:  ContextTypes.DEFAULT_TYPE):
    """Turn OFF Hotspot"""
    query = update.callback_query
    await query.answer()
    
    await query. edit_message_text("🐵 Loading...")
    
    # Turn off hotspot
    run_command("svc tethering disable")
    
    await asyncio.sleep(2)
    
    keyboard = [
        [
            InlineKeyboardButton("🔙 Back", callback_data='hotspot_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "💣 Hotspot berhasil di-OFF!",
        reply_markup=reply_markup
    )

# ==================== Camera Menu ====================
async def camera_menu(update:  Update, context: ContextTypes. DEFAULT_TYPE):
    """Menu Camera"""
    query = update. callback_query
    await query. answer()
    
    keyboard = [
        [
            InlineKeyboardButton("📷 Open Camera", callback_data='camera_open'),
            InlineKeyboardButton("🤳 Selfie", callback_data='camera_selfie')
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "📷 Camera Control:",
        reply_markup=reply_markup
    )

async def camera_open(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Open Camera"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text("🐵 Loading...")
    
    # Buka camera app
    run_command("am start -a android.intent.action.MAIN -n com.android.camera/com.android.camera.CameraActivity")
    
    await asyncio.sleep(1)
    
    keyboard = [
        [
            InlineKeyboardButton("🔙 Back", callback_data='camera_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "📷 Camera terbuka!",
        reply_markup=reply_markup
    )

async def camera_selfie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Open Selfie Camera"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text("🐵 Loading...")
    
    # Buka camera dengan facing front
    run_command("am start -a android.intent.action.MAIN -n com.android.camera/com.android.camera.CameraActivity --ei android.intent.extras.CAMERA_FACING 1")
    
    await asyncio.sleep(1)
    
    keyboard = [
        [
            InlineKeyboardButton("🔙 Back", callback_data='camera_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🤳 Selfie camera terbuka!",
        reply_markup=reply_markup
    )

# ==================== Flashlight Menu ====================
async def flashlight_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menu Flashlight"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("💡 ON", callback_data='flashlight_on'),
            InlineKeyboardButton("⚫ OFF", callback_data='flashlight_off')
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "💡 Flashlight Control:",
        reply_markup=reply_markup
    )

async def flashlight_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Turn ON Flashlight"""
    query = update. callback_query
    await query. answer()
    
    await query.edit_message_text("🐵 Loading...")
    
    # Nyalain lampu dengan berbagai method
    run_command("termux-torch on 2>/dev/null || am start -n com.android.torch/com.android.torch.MainActivity 2>/dev/null || am start -n com.example.flashlight/com.example. flashlight.MainActivity")
    
    await asyncio. sleep(1)
    
    keyboard = [
        [
            InlineKeyboardButton("🔙 Back", callback_data='flashlight_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "💡 Lampu HP berhasil di-ON!",
        reply_markup=reply_markup
    )

async def flashlight_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Turn OFF Flashlight"""
    query = update. callback_query
    await query. answer()
    
    await query.edit_message_text("🐵 Loading...")
    
    # Matiin lampu
    run_command("termux-torch off 2>/dev/null || am start -n com.android.torch/com. android.torch.MainActivity 2>/dev/null || pkill -f torch")
    
    await asyncio.sleep(1)
    
    keyboard = [
        [
            InlineKeyboardButton("🔙 Back", callback_data='flashlight_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "⚫ Lampu HP berhasil di-OFF!",
        reply_markup=reply_markup
    )

# ==================== Status Menu ====================
async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Status sistem keseluruhan"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("⏳ Loading...")
    
    output = "📊 *Status Sistem*\n\n"
    
    battery = run_command("dumpsys battery | grep level")
    output += f"🔋 Baterai: {battery. strip()}\n"
    
    ram = run_command("free -h | grep Mem")
    output += f"💾 RAM: {ram. strip()}\n\n"
    
    storage = run_command("df -h /storage/emulated/0 | tail -1")
    output += f"💿 Storage: {storage.strip()}\n\n"
    
    uptime = run_command("uptime -p")
    output += f"⏱️ Uptime: {uptime.strip()}\n"
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Refresh", callback_data='status'),
            InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        output,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def battery_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info detail baterai"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("⏳ Loading...")
    
    output = run_command("dumpsys battery")
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Refresh", callback_data='battery'),
            InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"```\n{output}\n```",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def ram_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info RAM"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("⏳ Loading...")
    
    output = run_command("free -h")
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Refresh", callback_data='ram'),
            InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"```\n{output}\n```",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def storage_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info Storage"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("⏳ Loading...")
    
    output = run_command("df -h")
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Refresh", callback_data='storage'),
            InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"```\n{output}\n```",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def network_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info Network"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("⏳ Loading...")
    
    output = run_command("ifconfig")
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Refresh", callback_data='network'),
            InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"```\n{output}\n```",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def cpu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info CPU"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("⏳ Loading...")
    
    output = run_command("top -n 1 | head -20")
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Refresh", callback_data='cpu'),
            InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"```\n{output}\n```",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ==================== Reboot ====================
async def reboot_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Konfirmasi Reboot"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Ya, Reboot", callback_data='reboot_yes'),
            InlineKeyboardButton("❌ Batal", callback_data='back_to_menu')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "⚠️ *Yakin ingin Reboot HP?*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def reboot_yes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reboot HP"""
    query = update.callback_query
    await query.answer()
    
    await query. edit_message_text("⏳ HP Rebooting dalam 5 detik...")
    run_command("sleep 5 && reboot")

# ==================== Back to Menu ====================
async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kembali ke menu utama"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("📊 Status", callback_data='status'),
            InlineKeyboardButton("🔋 Battery", callback_data='battery')
        ],
        [
            InlineKeyboardButton("💾 RAM", callback_data='ram'),
            InlineKeyboardButton("💿 Storage", callback_data='storage')
        ],
        [
            InlineKeyboardButton("📡 Network", callback_data='network'),
            InlineKeyboardButton("⚙️ CPU", callback_data='cpu')
        ],
        [
            InlineKeyboardButton("📶 WiFi", callback_data='wifi_menu'),
            InlineKeyboardButton("🔥 Hotspot", callback_data='hotspot_menu')
        ],
        [
            InlineKeyboardButton("📷 Camera", callback_data='camera_menu'),
            InlineKeyboardButton("💡 Flashlight", callback_data='flashlight_menu')
        ],
        [
            InlineKeyboardButton("🔄 Reboot", callback_data='reboot_confirm')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "🤖 *Bot Monitoring HP Termux*\n\n"
        "Pilih menu yang ingin Anda akses:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle semua button callback"""
    query = update.callback_query
    
    # Check if user is admin
    if query.from_user.id != ADMIN_ID:
        await query.answer("🔞", show_alert=False)
        return
    
    data = query.data
    
    handlers = {
        'status': status_handler,
        'battery':  battery_handler,
        'ram': ram_handler,
        'storage': storage_handler,
        'network': network_handler,
        'cpu': cpu_handler,
        'wifi_menu': wifi_menu,
        'wifi_on': wifi_on,
        'wifi_off': wifi_off,
        'hotspot_menu': hotspot_menu,
        'hotspot_on': hotspot_on,
        'hotspot_off': hotspot_off,
        'camera_menu': camera_menu,
        'camera_open': camera_open,
        'camera_selfie': camera_selfie,
        'flashlight_menu': flashlight_menu,
        'flashlight_on': flashlight_on,
        'flashlight_off': flashlight_off,
        'reboot_confirm': reboot_confirm,
        'reboot_yes':  reboot_yes,
        'back_to_menu': back_to_menu,
    }
    
    handler = handlers.get(data)
    if handler:
        await handler(update, context)
    else:
        await query.answer("Command tidak tersedia", show_alert=False)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle error"""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

def main():
    """Start bot"""
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(MessageHandler(filters. COMMAND, start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    print("🤖 Bot sedang berjalan...")
    application.run_polling()

if __name__ == '__main__':
    main()
