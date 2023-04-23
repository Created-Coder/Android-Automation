from packages import *


def main(des_cap): 
    config = configparser.ConfigParser()
    config.read('config.ini')

   
    interval = config['time']['interval']

    count = 0
    if config['proxy']['enabled'] == "Yes":
        print("Proxy Enabled : ON")
        des_cap_proxy = config_proxy(des_cap[0][0]['udid'], des_cap[0][0]['systemPort'])

        flag = True
        while flag:
            try:
                driver = webdriver.Remote('http://localhost:4723/wd/hub',des_cap_proxy)
                print("Oxylab App Opening!")
                time.sleep(5)
                flag = False


            except Exception as e:
                des_cap_proxy['systemPort'] = des_cap_proxy['systemPort'] + 5
                count = count + 1
                if count == 10:
                    print("Issues in connectitiy of Device, Please check device in adb and try again.")
                    flag = False

                else:
                    time.sleep(1)
                    continue
        
        proxy(driver, des_cap_proxy)
        print("Proxy Connected!")

    else:
        print("Proxy Enabled : OFF")

    time.sleep(5)
    
    # while True:
    for i, desired_cap in enumerate(des_cap):
        cred = desired_cap[1]
        desired_cap = desired_cap[0]
    
        try:
            
            for j in range(5):
                try:
                    killPort(desired_cap['systemPort'])
                    driver = webdriver.Remote('http://localhost:4723/wd/hub',desired_cap)
                    print(i + 1, f"{desired_cap['app']} App Opening!")
                    time.sleep(5)
                    break

                except Exception as e:
                    if "systemPort" in str(e):
                        desired_cap['systemPort'] = desired_cap['systemPort'] + 5
                        print(f"Port is busy, Shifting to {desired_cap['systemPort']}")
                        
                        continue

                    else:
                        # print(e)
                        print("Unknown Error")
                        continue

            count = 0
            flag = True
            while flag:
                if driver.current_activity == "com.deezer.android.ui.activity.LauncherActivity":
                    time.sleep(0.25)
                    continue


                if driver.current_activity == "com.deezer.feature.unloggedpages.smartJourney.SmartJourneyActivity":
                    print("App is not logged in. Bot is doing logging!")
                    time.sleep(5)

                    driver, response = logIn(driver, cred['username'],cred['password'])
                    print(f"Logged in with {cred['username'], cred['password']}")

                    if response == "Logged in Successfully":
                        print(response)
                        print("Playing Music.")
                        driver, response = music(driver)

                        print(response)

                    else:
                        print("App not logged in!")

                    flag = False

                elif driver.current_activity == "com.deezer.ui.dynamicpage.DynamicPageRootActivity":
                    print("App is already logged in!")
                    time.sleep(5)

                    count = 0
                    while True:
                        try:
                            try:
                                WebDriverWait(driver, 5).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, "//android.widget.ProgressBar"))
                                )

                                print("Loading")
                            
                            except:
                                break

                            if count == 20:
                                break
                            
                            else:
                                time.sleep(2)
                                count = count + 1

                            continue

                        except:
                            break
                    
                    driver, response = playMusic(driver)
                    
                    if response == "Play button pressed again!":
                        print(response)

                    elif response == "Not Found Play button":
                        driver, response = music(driver)
                        print(response)                    
                    
                    flag = False

                else:
                    count = count + 1
                    if count == 10:
                        time.sleep(2)
                        flag = False

                    
        except Exception as e:
            continue  

        
        time.sleep(int(interval))
            
