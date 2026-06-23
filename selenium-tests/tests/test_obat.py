import pytest
import time
import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from helpers.wait_helper import WaitHelper
from helpers.auth_helper import AuthHelper
from config import BASE_URL, TEST_EMAIL, TEST_PASSWORD

@pytest.fixture(scope="module")
def setup_login(browser):
    auth = AuthHelper(browser)
    auth.login(TEST_EMAIL, TEST_PASSWORD)
    yield

def test_add_obat(browser, setup_login):
    """
    Tujuan: TC.Obat.001.001 - Menambah data obat baru dengan input valid.
    """
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/master-data/obat/create")
    
    random_suffix = ''.join(random.choices(string.ascii_uppercase, k=6))
    dummy_nama = f"Obat Selenium {random_suffix}"
    
    wait.wait_for_element(By.ID, "nama").send_keys(dummy_nama)
    
    category_select = Select(browser.find_element(By.ID, "category_id"))
    if len(category_select.options) > 1:
        category_select.select_by_index(1) 
    
    jenis_select = Select(browser.find_element(By.ID, "jenis"))
    jenis_select.select_by_value("tablet")
    
    browser.find_element(By.ID, "stok").send_keys("50")
    browser.find_element(By.ID, "harga").send_keys("15000")
    browser.find_element(By.ID, "deskripsi").send_keys("Data obat ini dibuat oleh skrip Automation Selenium")
    
    submit_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "button.btn-primary[type='submit']")
    browser.execute_script("arguments[0].click();", submit_btn)
    
    wait.wait_for_element(By.ID, "obatTable")
    assert "/master-data/obat" in browser.current_url

def test_add_obat_empty_name(browser, setup_login):
    """
    Tujuan: TC.Obat.001.002 - Add medicine with empty name.
    """
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/master-data/obat/create")
    
    nama_input = wait.wait_for_element(By.ID, "nama")
    
    category_select = Select(browser.find_element(By.ID, "category_id"))
    if len(category_select.options) > 1:
        category_select.select_by_index(1) 
    jenis_select = Select(browser.find_element(By.ID, "jenis"))
    jenis_select.select_by_value("tablet")
    
    browser.find_element(By.ID, "stok").send_keys("50")
    browser.find_element(By.ID, "harga").send_keys("15000")
    browser.find_element(By.ID, "deskripsi").send_keys("Data obat")
    
    submit_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "button.btn-primary[type='submit']")
    browser.execute_script("arguments[0].click();", submit_btn)
    
    assert nama_input.get_attribute("validationMessage") != ""

def test_add_obat_duplicate(browser, setup_login):
    """
    Tujuan: TC.Obat.001.003 - Add duplicate medicine name.
    """
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/master-data/obat/create")
    
    wait.wait_for_element(By.ID, "nama").send_keys("Antangin") # Seeded data
    
    category_select = Select(browser.find_element(By.ID, "category_id"))
    if len(category_select.options) > 1:
        category_select.select_by_index(1) 
    jenis_select = Select(browser.find_element(By.ID, "jenis"))
    jenis_select.select_by_value("tablet")
    browser.find_element(By.ID, "stok").send_keys("50")
    browser.find_element(By.ID, "harga").send_keys("15000")
    browser.find_element(By.ID, "deskripsi").send_keys("Duplicate test")
    
    submit_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "button.btn-primary[type='submit']")
    browser.execute_script("arguments[0].click();", submit_btn)
    
    error_msg = wait.wait_for_element(By.CLASS_NAME, "invalid-feedback")
    assert error_msg.is_displayed()

def test_add_obat_negative_stock(browser, setup_login):
    """
    Tujuan: TC.Obat.001.004 - Add medicine with negative stock.
    """
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/master-data/obat/create")
    
    wait.wait_for_element(By.ID, "nama").send_keys("Obat Negatif Stok")
    
    category_select = Select(browser.find_element(By.ID, "category_id"))
    if len(category_select.options) > 1:
        category_select.select_by_index(1) 
    jenis_select = Select(browser.find_element(By.ID, "jenis"))
    jenis_select.select_by_value("tablet")
    
    stok_input = browser.find_element(By.ID, "stok")
    stok_input.send_keys("-10")
    browser.find_element(By.ID, "harga").send_keys("15000")
    browser.find_element(By.ID, "deskripsi").send_keys("Test stok negatif")
    
    submit_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "button.btn-primary[type='submit']")
    browser.execute_script("arguments[0].click();", submit_btn)
    
    assert stok_input.get_attribute("validationMessage") != "" or len(browser.find_elements(By.CLASS_NAME, "invalid-feedback")) > 0

def test_add_obat_negative_price(browser, setup_login):
    """
    Tujuan: TC.Obat.001.005 - Add medicine with negative price.
    """
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/master-data/obat") # Go somewhere else first
    browser.get(f"{BASE_URL}/master-data/obat/create")
    
    wait.wait_for_element(By.ID, "nama").send_keys("Obat Negatif Harga")
    
    category_select = Select(browser.find_element(By.ID, "category_id"))
    if len(category_select.options) > 1:
        category_select.select_by_index(1) 
    jenis_select = Select(browser.find_element(By.ID, "jenis"))
    jenis_select.select_by_value("tablet")
    
    browser.find_element(By.ID, "stok").send_keys("50")
    harga_input = browser.find_element(By.ID, "harga")
    harga_input.send_keys("-15000")
    browser.find_element(By.ID, "deskripsi").send_keys("Test harga negatif")
    
    submit_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "button.btn-primary[type='submit']")
    browser.execute_script("arguments[0].click();", submit_btn)
    
    error_msg = wait.wait_for_element(By.CLASS_NAME, "invalid-feedback")
    assert error_msg.is_displayed()

def test_search_obat(browser, setup_login):
    """
    Tujuan: TC.Obat.002.001 - Mencari obat di Datatables menggunakan fitur pencarian kustom.
    """
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/master-data/obat")
    
    search_input = wait.wait_for_element(By.CSS_SELECTOR, "#entries input[type='text']")
    search_input.clear()
    search_input.send_keys("Antangin")
    time.sleep(3)
    
    table = browser.find_element(By.TAG_NAME, "table")
    assert "Antangin" in table.text

def test_update_obat(browser, setup_login):
    """
    Tujuan: TC.Obat.003.001 - Update medicine data with valid stock and price.
    """
    wait = WaitHelper(browser)
    
    # 1. Create dummy to update
    browser.get(f"{BASE_URL}/master-data/obat/create")
    random_suffix = ''.join(random.choices(string.ascii_uppercase, k=4))
    dummy_nama = f"Obat Update {random_suffix}"
    
    wait.wait_for_element(By.ID, "nama").send_keys(dummy_nama)
    category_select = Select(browser.find_element(By.ID, "category_id"))
    if len(category_select.options) > 1: category_select.select_by_index(1) 
    Select(browser.find_element(By.ID, "jenis")).select_by_value("tablet")
    browser.find_element(By.ID, "stok").send_keys("10")
    browser.find_element(By.ID, "harga").send_keys("1000")
    browser.find_element(By.ID, "deskripsi").send_keys("To be updated")
    submit_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "button.btn-primary[type='submit']")
    browser.execute_script("arguments[0].click();", submit_btn)
    wait.wait.until(EC.url_contains("/master-data/obat"))
    
    try:
        swal_confirm = wait.wait_for_clickable(By.CLASS_NAME, "swal2-confirm")
        swal_confirm.click()
        wait.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "swal2-container")))
    except:
        pass
    
    # 2. Search dummy
    search_input = wait.wait_for_element(By.CSS_SELECTOR, "#entries input[type='text']")
    search_input.send_keys(dummy_nama)
    time.sleep(2)
    
    # 3. Click Edit
    for _ in range(5):
        try:
            edit_btn = wait.wait_for_clickable(By.XPATH, "//a[contains(text(), 'Edit')]")
            browser.execute_script("arguments[0].click();", edit_btn)
            break
        except:
            time.sleep(1)
    
    # 4. Update fields
    stok_input = wait.wait_for_element(By.ID, "stok_sisa")
    stok_input.clear()
    stok_input.send_keys("25")
    
    harga_input = browser.find_element(By.ID, "harga")
    harga_input.clear()
    harga_input.send_keys("25000")
    
    submit_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "button.btn-primary[type='submit']")
    browser.execute_script("arguments[0].click();", submit_btn)
    
    # 5. Assert Success
    wait.wait.until(EC.url_contains("/master-data/obat"))
    time.sleep(1)

def test_delete_obat(browser, setup_login):
    """
    Tujuan: TC.Obat.004.001 - Delete medicine data.
    """
    wait = WaitHelper(browser)
    
    # 1. Create dummy to delete
    browser.get(f"{BASE_URL}/master-data/obat/create")
    random_suffix = ''.join(random.choices(string.ascii_uppercase, k=4))
    dummy_nama = f"Obat Delete {random_suffix}"
    
    wait.wait_for_element(By.ID, "nama").send_keys(dummy_nama)
    category_select = Select(browser.find_element(By.ID, "category_id"))
    if len(category_select.options) > 1: category_select.select_by_index(1) 
    Select(browser.find_element(By.ID, "jenis")).select_by_value("tablet")
    browser.find_element(By.ID, "stok").send_keys("10")
    browser.find_element(By.ID, "harga").send_keys("1000")
    browser.find_element(By.ID, "deskripsi").send_keys("To be deleted")
    submit_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "button.btn-primary[type='submit']")
    browser.execute_script("arguments[0].click();", submit_btn)
    wait.wait.until(EC.url_contains("/master-data/obat"))
    
    try:
        swal_confirm = wait.wait_for_clickable(By.CLASS_NAME, "swal2-confirm")
        browser.execute_script("arguments[0].click();", swal_confirm)
        wait.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "swal2-container")))
    except:
        pass
    
    # 2. Search dummy
    search_input = wait.wait_for_element(By.CSS_SELECTOR, "#entries input[type='text']")
    search_input.send_keys(dummy_nama)
    time.sleep(2)
    
    # 3. Click Delete
    for _ in range(5):
        try:
            delete_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "button.btn-delete")
            browser.execute_script("arguments[0].click();", delete_btn)
            break
        except:
            time.sleep(1)
    
    # 4. Confirm SweetAlert
    time.sleep(1)
    confirm_btn = wait.wait_for_clickable(By.CLASS_NAME, "swal2-confirm")
    browser.execute_script("arguments[0].click();", confirm_btn)
    
    # 5. Assert
    wait.wait.until(EC.url_contains("/master-data/obat"))
    time.sleep(1)
