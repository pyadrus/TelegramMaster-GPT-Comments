# TelegramMaster-GPT-Comments 🚀

![alt text](doc/images/TelegramMaster_Commentator.png "TelegramMaster_Commentator")

**TelegramMaster-GPT-Comments** — bu Telegram kanallari, guruhlari va akkauntlari bilan ishlashni avtomatlashtirish
uchun kuchli vosita.  
Bot sizga kanallarni boshqarish, postlarga izoh qoldirish, profilni o‘zgartirish hamda Flet asosidagi qulay interfeys
orqali boshqa ko‘plab ishlarni bajarishga yordam beradi.

## Hujjatlar

[Hujjatlar](doc/doc.md)

## 🌟 Mening boshqa loyihalarim

Men Telegram uchun vositalar ishlab chiqishda faol rivojlanmoqdaman. Sizni qiziqtirishi mumkin bo‘lgan boshqa
loyihalarim:

**TelegramMaster 2.0**

**TelegramMaster 2.0** — bu Telegram bilan ishlash uchun ilg‘or vosita.

📨 Dastur quyidagi imkoniyatlarni taklif etadi:

* Akkauntlarni boshqarish.
* Foydalanuvchilar bilan muloqot qilish.
* Oddiy jarayonlarni avtomatlashtirish.

Ko‘proq bilish uchun havolaga o‘ting:  
👉 TelegramMaster 2.0 (https://github.com/pyadrus/TelegramMaster-2.0)

Shuningdek:  
👉 TelegramMaster-Search-GPT (https://github.com/pyadrus/TelegramMaster-Search-GPT)

## Imkoniyatlar

- **Kanallar ro‘yxatini olish**: Akkauntni skanerlab, kanallar haqida ma’lumot to‘playdi.
- **Izoh yuborish**: Belgilangan kanallarga avtomatik tarzda izoh yuboradi.
- **Profilni boshqarish**: Telegram akkaunt profilidagi ism va tavsifni o‘zgartirish imkonini beradi.
- **Kanallarga obuna bo‘lish**: Belgilangan kanallarga ommaviy tarzda obuna bo‘lishni osonlashtiradi.
- **Kanallar ro‘yxatini shakllantirish**: Kanallar ro‘yxatini SQLite bazasida saqlaydi.

## Asosiy xususiyatlar

- Tkinter yordamida qulay grafik interfeys.
- Loguru orqali barcha harakatlarni loglash.
- SQLite bazasidan foydalanib ma’lumotlarni saqlash.
- Config fayli orqali oson sozlash.
- Zamonaviy UX ni taqlid qiluvchi interfeys yo‘nalishlari.

## O‘rnatish

1. Repozitoriyani klonlang:
   ```bash
   git clone https://github.com/pyadrus/TelegramMaster_Commentator.git
   cd TelegramMaster_Commentator

```

## Kerakli kutubxonalarni o‘rnating:
```bash
pip install -r requirements.txt
```

## Konfiguratsiyani sozlash:

Telegram API ma’lumotlarini ko‘rsatish uchun `config/config.ini` faylini tahrir qiling.
Keyin loyiha quyidagicha ishga tushiriladi:

```bash
python main.py
```

## Interfeysdagi asosiy funksiyalar:

- Harakatlarni ishga tushirish tugmalari.
- Parametrlarni sozlash va muallif haqida ma’lumot ko‘rish menyusi.

## Talablar

- Python 3.8 yoki undan yuqori versiya.
- `requirements.txt` dagi kutubxonalar.

## Loglash

Barcha harakatlar `log/log.log` faylida saqlanadi. Fayl hajmi 1 MB dan oshsa, loglar avtomatik arxivlanadi.

## Hissa qo‘shish

Agar sizda g‘oyalar bo‘lsa yoki yaxshilanishlarni kiritmoqchi bo‘lsangiz, Pull Request yarating yoki Issues orqali
murojaat qiling.

## Litsenziya

Ushbu loyiha GNU GENERAL PUBLIC LICENSE ostida tarqatiladi.

## Aloqa

Savollar yoki takliflar bo‘lsa, muallif bilan bog‘laning:

Telegram: https://t.me/PyAdminRU
