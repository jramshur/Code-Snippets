# VPN Status Check Script

This Python script checks the VPN status by pinging a specified host 5 times. It returns the VPN state (connected or not) and a status message.

## Requirements

- Python 3.x
- `subprocess` module (comes with Python standard library)
- `platform` module (comes with Python standard library)

## Script

```python
import subprocess
import platform

def check_vpn_status(host):
    try:
        # Determine the appropriate ping command based on the OS
        if platform.system().lower() == 'windows':
            command = ['ping', '-n', '5', '-w', '1000', host]  # Timeout in milliseconds, ping 5 times
        else:
            command = ['ping', '-c', '5', '-W', '1', host]  # Timeout in seconds, ping 5 times

        # Run the ping command
        output = subprocess.run(command, capture_output=True, text=True)
        
        # Check if the ping was successful
        if output.returncode == 0:
            return True, f"VPN is connected. Successfully pinged {host} 5 times."
        else:
            return False, f"VPN is not connected. Failed to ping {host} 5 times."
    except Exception as e:
        return False, f"An error occurred: {e}"

def main():
    # Host to ping
    host_to_check = 'ent.core.medtronic.com'

    # Check VPN status
    vpn_state, status_message = check_vpn_status(host_to_check)
    print(status_message)

if __name__ == '__main__':
    main()
```

## Explanation
Importing Modules:

The script imports subprocess to run system commands and platform to detect the operating system.
Defining the check_vpn_status Function:

The function accepts a host parameter, which is the hostname to ping.
Determining the Ping Command:

Based on the operating system, the appropriate ping command is chosen.
For Windows: ping -n 5 -w 1000 host (5 pings with a 1-second timeout each)
For Unix/Linux: ping -c 5 -W 1 host (5 pings with a 1-second timeout each)
Running the Ping Command:

The subprocess.run function executes the ping command and captures the output.
Checking the Ping Results:

The function checks the return code of the ping command.
If the return code is 0, it means at least one ping was successful, indicating the VPN is connected.
Otherwise, it means the ping failed, indicating the VPN is not connected.
Handling Exceptions:

Any exceptions that occur during the execution of the ping command are caught and returned as part of the status message.
Defining the main Function:

The main function defines the host to check, calls the check_vpn_status function, and prints the status message.
Using if __name__ == '__main__'::

This block ensures that the main function is only executed when the script is run directly, not when it is imported as a module.
Usage
Save the script to a file, e.g., check_vpn_status.py.
Run the script using Python:
bash
Copy code
python check_vpn_status.py
