from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select 
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from telebot import TeleBot
from telebot.types import InputMediaPhoto
from os import path, makedirs, getenv
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv


load_dotenv()

EMAIL_ENV = getenv("PET_SITTING_EMAIL")
PSSWRD_ENV = getenv("PET_SITTING_PASSWORD")
BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")
CHATID = -100123456789                      # Replace with your actual chat ID ; -100 IF CHANEL
FOLDER_SCREENSHOTS = "screenshots"
BINARY_LOC = "/usr/bin/google-chrome-stable" # DEFAULT FOR LINUX
MINUTES_TO_SLEEP = 12                   # Minutes to sleep if no new offers found





bot = TeleBot(BOT_TOKEN)

while True:

    if not path.exists(FOLDER_SCREENSHOTS):
        makedirs(FOLDER_SCREENSHOTS)
    try: open("used_links.txt", "r")
    except FileNotFoundError: open("used_links.txt", "w").close()

    opts = ChromeOptions()
    opts.binary_location = BINARY_LOC
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    driver = Chrome(options=opts)

    driver.get("https://petsitting24.ch/en/sign_in")
    driver.set_window_size(1920, 3000)
    sleep(1.5)
    

    agree_cookies = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[4]/div[1]/div/div[2]/button[4]")
    agree_cookies.click()
    sleep(1.5)
    try:
        email = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div/form/div[1]/div/div[1]/div[2]/input")
        email.send_keys(EMAIL_ENV)

        psswrd = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div/form/div[2]/div/div[1]/div[2]/input")
        psswrd.send_keys(PSSWRD_ENV) 

        log_btn = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div/input")
        log_btn.click()
    except Exception as e:
        driver.refresh()
        email = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div/form/div[1]/div/div[1]/div[2]/input")
        email.send_keys(EMAIL_ENV)

        psswrd = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div/form/div[2]/div/div[1]/div[2]/input")
        psswrd.send_keys(PSSWRD_ENV) 

        log_btn = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div/input")
        log_btn.click()

    del psswrd, email, log_btn


    select_radius: Select = driver.find_element(By.XPATH, "/html/body/div[2]/form/div[1]/div[2]/select")
    select_radius = Select(select_radius)
    select_radius.select_by_index(3)
    search_offers_btn = driver.find_element(By.XPATH, "/html/body/div[2]/form/div[2]/button")
    search_offers_btn.click()

    del search_offers_btn, select_radius


    list_offers: list[WebElement] = driver.find_elements(By.CLASS_NAME, "search-card__link")
    links_list = [str(link.get_attribute("href")).split("?")[0] for link in list_offers]
    used_links = open("used_links.txt", "r").read().splitlines()
    links_list = [link for link in links_list if link not in used_links]
    with open("used_links.txt", "a") as f:
        for link in links_list:
            f.write(link + "\n")
    if len(links_list) == 0:
        print(f"No new offers found. Sleeping for {MINUTES_TO_SLEEP} minutes...")
        bot.send_message(CHATID, f"No new offers found. Sleeping for {MINUTES_TO_SLEEP} minutes...")
        driver.quit()
        sleep(MINUTES_TO_SLEEP * 60)
        continue
    else:
        for link in links_list:
            
            print(link)
            driver.get(link)
            sleep(2)
            City = driver.find_element(By.CLASS_NAME, "profile__localisation-info-item").text
            try: Species = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[2]/div/div/div[1]/div//div/div[2]").text
            except: Species = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div[2] ").text
            try: created_by = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div/div[2]/div[2]/div/div").text
            except: 
                try: created_by = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div[1]/div[1]/div/div/div/div[2]/div[2]/div/div").text
                except: created_by = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[1]/div/div/div/div[2]/div[2]/div/div").text
            IATA = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[2]")
            IATNC = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[3]")
            IATJ = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div[4]")
            
            png = driver.get_screenshot_as_png()
            im = Image.open(BytesIO(png))
            IATA_png = im.crop((
                IATA.location['x'],
                IATA.location['y'],
                IATA.location['x'] + IATA.size['width'],
                IATA.location['y'] + IATA.size['height']
            ))
            IATA_png.save(f"{FOLDER_SCREENSHOTS}/{link.split('/')[-1]}_IATA.png")
            IATNC_png = im.crop((
                IATNC.location['x'],
                IATNC.location['y'],
                IATNC.location['x'] + IATNC.size['width'],
                IATNC.location['y'] + IATNC.size['height']
            ))
            IATNC_png.save(f"{FOLDER_SCREENSHOTS}/{link.split('/')[-1]}_IATNC.png")
            IATJ_png = im.crop((
                IATJ.location['x'],
                IATJ.location['y'],
                IATJ.location['x'] + IATJ.size['width'],
                IATJ.size['height'] + IATJ.location['y']
            ))
            IATJ_png.save(f"{FOLDER_SCREENSHOTS}/{link.split('/')[-1]}_IATJ.png")

            i1 = open(f"{FOLDER_SCREENSHOTS}/{link.split('/')[-1]}_IATA.png", "rb")
            i2 = open(f"{FOLDER_SCREENSHOTS}/{link.split('/')[-1]}_IATNC.png", "rb")
            i3 = open(f"{FOLDER_SCREENSHOTS}/{link.split('/')[-1]}_IATJ.png", "rb")
            bot.send_media_group(CHATID, [InputMediaPhoto(i1, caption=f"New offer!\n\nLink: {link} \nCity: {City} \nSpecies: {Species} \nCreated by: {created_by}"), InputMediaPhoto(i2), InputMediaPhoto(i3)])
        print(f"Sleeping for {MINUTES_TO_SLEEP} minutes...")
        driver.quit()
        sleep(MINUTES_TO_SLEEP * 60)
