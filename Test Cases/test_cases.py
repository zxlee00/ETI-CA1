import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pytest
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

def test_viewing_home_page():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:8000/projects")

    assert driver.page_source.find("SELF INTRODUCTION")
    assert driver.page_source.find("RESUME")
    driver.quit()

def test_scrolling():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:8000/projects")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    scrollTop = driver.execute_script("return document.body.scrollTop;")
    scrollHeight = driver.execute_script("return document.body.scrollHeight;")
    clientHeight = driver.execute_script("return document.body.clientHeight;")
    assert scrollTop == scrollHeight - clientHeight

    driver.quit()

def test_viewing_blog_page():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:8000/projects")

    blog_link_elem = driver.find_element_by_link_text("Blog")
    blog_link_elem.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "blogpageheader")))

    assert driver.find_element_by_link_text("CCA")
    assert driver.find_element_by_link_text("Hobbies")
    assert driver.find_element_by_link_text("Taspense")

    driver.quit()

def test_check_home_page_title():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:8000/projects")

    assert driver.title == "Home" 

    driver.quit()

def test_check_blog_page_title():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:8000/projects")

    blog_link_elem = driver.find_element_by_link_text("Blog")
    blog_link_elem.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "blogpageheader")))

    assert driver.title == "Blog"

    driver.quit()

def test_viewing_blog_post_details():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:8000/projects")

    blog_link_elem = driver.find_element_by_link_text("Blog")
    blog_link_elem.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "blogpageheader")))

    cca_blog_post_elem = driver.find_element_by_link_text("CCA")
    cca_blog_post_elem.click()

    assert driver.page_source.find("CCA")
    assert driver.page_source.find("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed \
                                    do eiusmod tempor incididunt ut labore et dolore magna aliqua. \
                                    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris \
                                    nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in \
                                    reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla \
                                    pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa \
                                    qui officia deserunt mollit anim id est laborum")
    assert driver.find_element_by_xpath('//a[contains(@href, "/blog/cca/")]')
    assert driver.page_source.find("Test Comment")

    driver.quit()

def test_viewing_list_of_posts_by_category():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:8000/projects")

    blog_link_elem = driver.find_element_by_link_text("Blog")
    blog_link_elem.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "blogpageheader")))

    cca_category_elem = driver.find_element_by_xpath('//a[contains(@href, "/blog/cca/")]')
    cca_category_elem.click()
    
    assert WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(., 'Cca')]]")))
    assert driver.find_element_by_link_text("CCA")

    driver.quit()

def test_leaving_a_comment():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:8000/projects")

    blog_link_elem = driver.find_element_by_link_text("Blog")
    blog_link_elem.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "blogpageheader")))

    taspense_blog_post_elem = driver.find_element_by_link_text("Taspense")
    taspense_blog_post_elem.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(., 'Taspense')]]")))

    author_txtfld_elem = driver.find_element_by_name("author")
    author_txtfld_elem.send_keys("Lee Zhi Xuan")

    body_txtfld_elem = driver.find_element_by_name("body")
    body_txtfld_elem.send_keys("Test Comment 1")

    submit_btn_elem = driver.find_element_by_class_name("btn.btn-primary")
    submit_btn_elem.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(., 'Taspense')]]"))) #wait for the page to refresh
    assert driver.find_element_by_xpath("//b[text()[contains(., 'Lee Zhi Xuan')]]")
    assert driver.find_element_by_xpath("//p[text()[contains(., 'Test Comment 1')]]")

    driver.quit()

def test_comment_author_more_than_60_chars():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:8000/projects")

    blog_link_elem = driver.find_element_by_link_text("Blog")
    blog_link_elem.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "blogpageheader")))
    taspense_blog_post_elem = driver.find_element_by_link_text("Taspense")
    taspense_blog_post_elem.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(., 'Taspense')]]")))
    author_txtfld_elem = driver.find_element_by_name("author")
    author_txtfld_elem.send_keys("ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHI") #61 characters

    assert author_txtfld_elem.get_attribute('value') == "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGH"

    driver.quit()
    
def test_leaving_comment_without_author():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:8000/projects")

    blog_link_elem = driver.find_element_by_link_text("Blog")
    blog_link_elem.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "blogpageheader")))
    taspense_blog_post_elem = driver.find_element_by_link_text("Taspense")
    taspense_blog_post_elem.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(., 'Taspense')]]")))

    submit_btn_elem = driver.find_element_by_class_name("btn.btn-primary")
    submit_btn_elem.click()

    assert driver.find_element_by_css_selector("input:invalid")

    driver.quit()

def test_leaving_comment_without_body():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://localhost:8000/projects")

    blog_link_elem = driver.find_element_by_link_text("Blog")
    blog_link_elem.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "blogpageheader")))
    taspense_blog_post_elem = driver.find_element_by_link_text("CCA")
    taspense_blog_post_elem.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(., 'CCA')]]")))

    author_txtfld_elem = driver.find_element_by_name("author")
    author_txtfld_elem.send_keys("Lee Zhi Xuan")

    assert author_txtfld_elem.get_attribute('value') == "Lee Zhi Xuan"
    
    submit_btn_elem = driver.find_element_by_class_name("btn.btn-primary")
    submit_btn_elem.click()

    assert driver.find_element_by_css_selector("textarea:invalid")

    driver.quit()
