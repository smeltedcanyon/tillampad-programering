from subprocess import run
import sys
import time
import random

def fake_download():
    total = 500
    progress = 0
    while progress < total:
        step = random.randint(10, 15)  # random step increase
        progress += step
        if progress > total:
            progress = total
        bar = "#" * (progress // 2) + "-" * ((100 - progress) // 2)
        print(f"\rDownloading: [{bar}] {progress}%", end="")
        time.sleep(random.uniform(0.1, 0.3))  # random delay
    print("\nDone!")

print(sys.argv)
platform = sys.platform.lower()

if 'win' in platform:
    print('Executing command run(["winget", "install", "--id", "Microsoft.VisualStudioCode"])')
    time.sleep(2)
    fake_download()
elif 'linux' in platform:
    try:
        os_release = open("/etc/os-release").read().lower()
    except FileNotFoundError:
        os_release = ""

    if "alpine" in os_release:
        print('Executing command run(["sudo", "apk", "add", "--no-cache", "code"])')
        fake_download()
        # run(["sudo", "apk", "add", "--no-cache", "code"])
    elif "debian" in os_release or "ubuntu" in os_release:
        print('Executing command run(["sudo", "apt", "update", "-y"])')
        fake_download()
        # run(["sudo", "apt", "update", "-y"])

        print('Executing command run(["sudo", "apt", "install", "-y", "code"])')
        fake_download()
        # run(["sudo", "apt", "install", "-y", "code"])
    else:
        print("nun supported bro")
