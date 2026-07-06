[app]
title = Nader Khadr App
package.name = naderkhadrapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,mp3

# 🛠️ استبعاد ملفات اللغات غير الضرورية لتسريع البناء
source.exclude_patterns = lib/python3.11/encodings/iso*, lib/python3.11/encodings/cp12*, lib/python3.11/encodings/euc*, tests/*, test/*

version = 1.1
# 🛠️ ترتيب المتطلبات الصحيح
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,arabic-reshaper,python-bidi,pyjnius

orientation = portrait
fullscreen = 0

# Android specific
# 🛠️ تحديث لـ 34 ليتوافق مع متطلبات جوجل بلاي الحديثة ويصلح مسارات الـ SDK تلقائياً
android.api = 34
android.minapi = 24
# 🛠️ حل مشكلة الـ NDK (تحديد الحد الأدنى المتوافق)
android.ndk_api = 25
android.private_storage = True
p4a.bootstrap = sdl2
p4a.branch = master
# 🛠️ منع تجميع ملفات الاختبارات
android.no_test_compile = 1

[buildozer]
log_level = 2
warn_on_root = 1
