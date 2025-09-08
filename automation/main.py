from subprocess import run
import sys
print(sys.argv)
platform = sys.platform.lower()

if 'win' in platform:
    run(["winget", "install", "--id", "Microsoft.VisualStudioCode"])
elif 'linux' in platform:
    run(["sudo", "apt", "install", "-y", "code"])
