import subprocess

# List the scripts in the order you want to run them
# scripts = ["gariHtmlExtractor.py", "reportExtractor.py", "imageExtractor.py"]
scripts = ["imageExtractor.py"]


for script in scripts:
    print(f"\n=== RUNNING {script} ===\n")
    # subprocess.run waits until the script finishes
    result = subprocess.run(["python3", script], capture_output=False)
    
    if result.returncode != 0:
        print(f"[ERROR] {script} exited with code {result.returncode}")
    else:
        print(f"[DONE] {script} finished successfully")