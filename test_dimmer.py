import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

print("--- Step 1: Chrome browser open ho raha hai ---")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get("http://localhost:8080")

    # 1. Test ON Button
    print("--- Step 2: Testing ON Button ---")
    btn_on = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "btn-on"))
    )
    btn_on.click()
    time.sleep(1)
    assert driver.find_element(By.ID, "bulb-status").text == "ON"
    print(">> [PASS] ON Button verified")

    # 2. Test Slider to 80%
    print("--- Step 3: Testing Dimmer Slider (80%) ---")
    slider = driver.find_element(By.ID, "dimmer-slider")
    # JavaScript se slider value 80 set karte hain aur update trigger karte hain
    driver.execute_script("arguments[0].value = 80; arguments[0].dispatchEvent(new Event('input'));", slider)
    time.sleep(1)
    bright_val = driver.find_element(By.ID, "brightness-val").text
    assert bright_val == "80", f"Expected 80, but got {bright_val}"
    print(">> [PASS] Dimmer Slider verified at 80%")

    # 3. Test Reset Button
    print("--- Step 4: Testing Reset Button ---")
    btn_reset = driver.find_element(By.ID, "btn-reset")
    btn_reset.click()
    time.sleep(1)
    assert driver.find_element(By.ID, "bulb-status").text == "OFF"
    assert driver.find_element(By.ID, "brightness-val").text == "0"
    print(">> [PASS] Reset Button verified")

    print("\n=======================================================")
    print(">>> ALL UI TESTS PASSED SUCCESSFULLY! <<<")
    print("=======================================================\n")

finally:
    driver.quit()
    print("--- Browser closed ---")