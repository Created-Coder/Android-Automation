import os
from packages import *
import main

if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('config.ini')
    path = config['app_instances_folder']['location']
    tracking_file = config['tracking_file']['location']
    cred_file = config['credentials']['location']

    file = open(cred_file, "r")
    cred = list(csv.reader(file, delimiter=","))
    cred = cred[1:]
    file.close()

    app_instances = [i if i.endswith('.apk') else None for i in os.listdir(path)]

    file_read = open(tracking_file, "r", encoding="utf-8-sig")
    tracking = [i for i in csv.DictReader(file_read)]

    file = open(tracking_file , 'a+', newline='', encoding='utf-8-sig')
    writer_data = csv.writer(file)

    unique_instances = []
    for index, app in enumerate(app_instances):
        res = next((sub for sub in tracking if sub['App Instance'] == app), None)
        if res != None:
            continue

        else:
            unique_instances.append((index,app))
        
    devices = []
    getDevices(devices)
    print(f"Got {len(devices)} Devices in ADB.")

    port = 8200
    processes = []
    
    params = []

    for deviceName in devices:
        realName = getDeviceRealName(deviceName)
        count = input(f"How many instances do you want to open in {realName} : ")
        count = int(count)

        params.append({
            "device" : deviceName,
            "count" : count,
            "real_name" : realName
        })
 

    for i in params:
        count = i['count']
        deviceName = i['device']
        devicerealName = i['real_name']

        desired_capablitites = []
        
        for index, app in unique_instances[:count]:
            apk_file = f"{path}\{app}"
            des_cap = credentials(deviceName, port, apk_file) 
            desired_capablitites.append([des_cap, {"username" : cred[index][0], "password" : cred[index][1]} ])  
            port = port + 5    
            
            writer_data.writerow([app, devicerealName])
            
            print(f"Processing {app} in {devicerealName}")

       
        del unique_instances[:count]    
        
        if desired_capablitites == []:
            print(f"No Unique Instance Found for {devicerealName}")
            continue

        else:
            process = multiprocessing.Process(target=main.main, args=(desired_capablitites, ))
            processes.append(process)
            process.start()
 
    
    for process in processes:
        process.join()



    
    
    
