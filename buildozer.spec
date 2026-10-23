[app]
title = MathX
package.name = mathx
package.domain = org.barmanzarei
source.dir = script
source.include_exts = py,png,jpg,kv,atlas,ttf
source.exclude_dirs = tests,__pycache__,.buildozer
version = 1.0.0
requirements = python3,kivy==2.3.1,mathzx
orientation = portrait
android.accept_sdk_license = True
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
