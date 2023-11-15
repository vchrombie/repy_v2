import os
import json
from subprocess import call

# Paths
writeups_path = "writeups"
reference_monitors_1_path = "2.1_reference_monitors"
reference_monitors_3_path = "2.3_reference_monitors"
json_file_path = 'netid-data.json'

# Function to search for files and return a list of paths
def find_files(directory, format):
    return [os.path.join(directory, f) for f in os.listdir(directory) if format in f]

# Function to create the dictionary from filenames
def create_dict(ref_monitors_1, ref_monitors_3, writeups):
    data = {}
    for ref_monitor in ref_monitors_1:
        netid = os.path.splitext(ref_monitor)[0].split('_')[-1]
        data[netid] = {'reference_monitor_1': os.path.basename(ref_monitor)}

    for ref_monitor in ref_monitors_3:
        netid = os.path.splitext(ref_monitor)[0].split('_')[-1]
        if netid in data:
            data[netid]['reference_monitor_3'] = os.path.basename(ref_monitor)
        else:
            data[netid] = {'reference_monitor_3': os.path.basename(ref_monitor)}

    for writeup in writeups:
        netid, name_ext = os.path.basename(writeup).split(' - ')
        name, _ = os.path.splitext(name_ext)
        if netid in data:
            data[netid]['name'] = name
            data[netid]['writeup'] = os.path.basename(writeup)
        else:
            data[netid] = {'name': name, 'writeup': os.path.basename(writeup)}
    
    for netid in data.keys():
        data[netid] = [
            {'name': data[netid].get('name', None)},
            {'reference_monitor_1': data[netid].get('reference_monitor_1', None)},
            {'reference_monitor_3': data[netid].get('reference_monitor_3', None)},
            {'writeup': data[netid].get('writeup', None)}
        ]
    return data

# Function to open files in VS Code
def open_in_vscode(file_path):
    if file_path:
        call(["code", file_path])
    else:
        print("Error: ", file_path, " does not exist")

# Function to run reference monitor against base attack case
def run_reference_monitor_base_test(reference_monitors_path, ref_monitor):
    print("Running reference monitor against vt2182_attackcase2.r2py")
    os.chdir(reference_monitors_path)
    # run cat ref_monitor
    os.system(f"rr2 {ref_monitor} vt2182_attackcase2.r2py")
    os.system(f"cd ..")
    print(os.getcwd())


# Check if JSON file exists and is not empty
if os.path.exists(json_file_path) and os.path.getsize(json_file_path) > 0:
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    netid = input("Enter netid: ")
    if netid in data:
        name = data[netid][0]['name'] if data[netid][0]['name'] else "No name found"
        print(f"Name: {name}")
        ref_monitor_1 = data[netid][1]['reference_monitor_1']
        ref_monitor_3 = data[netid][2]['reference_monitor_3']
        writeup = data[netid][3]['writeup']

        # Check if the reference monitor or writeup exists and print message accordingly
        ref_monitor_1_path = f"{reference_monitors_1_path}/{ref_monitor_1}" if ref_monitor_1 else "No submission for reference monitor 2.1 assignment"
        ref_monitor_3_path = f"{reference_monitors_3_path}/{ref_monitor_3}" if ref_monitor_3 else "No submission for reference monitor 2.3 assignment"
        writeup_path = f"{writeups_path}/{writeup}" if writeup else "No submission for writeup"

        if not ref_monitor_1:
            print("No submission for reference monitor 2.1 assignment ", name)
        else:
            open_in_vscode(ref_monitor_1_path)

            # Run the reference monitor against base attack case
            run_reference_monitor_base_test(reference_monitors_1_path, ref_monitor_1)

        if not ref_monitor_3:
            print("No submission for reference monitor 2.3 assignment ", name)
        else:
            open_in_vscode(ref_monitor_3_path)

            # Run the reference monitor against base attack case
            run_reference_monitor_base_test(reference_monitors_3_path, ref_monitor_3)

        if not writeup:
            print("No submission for writeup ", name)
        else:
            if writeup.endswith('.docx'):
                call(["open", writeup_path])
            else:
                open_in_vscode(writeup_path)

    else:
        print("No data found for the provided netid ", netid)
else:
    # If the JSON file is empty or doesn't exist, populate it
    ref_monitors_1 = find_files(reference_monitors_1_path , 'reference_monitor_')
    ref_monitors_3 = find_files(reference_monitors_3_path , 'reference_monitor_')
    writeups = find_files(writeups_path, '.docx') + find_files(writeups_path, '.pdf')

    # Create dictionary
    data = create_dict(ref_monitors_1, ref_monitors_3, writeups)

    # Write dictionary to JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
