import csv
from datetime import datetime
import os

def write_current_time_to_csv(file_path):
    try:
        # Ensure directory exists
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            print(f"Directory {directory} does not exist. Creating it.")
            os.makedirs(directory, exist_ok=True)

        # Get the current time
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Current time: {current_time}")
        
        # Write the current time to the CSV file
        with open(file_path, mode='a', newline='') as file:
            print(f"Writing to file {file_path}")
            writer = csv.writer(file)
            writer.writerow([current_time])
            print(f"Write successful")

    except PermissionError as e:
        print(f"PermissionError: {e}. Check the file and directory permissions.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage with absolute path
write_current_time_to_csv('/home/ec2-user/Trading_App/test_file.csv')
