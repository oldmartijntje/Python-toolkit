import os
import json

def map_folder_to_json(folder_path):
    data = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # Use relative paths for JSON structure
            relative_path = os.path.relpath(file_path, folder_path)
            data[relative_path] = {
                "size": os.path.getsize(file_path),
                "created_time": os.path.getctime(file_path),
                "modified_time": os.path.getmtime(file_path)
            }
    return data

def save_to_json(data, output_file):
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    folder_path = input("Enter the path of the folder you want to map: ")
    output_file = input("Enter the name of the output JSON file (with .json extension): ")
    
    folder_data = map_folder_to_json(folder_path)
    save_to_json(folder_data, output_file)
    print(f"Folder mapped successfully to {output_file}")
