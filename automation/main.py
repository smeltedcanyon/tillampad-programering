from subprocess import run
import sys

print(sys.argv)
platform = sys.platform.lower()

if 'win' in platform:
    run(["winget", "install", "--id", "Microsoft.VisualStudioCode"])
elif 'linux' in platform:
    try:
        os_release = open("/etc/os-release").read().lower()
    except FileNotFoundError:
        os_release = ""

    if "alpine" in os_release:
        run(["sudo", "apk", "add", "--no-cache", "code"])
    elif "debian" in os_release or "ubuntu" in os_release:
        run(["sudo", "apt", "update", "-y"])
        run(["sudo", "apt", "install", "-y", "code"])
    else:
        print("nun supported bro")
