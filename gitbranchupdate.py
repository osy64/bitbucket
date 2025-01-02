import git
import paramiko
import sys
import chilkat

def ssh_connect():

        repo_path = '/efs/clickandgo/www/staging3/web'
        branch_name = 'develop'           # Branch you want to update to
        hostname = '10.100.68.198'  # Server's IP address or hostname
        username = 'ubuntu'  # SSH username

        key = chilkat.CkSshKey()
        keyStr = key.loadText("C:\\Users\\osama\\Desktop\\c&G\\clickandgo-priv-key.ppk")
        success = key.FromPuttyPrivateKey(keyStr)
        if (success != True):
            print(key.lastErrorText())
            sys.exit()
        bEncrypt = False
        unencryptedKeyStr = key.toOpenSshPrivateKey(bEncrypt)
        success = key.SaveText(unencryptedKeyStr, "staging_openssh.pem")
        if (success != True):
            print(key.lastErrorText())
            sys.exit()
        private_key_path = "C:\\gitupdate\\staging_openssh.pem"
        key = paramiko.RSAKey.from_private_key_file(private_key_path)

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname, username=username, pkey=key)
            # stdin, stdout, stderr = client.exec_command('df -h')
            # print(stdout.read().decode())
            stdin, stdout, stderr = client.exec_command('cd /efs/clickandgo/www/staging3/web/;sudo git checkout develop;git branch;sudo git pull origin develop;sudo git status -u no')
            print(stdout.read().decode())
            #stdin, stdout, stderr = client.exec_command('sudo git branch')
            #print(stdout.read().decode())

            # repo = git.Repo(repo_path)  # Initialize the repository object
            # origin = repo.remotes.origin  # Get the remote repository
            # repo.git.checkout(branch_name)  # Checkout the desired branch
            # #origin.pull()  # Pull the latest changes from the remote repository
            # print(f"Successfully switched to branch '{branch_name}' and updated the repository.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            client.close()

if __name__ == '__main__':
    ssh_connect()