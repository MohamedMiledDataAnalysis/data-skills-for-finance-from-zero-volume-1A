# check_java.py - show which Java and Python Spark will use
import os
import subprocess
import sys

print("Python:", sys.version.split()[0])
print("JAVA_HOME:", os.environ.get("JAVA_HOME", "(not set)"))
result = subprocess.run(
    ["java", "-version"], capture_output=True, text=True
)
print(result.stderr.strip().splitlines()[-3])
