#!/bin/bash

echo "------------------------------------------"
echo "   Termux AI Agent - Installation Script   "
echo "------------------------------------------"

# تحديث الحزم
echo "[*] Updating packages..."
pkg update -y && pkg upgrade -y

# تثبيت المتطلبات الأساسية
echo "[*] Installing dependencies (Python, Termux-API)..."
pkg install python ncurses-utils termux-api -y

# إنشاء بيئة افتراضية (اختياري ولكن مفضل)
# python -m venv venv
# source venv/bin/activate

# تثبيت مكتبات بايثون
echo "[*] Installing Python libraries..."
pip install -r requirements.txt

# إنشاء ملف .env إذا لم يكن موجوداً
if [ ! -f .env ]; then
    echo "[!] .env file not found. Creating one..."
    echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
    echo "DEFAULT_MODEL=gemini-1.5-flash" >> .env
    echo "ADVANCED_MODEL=gemini-1.5-pro" >> .env
    echo "[+] Created .env. Please edit it and add your API Key."
fi

# جعل الوكيل قابلاً للتشغيل كأمر
echo "[*] Setting up shortcut..."
echo "alias termux-ai='python $(pwd)/agent.py'" >> ~/.bashrc
source ~/.bashrc

echo "------------------------------------------"
echo "   Installation Complete!                 "
echo "   To start, run: python agent.py         "
echo "   Or restart Termux and type: termux-ai  "
echo "------------------------------------------"
