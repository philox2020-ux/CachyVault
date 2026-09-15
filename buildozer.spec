[app]
title = CachyVault Mobile
package.name = cachyvault
package.domain = org.philox
source.dir = .
source.include_exts = py,png,jpg,json
version = 1.1

# ⛓️ DEPENDENCY HOOKS: Include core mobile engines and encryption modules
requirements = python3,kivy,cryptography

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a

# Basic system paths required to prevent parser crashes
icon.filename = %(source.dir)s/icon.png
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 0
