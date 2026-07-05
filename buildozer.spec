[app]

title = Amo Songs
package.name = amosongs
package.domain = org.amosongs

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,ttf,mp3

version = 1.0

requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,arabic-reshaper,python-bidi,pyjnius

orientation = portrait
fullscreen = 0

icon.filename = icon.png
presplash.filename = default_poster.png

android.permissions = INTERNET

android.api = 33
android.minapi = 23
android.ndk = 25b

android.archs = arm64-v8a,armeabi-v7a

android.accept_sdk_license = True

android.enable_androidx = True

log_level = 2

warn_on_root = 0
