import os
import paramiko

# need to be in root in order to have env vars
host = "romiq"
port = 22
username = os.getenv("UNAME")
# print(username)
password = os.getenv("PASSWORD")
# print(password)


def run_cmd_ssh(ssh_cmd):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    stdin, stdout, stderr = ssh.exec_command(ssh_cmd)
    lines = stdout.readlines()
    ssh.close()
    print(lines)


if __name__ == "__main__":
    # ssh_cmd = 'whoami'
    # ssh_cmd = f"Rscript -e \"write.csv(mtcars, '/home/{username}/out.csv')\""
    ssh_cmd = f'Rscript /home/{username}/test.R'
    print(ssh_cmd)
    run_cmd_ssh(ssh_cmd)
