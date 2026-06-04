[app]
title = Aplex
package.name = aplexapp
package.domain = org.tanmoy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# 1. Hard lock the programming environment
requirements = python3==3.11.1,kivy,speechrecognition,requests,setuptools

orientation = portrait
fullscreen = 1

# 2. Hard lock the Android SDK platform tools
android.api = 33
android.minapi = 24
android.ndk = 25b
android.ndk_api = 21

# 3. Security Permissions
android.permissions = INTERNET, RECORD_AUDIO
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
