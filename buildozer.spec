[app]
title = CachyVault Mobile
package.name = cachyvault
package.domain = org.philox
source.dir = .
source.include_exts = py,png,jpg,json
version = 1.1

# ⛓️ DEPENDENCY HOOKS: Force the mobile processor to download your cryptographic modules
requirements = python3,kivy,cryptography,openssl

orientation = portrait
fullscreen = 1
android.archs = armeabi-v7a, arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
