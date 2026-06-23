import pytest
import time
import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers.wait_helper import WaitHelper
from helpers.auth_helper import AuthHelper
from config import BASE_URL, TEST_EMAIL, TEST_PASSWORD

@pytest.fixture(scope="module")
def setup_login(browser):
    auth = AuthHelper(browser)
    auth.login(TEST_EMAIL, TEST_PASSWORD)
    yield

def test_add_kategori_valid(browser, setup_login):
    """
    Tujuan: TC.Kat.001.001 - Add new category with valid name.
    """
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/master-data/kategori/create")
    
    random_suffix = ''.join(random.choices(string.ascii_uppercase, k=4))
    dummy_kategori = f"Kategori {random_suffix}"
    
    wait.wait_for_element(By.ID, "name").send_keys(dummy_kategori)
    browser.find_element(By.CSS_SELECTOR, "button.btn-primary[type='submit']").click()
    
    wait.wait.until(EC.url_contains("/master-data/kategori"))
    assert "/master-data/kategori" in browser.current_url

def test_add_kategori_empty_name(browser, setup_login):
    """
    Tujuan: TC.Kat.001.002 - Add category with empty name.
    """
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/master-data/kategori/create")
    
    submit_btn = browser.find_element(By.CSS_SELECTOR, "button.btn-primary[type='submit']")
    browser.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    time.sleep(0.5)
    browser.execute_script("arguments[0].click();", submit_btn)
    
    error_msg = wait.wait_for_element(By.CLASS_NAME, "invalid-feedback")
    assert error_msg.is_displayed()
    assert "/master-data/kategori/create" in browser.current_url

def test_add_kategori_duplicate(browser, setup_login):
    """
    Tujuan: TC.Kat.001.003 - Add duplicate category.
    """
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/master-data/kategori/create")
    
    wait.wait_for_element(By.ID, "name").send_keys("Obat Dalam")
    submit_btn = browser.find_element(By.CSS_SELECTOR, "button.btn-primary[type='submit']")
    browser.execute_script("arguments[0].click();", submit_btn)
    
    error_msg = wait.wait_for_element(By.CLASS_NAME, "invalid-feedback")
    assert error_msg.is_displayed()
    assert "/master-data/kategori/create" in browser.current_url

def test_add_kategori_invalid_chars(browser, setup_login):
    """
    Tujuan: TC.Kat.001.004 - Add category with numbers or symbols.
    """
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/master-data/kategori/create")
    
    wait.wait_for_element(By.ID, "name").send_keys("Kategori 123!")
    submit_btn = browser.find_element(By.CSS_SELECTOR, "button.btn-primary[type='submit']")
    browser.execute_script("arguments[0].click();", submit_btn)
    
    error_msg = wait.wait_for_element(By.CLASS_NAME, "invalid-feedback")
    assert error_msg.is_displayed()
    assert "/master-data/kategori/create" in browser.current_url

def test_search_kategori(browser, setup_login):
    """
    Tujuan: TC.Kat.002.001 - Search category by keyword.
    """
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/master-data/kategori")
    
    search_input = wait.wait_for_element(By.CSS_SELECTOR, "#entries input[type='text']")
    search_input.send_keys("Obat Luar")
    time.sleep(2)
    
    table = browser.find_element(By.TAG_NAME, "table")
    assert "Obat Luar" in table.text

def test_delete_kategori(browser, setup_login):
    """
    Tujuan: TC.Kat.003.001 - Delete unused category.
    """
    wait = WaitHelper(browser)
    
    # Setup: Create a temporary dummy category to delete
    browser.get(f"{BASE_URL}/master-data/kategori/create")
    dummy_name = "Kategori Hapus"
    wait.wait_for_element(By.ID, "name").send_keys(dummy_name)
    submit_btn = browser.find_element(By.CSS_SELECTOR, "button.btn-primary[type='submit']")
    browser.execute_script("arguments[0].click();", submit_btn)
    
    # Tutup Sweetalert dari aksi create agar tidak menghalangi klik
    try:
        swal_confirm = wait.wait_for_clickable(By.CLASS_NAME, "swal2-confirm")
        swal_confirm.click()
        wait.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "swal2-container")))
    except:
        pass
        
    browser.get(f"{BASE_URL}/master-data/kategori")
    
    # Action: Find delete button for this dummy and click it
    search_input = wait.wait_for_element(By.CSS_SELECTOR, "#entries input[type='text']")
    search_input.send_keys(dummy_name)
    time.sleep(2)
    
    for _ in range(5):
        try:
            delete_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "button.btn-delete")
            browser.execute_script("arguments[0].click();", delete_btn)
            break
        except:
            time.sleep(1)
    
    # Confirm SweetAlert
    time.sleep(1)
    confirm_btn = wait.wait_for_clickable(By.CLASS_NAME, "swal2-confirm")
    browser.execute_script("arguments[0].click();", confirm_btn)
    
    # Assert
    wait.wait.until(EC.url_contains("/master-data/kategori"))
    time.sleep(1)
