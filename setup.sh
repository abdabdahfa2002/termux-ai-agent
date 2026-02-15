#!/bin/bash

echo "------------------------------------------"
echo "   Termux AI Agent - Smart Installation   "
echo "------------------------------------------"

# وظيفة للتعامل مع قفل الحزم
fix_lock() {
    echo "[!] Checking for package manager locks..."
    if [ -f /data/data/com.termux/files/usr/var/lib/dpkg/lock-frontend ]; then
        echo "[!] Found lock. Attempting to clear safely..."
        # محاولة قتل العمليات العالقة التي تستخدم apt أو dpkg
        fuser -k /data/data/com.termux/files/usr/var/lib/dpkg/lock-frontend > /dev/null 2>&1
        rm -f /data/data/com.termux/files/usr/var/lib/dpkg/lock-frontend
    fi
}

# تنفيذ الإصلاح قبل البدء
fix_lock

# تحديث الحزم مع تخطي التحديثات الكبيرة إذا كانت تسبب قفلاً
echo "[*] Updating package lists..."
pkg update -y || { echo "[!] Update failed, trying to fix lock and retry..."; fix_lock; pkg update -y; }

# تثبيت المتطلبات الأساسية
echo "[*] Installing dependencies (Python, Termux-API)..."
pkg install python ncurses-utils termux-api -y

# تثبيت مكتبات بايثون
echo "[*] Installing Python libraries..."
pip install --upgrade pip
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
if ! grep -q "alias termux-ai" ~/.bashrc; then
    echo "alias termux-ai='python $(pwd)/agent.py'" >> ~/.bashrc
fi

echo "------------------------------------------"
echo "   Installation Complete!                 "
echo "   To start, run: python agent.py         "
echo "   Or restart Termux and type: termux-ai  "
echo "------------------------------------------"
