from dataclasses import dataclass
from random import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


@dataclass
class TyvResult:
    broad_words: list[str]
    broad_sel: list[bool]
    narrow_words: list[str]
    narrow_sel: list[bool]
    result: int


def _tyv_random_click(driver: webdriver.Chrome, rate: float) -> (list[str], list[bool]):
    words = []
    sel = []
    buttons = driver.find_elements(By.TAG_NAME, "button")
    buttons = [button for button in buttons if button.get_attribute("id").startswith("word_")]
    for button in buttons:
        words.append(button.find_element(By.XPATH, "following-sibling::span").text)
        if random() < rate:
            driver.execute_script("arguments[0].click();", button)
            sel.append(True)
        else:
            sel.append(False)
    return words, sel


def generate_tyv(driver: webdriver.Chrome, broad_rate: float, narrow_rate: float) -> TyvResult:
    driver.get("https://preply.com/en/learn/english/test-your-vocab")
    broad_words, broad_sel = _tyv_random_click(driver, broad_rate)
    driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//span[text()='Continue']"))
    wait = WebDriverWait(driver, 10)
    wait.until(lambda d: d.find_elements(By.CLASS_NAME, "preply-ds-heading").__len__() > 1 and
                         d.find_elements(By.CLASS_NAME, "preply-ds-heading")[1].text.startswith("Step 2"))
    narrow_words, narrow_sel = _tyv_random_click(driver, narrow_rate)
    driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//span[text()='Continue']"))
    wait.until(lambda d: d.find_elements(By.CLASS_NAME, "preply-ds-heading").__len__() > 0 and
                         d.find_elements(By.CLASS_NAME, "preply-ds-heading")[0].text.startswith("A"))
    result = int(driver.find_element(By.TAG_NAME, "h3").text)
    return TyvResult(broad_words, broad_sel, narrow_words, narrow_sel, result)
