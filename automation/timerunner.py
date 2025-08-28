import subprocess
import time
import sys
from pathlib import Path

# --------- CONFIGURATION ---------
# Set this to your target file (Python script or .exe)
target = r"main.py"  # or "main.exe"
runs = 10  # number of times to run
# ---------------------------------

target_path = Path(target)

if not target_path.exists():
    print(f"Error: {target_path} does not exist.")
    sys.exit(1)

times = []

for i in range(runs):
    start = time.time()
    if target_path.suffix == ".py":
        subprocess.run([sys.executable, str(target_path)])
    elif target_path.suffix == ".exe":
        subprocess.run([str(target_path)])
    else:
        print("Error: Target must be a .py or .exe file.")
        sys.exit(1)
    end = time.time()
    elapsed = end - start
    times.append(elapsed)
    print(f"Run {i+1}: {elapsed:.6f} seconds")

average = sum(times) / len(times)
print(f"\nAverage execution time over {runs} runs: {average:.6f} seconds")
