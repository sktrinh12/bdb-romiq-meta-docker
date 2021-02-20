import subprocess
import os
import re
from datetime import datetime

def validate_barcode(barcode):
    """
    validate the barcode string using the first 8 characters and converting it to a datetime
    """
    str_format = "%Y%m%d"
    try:
        datetime.strptime(barcode[:8], str_format)
        return True
    except ValueError:
        return False

def kill_Rscript():
    """
    kill subprocess (main_driver.R script)
    """
    pid = subprocess.Popen(["ps", "-C", "R"], stdout=subprocess.PIPE)
    pid = subprocess.check_output(["awk", "{print $1}"], stdin=pid.stdout)
    pid = pid.decode("utf8")
    try:
        pid = re.search("\d{1,3}", pid).group()
        kill = subprocess.check_output(["kill", pid])
        msg = f'process killed for: {pid}'
        print(msg)
        return {'output' : msg + ' ' + kill.decode('utf8')}
    except Exception as e:
        err_msg = f'Could not kill Rscript process - {e}'
        print(err_msg)
        return {'output': err_msg}


def run_Rscript(script_name, **kwargs):
    """
    use subprocess library to run Rscript command
    """
    username = os.getenv("UNAME", "bdb")
    version = os.getenv("VERSION", "1_2_1b")
    omiq_path = os.path.join("/home", username, "R")
    if script_name == "main_driver":
        rscript_path = os.path.join(omiq_path, f"omiq_v{version}",
                                    "OmiqPipeline",f"{script_name}.R")
    else:
        rscript_path = os.path.join(omiq_path, f"{script_name}.R")

    # run rscript
    cmd = ["Rscript"]
    cmd.append(rscript_path)
    barcode = kwargs.get('barcode', '')
    re_run = kwargs.get('re_run', '')
    if barcode:
        cmd.append(barcode)
    else:
        raise("need to supply barcode argument")
    if re_run not in ['', None]:
        cmd.append(re_run)

    print('='*40)
    print(f'running command: \"{cmd}\"')
    print('='*40)

    try:
        process = subprocess.check_output(cmd, universal_newlines=True)
    except subprocess.SubprocessError as e:
        err = f'Status: FAIL {e.returncode} {e.output}'
        print(err)
        process = err
    print(process)
    return process

