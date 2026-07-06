[app]

# (string) Title of your application
title = أغاني مريم أمو

# (string) Package name
package.name = amosongs

# (string) Package domain (needed for android packaging)
package.domain = org.nahdi

# (string) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,kv,png,jpg,jpeg,ttf,mp3,json

# (list) List of exclusions using pattern matching
source.exclude_patterns = license, README.md, *.pyc, **/test/**, **/tests/**, **/unittest/**

# (string) Application version
version = 1.0

# (string) Supported orientations
orientation = portrait

# (boolean) High reception screen or not
fullscreen = 0

# (int) Target Android API
android.api = 34

# (int) Minimum API your APK will support
android.minapi = 23

# (string) Android NDK version to use
android.ndk = 25b

# (list) Application requirements
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,arabic-reshaper,python-bidi,pyjnius

# (list) Supported architectures
android.archs = arm64-v8a, armeabi-v7a

# (list) Permissions
android.permissions = INTERNET, WAKE_LOCK

# (bool) Accept SDK license
android.accept_sdk_license = True

# (int) Log level (1 = error/warning only, 2 = stdout/stderr with info)
log_level = 1

# (int) Warn if buildozer is run as root
warn_on_root = 1


[buildozer]

# (int) Log level (1 = error/warning only, 2 = stdout/stderr with info)
log_level = 1

# (int) Warn if buildozer is run as root
warn_on_root = 1
