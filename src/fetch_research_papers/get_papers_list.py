import os

def main():
    # Get the current directory
    current_dir = os.getcwd()

    # List all CSV files
    csv_files = [f for f in os.listdir(current_dir) if f.endswith('.csv')]

    if csv_files:
        print("CSV Files in Directory:")
        for file in csv_files:
            print(file)
    else:
        print("No CSV files found in the current directory.")

if __name__ == "__main__":
    main()
