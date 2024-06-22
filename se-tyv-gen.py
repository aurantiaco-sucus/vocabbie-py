import pickle
from datetime import datetime
from random import randint

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

from support import *

name = "results_{}_{}.pkl".format(
    datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
    randint(1111, 9999))
options = Options()
options.headless = True
driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=options)
results = []
for i in tqdm(range(2000)):
    try:
        results.append(generate_tyv(driver, 0.5, 0.5))
    except Exception as e:
        print(e)
        driver.quit()
        driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=options)
with open(name, "wb") as file:
    pickle.dump(results, file)
