#For working from AWS RDP to Local make sure that your VPC security Inbound and Outbond rule have your IP address forwarded
#please refer to the link mentioned below:
# 

#installing packages
import winrm
import pandas as pd
import io

def get_file_from_aws_win_rdp(hostname, username, password, use_ssl=False):
  try:
    # Create a WinRM session
    session = winrm.Session(
        hostname,
        auth=(username, password),

        transport='ntlm',
        server_cert_validation='ignore' if not use_ssl else 'validate'
    )
    
    remote_file_path = "C:\\path_to_remote_locations\\file_to_download.csv"
    powershell_command = f'Get-Content -Path "{remote_file_path}"'
    # Execute the command on the remote machine
    result = session.run_ps(powershell_command)
    # Check if the command execution was successful
    if result.status_code == 0:
        # Extract the file content from the command output
        file_content = result.std_out.decode('utf-8')
        df = pd.read_csv(io.StringIO(file_content))

        print(file_content)
    else:
        print('Failed to read the file.')
    
    # Close the session
    session.close()


  except Exception as e:
    print(f"Error occurred: {e}")

# Replace these values with your actual Windows server details
hostname = 'host_ip_address'
username = 'Host_username' #its your admin name
password = 'host_password'

 

# Call the function to establish the WinRM connection and run a PowerShell command
rdp_file = get_file_from_aws_win_rdp(hostname, username, password)
