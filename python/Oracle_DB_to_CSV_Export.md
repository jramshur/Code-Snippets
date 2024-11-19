
# Oracle Database to CSV Export Script

This Python script connects to an Oracle database, executes a SQL query to fetch data from a specified table, and exports the results to a CSV file. It includes a VPN connection check to ensure the script runs only when the VPN is connected.

## Prerequisites

1. **Python**: Ensure Python is installed on your system.
2. **Oracle Client**: Ensure the Oracle client is installed and available.
3. **Python Packages**: Install the required Python packages using `pip`:
    ```bash
    pip install pandas sqlalchemy oracledb
    ```

## Environment Setup

### Environment Variables

Set the environment variable for the Oracle database password using below commands in a command prompt. This step may require admin priviledges.

#### On Windows:
1. Open Command Prompt and run:
    ```bash
    setx ORACLE_DB_PASSWORD "your_password"
    ```

#### On macOS/Linux:
1. Open Terminal and run:
    ```bash
    export ORACLE_DB_PASSWORD="your_password"
    ```
### How to open command prompt on Windows
1. Click the Start button or press the Windows key on your keyboard.
2. Type "cmd" or "Command Prompt" in the search bar.
3. In the search results, right-click on Command Prompt and select "Run as administrator".
4. If prompted by the User Account Control (UAC) dialog, click Yes to allow the application to make changes to your device.

## Script Explanation

### Imports

```python
import oracledb
import pandas as pd
import sqlalchemy
import csv
import os
import subprocess
import platform
```

### Functions

- `init_oracle_client(lib_dir)`  
Initializes the Oracle client to force Thick mode.

- `get_db_credentials()`  
Retrieves the database credentials, including username, password (from environment variable), and TNS alias.

- `create_engine(username, password, tnsnames_alias)`  
Creates the SQLAlchemy engine for connecting to the Oracle database.

- `execute_query(engine, sql_query)`  
Executes the SQL query and fetches the results into a DataFrame.

- `save_to_csv(df, filepath)`  
Saves the DataFrame to a CSV file.

- `check_vpn_status(host)`
Checks if the VPN is connected by pinging a specific host.

- `main()`  
Main function that coordinates the execution:
    1. Checks VPN status.
    2. Initializes the Oracle client.
    3. Retrieves database credentials.
    4. Creates the database engine.
    5. Executes the SQL query.
    6. Saves the results to a CSV file.

### Final Code/Script

```python
import oracledb
import pandas as pd
import sqlalchemy
import csv
import os
import subprocess
import platform

def init_oracle_client(oracle_lib_dir):
    """Initialize the Oracle client to force Thick mode."""
    try:
        oracledb.init_oracle_client(lib_dir=oracle_lib_dir)
    except Exception as e:
        print(f"Failed to initialize Oracle client: {e}")
        raise

def get_db_password(env_var_name):
    """Retrieve the database password from system environment varibles."""
    password = os.getenv(env_var_name)
    if not password:
        raise EnvironmentError(f"The {env_var_name} environment variable is missing / not found.")
    return password

def create_engine(username, password, tnsnames_alias):
    """Create the SQLAlchemy engine."""
    try:
        engine = sqlalchemy.create_engine(f'oracle+oracledb://{username}:{password}@{tnsnames_alias}')
        return engine
    except Exception as e:
        print(f"Failed to create engine: {e}")
        raise

def execute_query(engine, sql_query):
    """Execute the SQL query and fetch the results into a DataFrame."""
    try:
        df = pd.read_sql(sql_query, engine)
        return df
    except Exception as e:
        print(f"Failed to execute query: {e}")
        raise

def save_to_csv(df, filepath):
    """Save the DataFrame to a CSV file."""
    try:
        df.to_csv(filepath, index=False, quoting=csv.QUOTE_ALL)
    except Exception as e:
        print(f"Failed to save DataFrame to CSV: {e}")
        raise

def check_vpn_status(host):
    """Check if the VPN is connected by pinging a specific host."""
    try:
        if platform.system().lower() == 'windows':
            command = ['ping', '-n', '3', '-w', '1000', host]
        else:
            command = ['ping', '-c', '3', '-W', '1', host]

        output = subprocess.run(command, capture_output=True, text=True)
        if output.returncode == 0:
            return True, f"VPN STATUS CHECK: VPN is connected. Successfully pinged {host}."
        else:
            return False, f"VPN STATUS CHECK: VPN is NOT connected. Failed to ping {host}."
    except Exception as e:
        return False, f"VPN STATUS CHECK: An error occurred: {e}"

def main():
    # User defined variables. Thise will need to be modified for your enviroment.
    vpn_host = 'ent.core.medtronic.com'  # host used to check vpn status
    oracle_lib_dir = r"C:\APPS\oracle\product\19.0.0\client_1\bin"  # Oracle client bin directory
    oracle_tnsnames_alias = 'my_tnsnames_alias'  # alias used in tnsnames.ora file
    oracle_username = 'myOracleUsername'
    env_var_name = 'ORACLE_DB_PASSWORD'  # name of system environment variable containing password
    sql_query = "SELECT * FROM myuser.mytable"  # sql query to execute
    csv_filepath = r'C:\Users\MyUser\Documents\my_csv_filename.csv'
    
    #Check VPN connectivity by pinging a host that is only available when connected to VPN.
    vpn_connected, vpn_message = check_vpn_status(vpn_host)
    if not vpn_connected:
        print(vpn_message)
        return
    print(vpn_message)
    
    try:
        # MAIN CODE
        print('Attempting to retreive and export Oracle data...')
        init_oracle_client(oracle_lib_dir)
        oracle_password = get_db_password(env_var_name)
        engine = create_engine(oracle_username, oracle_password, oracle_tnsnames_alias)
        data_df = execute_query(engine, sql_query)
        save_to_csv(data_df, csv_filepath)
        print(f"### SUCCESS ###. Oracle data exported. Output file saved to: \n{csv_filepath}")

    # Handle exceptions
    except oracledb.DatabaseError as e:
        print(f"### EXPORT FAILED ###. Database error occurred: {e}")
    except EnvironmentError as e:
        print(f"### EXPORT FAILED ###. Environment error: {e}")
    except Exception as e:
        print(f"### EXPORT FAILED ###. An error occurred: {e}")
    finally:
        if 'engine' in locals():
            engine.dispose()

if __name__ == "__main__":
    main()
```

## Running the Script

1. Ensure you have set the `ORACLE_DB_PASSWORD` environment variable.
2. Open a terminal or command prompt.
3. Navigate to the directory where the script is saved.
4. Run the script:
    ```bash
    python your_script_name.py
    ```

The script will check the VPN connection, connect to the Oracle database, execute the query, and save the results to a specified CSV file.

## Troubleshooting

- **Failed to initialize Oracle client**: Ensure the Oracle client is installed and the path is correctly specified.
- **Environment variable missing**: Ensure the environment variable is set correctly including correct name.
- **Database connection issues**: Verify the database credentials and TNS alias.
