[app]
title = Aplex
package.name = aplexapp
package.domain = org.tanmoy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# Fixed to use stable Python 3.11.1 to avoid the version 3.14 experimental crash!
requirements = python3==3.11.1,kivy,speechrecognition,requests,setuptools

orientation = portrait
fullscreen = 1

# System permission parameters for your AI mic features
android.permissions = INTERNET, RECORD_AUDIO
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
