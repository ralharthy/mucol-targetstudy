import subprocess

spawn = 1
Brange = range(3,11)

if __name__ == "__main__":
    for b in Brange:
        subprocess.run(
            ["python", "akProducer.py", str(b), str(spawn)],
            check=True
        )
        print(f"B = {b:<2}, done!")