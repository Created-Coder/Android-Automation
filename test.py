import os
from packages import *
import main

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    path = config['app_instances_folder']['location']

    app_instances = [i if i.endswith('.apk') else None for i in os.listdir(path)]

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

        desired_capablitites = []
        for app in app_instances[:count]:
            apk_file = f"{path}\{app}"
            des_cap = credentials(deviceName, port, apk_file) 
            desired_capablitites.append(des_cap)

        del app_instances[:count]    
        port = port + 5

        print(desired_capablitites)

    for process in processes:
        process.join()