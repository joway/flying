import subprocess


def run_cmd(cmd):
    success = True
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        success = False
        out = e.output
    return success, out.decode('utf-8')
