import os
import json
import hashlib
import base64
import re
from datetime import datetime, timedelta
import getpass
import asyncio
import uuid
import time
from cryptography.fernet import Fernet
from telethon import TelegramClient, events

# ==================== CİHAZ BAZLI LİSANS SİSTEMİ ====================
class DeviceLicenseSystem:
    def __init__(self):
        self.license_file = ".tg_license.dat"
        self.device_id_file = ".tg_device.id"
        self.master_key = self._generate_master_key()
        self.device_id = self._get_device_id()

        # 50 adet 30 günlük lisans
        self.monthly_keys = {
            "TGA-7B9F-KL2M-4PZQ": 30, "TGA-N6DH-8R3S-1XCV": 30, "TGA-5T8Y-9W4U-7BVF": 30,
            "TGA-Q2WE-5R7T-9Y8U": 30, "TGA-1H4J-7K9L-0P3M": 30, "TGA-X5D8-F2G7-H1J3": 30,
            "TGA-9K8L-2M4N-6B5V": 30, "TGA-3Q9P-1L6K-8M2N": 30, "TGA-7R4T-9Y2U-1I3O": 30,
            "TGA-8F3D-5S2A-9Q7W": 30, "TGA-P4Z7-L2K9-M1N6": 30, "TGA-V9B3-C5X7-D8F2": 30,
            "TGA-J6H8-G4K2-L9P7": 30, "TGA-W3E5-R7T1-Y9U2": 30, "TGA-S4D6-F8G2-H1J3": 30,
            "TGA-M2N4-B6V8-C9X1": 30, "TGA-K5L7-P3O9-I8U2": 30, "TGA-Z1X3-C5V7-B9N2": 30,
            "TGA-E4R6-T8Y1-U3I5": 30, "TGA-D2F5-S8A9-Q7W3": 30, "TGA-G7H9-J2K4-L6P8": 30,
            "TGA-L3O5-I9U2-Y7T1": 30, "TGA-U1Y3-T5R7-E9W4": 30, "TGA-B4N6-M8P2-K1L9": 30,
            "TGA-C5V7-B9N2-M1L4": 30, "TGA-H8J2-K4L6-P9O3": 30, "TGA-Y3U5-I7O9-P2L6": 30,
            "TGA-R6T8-Y1U3-I5O7": 30, "TGA-F9G2-H4J6-K8L3": 30, "TGA-A7S9-D3F5-G8H2": 30,
            "TGA-O1P3-L5K7-J9H4": 30, "TGA-I6U8-Y2T4-R5E7": 30, "TGA-Q9W3-E5R7-T2Y4": 30,
            "TGA-V2B4-N6M8-P1L3": 30, "TGA-C8X1-Z3V5-B7N9": 30, "TGA-D1F3-S5A7-Q9W2": 30,
            "TGA-G4H6-J8K2-L1P5": 30, "TGA-M7P9-K3L5-O1I8": 30, "TGA-T4Y6-U8I2-O3P7": 30,
            "TGA-N9B1-V5C7-X2Z4": 30, "TGA-E3R5-T7Y1-U9I4": 30, "TGA-S6D8-F2G4-H7J9": 30,
            "TGA-W5Q7-E3R9-T1Y6": 30, "TGA-K2L4-J6H8-G9F1": 30, "TGA-O7P9-I3U5-Y8T2": 30,
            "TGA-U4I6-O8P2-L3K9": 30, "TGA-B2V4-N6M8-C1X3": 30, "TGA-Z5X7-C9V2-B4N6": 30,
            "TGA-F1G3-H5J7-K9L2": 30
        }

        # 50 adet süresiz lisans
        self.unlimited_keys = {
            "TGS-7B9F-KL2M-4PZQ": 9999, "TGS-N6DH-8R3S-1XCV": 9999, "TGS-5T8Y-9W4U-7BVF": 9999,
            "TGS-Q2WE-5R7T-9Y8U": 9999, "TGS-1H4J-7K9L-0P3M": 9999, "TGS-X5D8-F2G7-H1J3": 9999,
            "TGS-9K8L-2M4N-6B5V": 9999, "TGS-3Q9P-1L6K-8M2N": 9999, "TGS-7R4T-9Y2U-1I3O": 9999,
            "TGS-8F3D-5S2A-9Q7W": 9999, "TGS-P4Z7-L2K9-M1N6": 9999, "TGS-V9B3-C5X7-D8F2": 9999,
            "TGS-J6H8-G4K2-L9P7": 9999, "TGS-W3E5-R7T1-Y9U2": 9999, "TGS-S4D6-F8G2-H1J3": 9999,
            "TGS-M2N4-B6V8-C9X1": 9999, "TGS-K5L7-P3O9-I8U2": 9999, "TGS-Z1X3-C5V7-B9N2": 9999,
            "TGS-E4R6-T8Y1-U3I5": 9999, "TGS-D2F5-S8A9-Q7W3": 9999, "TGS-G7H9-J2K4-L6P8": 9999,
            "TGS-L3O5-I9U2-Y7T1": 9999, "TGS-U1Y3-T5R7-E9W4": 9999, "TGS-B4N6-M8P2-K1L9": 9999,
            "TGS-C5V7-B9N2-M1L4": 9999, "TGS-H8J2-K4L6-P9O3": 9999, "TGS-Y3U5-I7O9-P2L6": 9999,
            "TGS-R6T8-Y1U3-I5O7": 9999, "TGS-F9G2-H4J6-K8L3": 9999, "TGS-A7S9-D3F5-G8H2": 9999,
            "TGS-O1P3-L5K7-J9H4": 9999, "TGS-I6U8-Y2T4-R5E7": 9999, "TGS-Q9W3-E5R7-T2Y4": 9999,
            "TGS-V2B4-N6M8-P1L3": 9999, "TGS-C8X1-Z3V5-B7N9": 9999, "TGS-D1F3-S5A7-Q9W2": 9999,
            "TGS-G4H6-J8K2-L1P5": 9999, "TGS-M7P9-K3L5-O1I8": 9999, "TGS-T4Y6-U8I2-O3P7": 9999,
            "TGS-N9B1-V5C7-X2Z4": 9999, "TGS-E3R5-T7Y1-U9I4": 9999, "TGS-S6D8-F2G4-H7J9": 9999,
            "TGS-W5Q7-E3R9-T1Y6": 9999, "TGS-K2L4-J6H8-G9F1": 9999, "TGS-O7P9-I3U5-Y8T2": 9999,
            "TGS-U4I6-O8P2-L3K9": 9999, "TGS-B2V4-N6M8-C1X3": 9999, "TGS-Z5X7-C9V2-B4N6": 9999,
            "TGS-F1G3-H5J7-K9L2": 9999
        }

        self.all_keys = {**self.monthly_keys, **self.unlimited_keys}

    def _generate_master_key(self):
        return hashlib.sha256(b"telegram-ultimate-secure-key-2023").digest()

    def _get_device_id(self):
        """Cihaza özgü benzersiz ID oluşturur"""
        if os.path.exists(self.device_id_file):
            with open(self.device_id_file, 'r') as f:
                return f.read()

        device_id = str(uuid.uuid4())
        with open(self.device_id_file, 'w') as f:
            f.write(device_id)
        return device_id

    def _encrypt_data(self, data: dict) -> str:
        key = base64.b64encode(self.master_key[:32])
        return Fernet(key).encrypt(json.dumps(data).encode()).decode()

    def _decrypt_data(self, token: str) -> dict:
        key = base64.b64encode(self.master_key[:32])
        return json.loads(Fernet(key).decrypt(token.encode()).decode())

    def check_license(self):
        if not os.path.exists(self.license_file):
            return False

        try:
            with open(self.license_file, 'r') as f:
                data = self._decrypt_data(f.read())

            # 1. Cihaz ID kontrolü
            if data.get('device_id') != self.device_id:
                print("❌ Lisans başka cihaz için kayıtlı!")
                return False

            # 2. Lisans anahtarı geçerlilik kontrolü
            if data['license_key'] not in self.all_keys:
                print("❌ Geçersiz lisans anahtarı!")
                return False

            # 3. Süre kontrolü (30 günlük lisanslar için)
            if self.all_keys[data['license_key']] != 9999:
                expire_date = datetime.strptime(data['expire_date'], '%Y-%m-%d')
                if datetime.now() > expire_date:
                    print("❌ Lisans süresi dolmuş!")
                    os.remove(self.license_file)
                    return False

            return True

        except Exception as e:
            print(f"Lisans kontrol hatası: {str(e)}")
            return False

    def activate_license(self):
        print("\n" + "="*50)
        print(" TELEGRAM LİSANS AKTİVASYONU ".center(50, '#'))
        print("="*50)

        key = getpass.getpass("Geçerli lisans anahtarı giriniz: ").strip().upper()

        if key not in self.all_keys:
            print("\n❌ HATA: Geçersiz lisans anahtarı!")
            print("Lütfen doğru bir lisans anahtarı giriniz.")
            return False

        license_days = self.all_keys[key]

        if license_days == 9999:  # Süresiz lisans
            data = {
                'license_key': key,
                'type': "SONSUZ",
                'device_id': self.device_id,
                'activate_date': datetime.now().strftime('%Y-%m-%d'),
                'expire_date': "SONSUZ"
            }
            print("\n✅ Süresiz lisans aktif edildi!")
            print("Bu lisans SADECE bu cihazda çalışacaktır.")
        else:  # 30 günlük lisans
            expire_date = datetime.now() + timedelta(days=license_days)
            data = {
                'license_key': key,
                'type': "30GUN",
                'device_id': self.device_id,
                'activate_date': datetime.now().strftime('%Y-%m-%d'),
                'expire_date': expire_date.strftime('%Y-%m-%d')
            }
            print(f"\n✅ {license_days} günlük lisans aktif edildi!")
            print(f"Son kullanma tarihi: {expire_date.strftime('%d/%m/%Y')}")

        with open(self.license_file, 'w') as f:
            f.write(self._encrypt_data(data))

        return True

# ==================== METİN FİLTRELEME FONKSİYONU ====================
def clean_text(text):
    """Metinden sadece istenmeyen içerikleri temizler, boşluklara dokunmaz"""
    if not text:
        return ""

    pattern = r'(@\w+|https?://\S+|t\.me/\S+)'
    return re.sub(pattern, '', text)

# ==================== LİSANS KONTROLÜ ====================
license = DeviceLicenseSystem()
if not license.check_license():
    print("\n" + " LİSANS GEREKLİDİR ".center(50, '='))
    print("Lütfen geçerli bir lisans anahtarı girin")
    print("30 günlük (TGA-...) veya süresiz (TGS-...) lisans anahtarı kullanabilirsiniz")

    if not license.activate_license():
        exit("\n❌ Lisanssız kullanım mümkün değildir. Program sonlandırılıyor...")
    print("\n" + "="*50 + "\n")

# ==================== TELEGRAM BOT AYARLARI ====================
config_file = 'tg_config.json'

if not os.path.exists(config_file):
    print("\nTelegram Ayarları:")
    api_id = int(input("API ID: ").strip())
    api_hash = input("API HASH: ").strip()
    source_channel = input("Kaynak kanal (@ olmadan): ").strip()
    target_channel = input("Hedef kanal (@ olmadan): ").strip()

    with open(config_file, 'w') as f:
        json.dump({
            'api_id': api_id,
            'api_hash': api_hash,
            'source_channel': source_channel,
            'target_channel': target_channel
        }, f)
else:
    with open(config_file, 'r') as f:
        config = json.load(f)
        api_id = config['api_id']
        api_hash = config['api_hash']
        source_channel = config['source_channel']
        target_channel = config['target_channel']

client = TelegramClient('tg_user_session', api_id, api_hash)
sent_message_ids = {}
processed_albums = set()

# ==================== MESAJ GÖNDERİM KONTROLÜ ====================
last_message_time = 0  # Son mesajın gönderildiği zaman
MESSAGE_DELAY = 900    # 15 dakika (saniye cinsinden)

# ==================== LOG SİSTEMİ ====================
def log(event_type, message):
    emojis = {
        "new": "🆕", "sent": "✅", "edit": "✏️",
        "delete": "🗑️", "error": "❌", "info": "ℹ️",
        "license": "🔐", "warning": "⚠️", "wait": "⏳"
    }
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {emojis.get(event_type, '')} {message[:100]}"
    print(log_msg)
    with open("telegram_bot.log", "a", encoding="utf-8") as f:
        f.write(log_msg + "\n")

# ==================== BOT FONKSİYONLARI ====================
async def resolve_reply(message):
    if message.is_reply:
        try:
            replied = await message.get_reply_message()
            if replied and replied.id in sent_message_ids:
                return sent_message_ids[replied.id]
        except Exception as e:
            log("error", f"Alıntı hatası: {e}")
    return None

@client.on(events.NewMessage(chats=source_channel))
async def handle_new_message(event):
    global last_message_time

    try:
        current_time = time.time()
        time_since_last = current_time - last_message_time

        # 15 dakika dolmadıysa bekle
        if time_since_last < MESSAGE_DELAY:
            wait_time = int(MESSAGE_DELAY - time_since_last)
            log("wait", f"Beklemede: Sonraki mesaj için {wait_time//60} dakika {wait_time%60} saniye kaldı")
            await asyncio.sleep(wait_time)

        msg = event.message
        log("new", msg.text or "[Medya]")

        # Albüm mesajı kontrolü
        if msg.grouped_id:
            if msg.grouped_id in processed_albums:
                return

            await asyncio.sleep(1.5)
            recent = await client.get_messages(msg.chat_id, limit=20)
            album = [m for m in recent if m.grouped_id == msg.grouped_id]
            album.sort(key=lambda m: m.id)

            if msg.id != album[0].id:  # Sadece albümün ilk mesajını işle
                return

            processed_albums.add(msg.grouped_id)

            # Tüm albüm mesajlarında reply kontrolü yap
            reply_to = None
            for m in album:
                current_reply = await resolve_reply(m)
                if current_reply:
                    reply_to = current_reply
                    break

            caption = clean_text(next((m.text for m in album if m.text), ""))
            media = []
            for m in album:
                if m.photo:
                    media.append(m.photo)
                elif m.video:
                    media.append(m.video)
                elif m.document:
                    media.append(m.document)

            if media:
                sent = await client.send_file(
                    target_channel,
                    media,
                    caption=caption,
                    reply_to=reply_to
                )
                # Tüm albüm mesajlarını kaydet
                if isinstance(sent, list):
                    for original, sent_msg in zip(album, sent):
                        sent_message_ids[original.id] = sent_msg.id
                else:
                    sent_message_ids[msg.id] = sent.id

                last_message_time = time.time()
                log("sent", f"Albüm gönderildi: {caption or '[Medya]'}")
            return

        # Normal mesajlar
        reply_to = await resolve_reply(msg)
        text = clean_text(msg.text or "")

        if msg.photo:
            sent = await client.send_file(
                target_channel,
                msg.photo,
                caption=text,
                reply_to=reply_to
            )
        elif msg.video:
            sent = await client.send_file(
                target_channel,
                msg.video,
                caption=text,
                reply_to=reply_to
            )
        elif msg.document:
            sent = await client.send_file(
                target_channel,
                msg.document,
                caption=text,
                reply_to=reply_to
            )
        elif text.strip():
            sent = await client.send_message(
                target_channel,
                text,
                reply_to=reply_to
            )
        else:
            log("info", "Boş mesaj gönderilmedi.")
            return

        sent_message_ids[msg.id] = sent.id
        last_message_time = time.time()
        log("sent", f"Mesaj gönderildi: {text[:50]}")

    except Exception as e:
        log("error", f"Mesaj hatası: {str(e)}")

@client.on(events.MessageEdited(chats=source_channel))
async def handle_edit(event):
    try:
        msg = event.message
        if msg.id not in sent_message_ids:
            return

        target_id = sent_message_ids[msg.id]
        text = clean_text(msg.text or "")

        if text.strip():
            await client.edit_message(target_channel, target_id, text)
            log("edit", f"Düzenlendi: {text[:50]}")

    except Exception as e:
        log("error", f"Düzenleme hatası: {str(e)}")

@client.on(events.MessageDeleted(chats=source_channel))
async def handle_delete(event):
    for msg_id in event.deleted_ids:
        if msg_id in sent_message_ids:
            try:
                await client.delete_messages(target_channel, sent_message_ids[msg_id])
                del sent_message_ids[msg_id]
                log("delete", f"Silindi: {msg_id}")
            except Exception as e:
                log("error", f"Silme hatası: {str(e)}")

# ==================== BOT BAŞLATMA ====================
async def start_bot():
    await client.start()

    # Lisans bilgilerini göster
    with open(license.license_file, 'r') as f:
        data = license._decrypt_data(f.read())
        if data['type'] == "SONSUZ":
            log("license", "SÜRESİZ LİSANS AKTİF - Bu cihaz için kayıtlı")
        else:
            days_left = (datetime.strptime(data['expire_date'], '%Y-%m-%d') - datetime.now()).days
            log("license", f"{days_left} GÜN KALAN LİSANS AKTİF")

    log("info", "🤖 Telegram Bot Başlatıldı")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        client.loop.run_until_complete(start_bot())
    except Exception as e:
        log("error", f"Bot başlatma hatası: {str(e)}")
        exit(1)
