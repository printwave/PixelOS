import subprocess

class Run():
    def run(script_name):
        global result
        try:
            result = subprocess.run(['python', script_name], check=True)
        except subprocess.CalledProcessError as e:
            return result