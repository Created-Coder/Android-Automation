from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from appium.webdriver.common.touch_action import TouchAction
import time
import csv
import adbutils
import os
import configparser
import multiprocessing
import subprocess
import psutil
import pickle
import socket

def killPort(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)

    try:
        sock.connect(('localhost', port))
        sock.shutdown(socket.SHUT_RDWR)
        print(f"Port {port} has been successfully killed")
    except:
        print(f"Port {port} is available for use")
    finally:
        sock.close()


def credentials(udid, systemPort, app):
    config = configparser.ConfigParser()
    config.read('config.ini')

    return {
        "platformName" : config['desired_cap']['platformName'],
        "udid" : udid,
        "systemPort" : int(systemPort),
        "session-override" : True,
        # "noReset" : config['desired_cap']['noReset'],
        "app" : app,
        # "newCommandTimeout" : int(config['desired_cap']['newCommandTimeout']),
        # "appWaitDuration" : 50000,
        # "appWaitForLaunch" : True
        "appWaitActivity" : "com.deezer.android.ui.activity.LauncherActivity"
        # "appWaitActivity" : "com.deezer.android.ui.activity.LauncherActivity,com.deezer.feature.unloggedpages.smartJourney.SmartJourneyActivity,com.deezer.ui.dynamicpage.DynamicPageRootActivity"
    }

def config_proxy(udid, systemPort):
    config = configparser.ConfigParser()
    config.read('config.ini')

    return {
        "platformName" : config['proxy']['platformName'],
        "udid" : udid,
        "systemPort" : int(systemPort),
        "noReset" : config['proxy']['noReset'],
        "app" : config['proxy']['apk'],
        "newCommandTimeout" : int(config['proxy']['newCommandTimeout']),
    }

def getDevices(devices):
    flag = True
    while flag:
        # os.system('cmd /c "adb kill-server"')
        # time.sleep(2)
        # os.system('cmd /c "adb start-server"')

        for info in adbutils.adb.device_list():
            devices.append(info.serial)
        
        return

def getDeviceRealName(adbName):
    output = subprocess.check_output(["adb","-s", adbName,"shell", "getprop"])
    manufacturer = next((line for line in output.decode().splitlines() if "product.manufacturer" in line),"")
    model = next((line for line in output.decode().splitlines() if "product.model" in line),"")
    
    manufacturer = manufacturer.split(":")[-1].replace("[", "").replace("]", "").strip()
    
    model = model.split(":")[-1].replace("[", "").replace("]", "").strip()
    
    device = f"{manufacturer.capitalize()} {model}"
    
    return device


def proxy(driver, des_cap):
    handle_one_size = driver.get_window_size()
    height = handle_one_size['height']

    time.sleep(2)
    wait = WebDriverWait(driver, 10)

    try:
        addproxyBtn = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//android.widget.Button[@index='1']"))
            )
        addproxyBtn.click()

        name = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//android.widget.EditText[@index='2']"))
            )
        name.send_keys('proxy')

        ip = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//android.widget.EditText[@index='7']"))
            )
        ip.send_keys('proxy.packetstream.io')

        port = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//android.widget.EditText[@index='9']"))
            )
        port.send_keys('31112')

        
        TouchAction(driver).press(x=243, y= height-200).move_to(x=240, y=0).release().perform()
        
        time.sleep(2)
        
        userName = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//android.view.View[@text='Username']/following-sibling::android.widget.EditText"))
                )

        userName.send_keys('froschimteich')

        password = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//android.view.View[@text='Password']/following-sibling::android.widget.EditText"))
            )
        password.send_keys('2rsprXHMbAYdC0EA')

        createBtn = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//android.widget.ScrollView/../android.view.View[@index='2']"))
            )
        
        createBtn.click()

        time.sleep(2)

        proxy_click = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//android.view.View[@text='Proxy List']/following-sibling::android.view.View"))
            )
        
        proxy_click.click()


    except Exception as e:
        proxy_click = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//android.view.View[@text='Proxy List']/following-sibling::android.view.View"))
            )
         
        proxy_click.click()

    
    return driver

#Login Function 
def logIn(driver, mail,password):    
    
    wait = WebDriverWait(driver, 20)

    # Click on input

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//android.widget.TextView[@text='Email or phone number']"))
        ).click()
    
    except:
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//android.widget.TextView[contains(@text,'Email')]"))
        ).click()

    time.sleep(1)
    
    # Send Email on Input
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//android.widget.EditText[contains(@text,'Email or phone number')]"))
        ).send_keys(f"{mail}")

    except:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//android.widget.EditText[contains(@text,'Email')]"))
        ).send_keys(f"{mail}")

    time.sleep(1)

    # Click on Continue button

    
    wait.until(
         EC.presence_of_element_located(
             (By.XPATH, "//android.widget.Button[contains(@resource-id,'continue_btn')]"))
     ).click()
    
    time.sleep(1)
    
    # Click on Password Input

    try:
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//android.widget.EditText[@text='Your password']"))
        ).send_keys(f"{password}")

    except:
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//android.widget.EditText[contains(@text,'password')]"))
        ).send_keys(f"{password}")

         
    time.sleep(1)
    
    # Click on Continue button

    wait.until(
         EC.presence_of_element_located(
             (By.XPATH, "//android.widget.Button[contains(@resource-id,'continue_btn')]"))
     ).click()
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//android.widget.Button[contains(@resource-id,'continue_btn')]"))
        ).click()

        time.sleep(2)

        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//android.widget.EditText[contains(@text,'Email or phone number')]"))
            ).send_keys(f"{mail}")

        except:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//android.widget.EditText[contains(@text,'Email')]"))
            ).send_keys(f"{mail}")

        time.sleep(2)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//android.widget.Button[contains(@resource-id,'continue_btn')]"))
        ).click()

    except:
        pass

    time.sleep(2)

    try:
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//android.widget.TextView[@text='Edit']"))
        )
        profile = WebDriverWait(driver, 5).until(
             EC.presence_of_element_located(
                 (By.XPATH, "//android.widget.ImageView[@index='0']"))
         ).click()
        
    except:
        pass

    return driver, "Logged in Successfully"



    

# music search and play function
def music(driver):
    config = configparser.ConfigParser()
    config.read('config.ini')
    music = config['music']['name']

    wait = WebDriverWait(driver, 10)

    searchBtn = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//android.widget.FrameLayout[@content-desc='Search']"))
    ).click()

    print("Click Search Button")

    time.sleep(5)

    driver.press_keycode(84)

    search = wait.until(
         EC.presence_of_element_located(
             (By.XPATH, "//android.widget.EditText[contains(@resource-id,'search_src_text')]"))
     ).send_keys(music)

    driver.press_keycode(66)
    
    searchResult = wait.until(
         EC.presence_of_element_located(
             (By.XPATH, "//android.widget.ImageView[contains(@resource-id,'cover')]"))
     ).click()
    
    print("Click on Search Result")

    time.sleep(10)
    

    playBtn = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//android.widget.TextView[contains(@resource-id,'playlist_page_play_fab')]"))
    ).click()
    
    print("Click Play Button")
    
    time.sleep(5)
   

    try:
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//android.widget.TextView[contains(@resource-id,'track_title_collapsed')]"))
        ).click()

    except:
        pass

    wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(@resource-id,'player_more_button')]"))
        ).click()

    time.sleep(3)

    wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//android.widget.ImageView[contains(@resource-id,'card_cover')]"))
        ).click()
    
    time.sleep(5)

    # try:
    #    repeat =  wait.until(
    #                 EC.presence_of_element_located(
    #                   (By.XPATH, "//android.widget.ImageView[@content-desc='Repeat']"))
    #             ).click()
       
    #    print("Clicked Repeat Button")

    # except:
    #     print("Not Found Repeat Button")
    
    
    time.sleep(5)
    
    driver.background_app(-1)
    return driver, "Music Played, App is running in background."


def playMusic(driver):
    wait = WebDriverWait(driver, 10)

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//android.widget.TextView[contains(@resource-id,'track_title_collapsed')]"))
        )


    except Exception as e:
        return driver, "Not Found Play button"

    
    count = 0
    while True:
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//android.widget.ProgressBar[contains(@resource-id,'player_buffering_notification')]"))
            )

            print("Loading button found in already played sound")
            
            if count == 20:
                break
            
            else:
                time.sleep(2)
                count = count + 1

            continue

        except:
            break

    try:
        playAgain = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//android.widget.ImageView[@content-desc='Play']"))
        ).click()

        time.sleep(10)

        driver.background_app(-1)
        print("App is running in background")
        return driver, "Play button pressed again!"

    except Exception as e:
        return driver, "Not Found Play button"
    

    
    