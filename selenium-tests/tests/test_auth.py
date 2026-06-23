import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from helpers.wait_helper import WaitHelper
from config import BASE_URL, TEST_EMAIL, TEST_PASSWORD

def test_login_valid_credentials(browser):
    """
    Tujuan: Memastikan admin bisa login dengan email dan password yang benar.
    """
    browser.delete_all_cookies() # Pastikan mulai dari state yang bersih
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/login")
    
    # Action
    browser.find_element(By.ID, "email").send_keys(TEST_EMAIL)
    browser.find_element(By.ID, "password").send_keys(TEST_PASSWORD)
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Assert
    wait.wait_for_element(By.CSS_SELECTOR, ".main-content")
    assert "/dashboard" in browser.current_url

def test_login_invalid_credentials(browser):
    """
    Tujuan: TC.Login.001.005 - Memastikan sistem menolak login dengan kredensial salah.
    """
    browser.delete_all_cookies() # Wajib hapus cookie agar tidak di-redirect ke dashboard!
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/login")
    
    # Action
    browser.find_element(By.ID, "email").send_keys(TEST_EMAIL)
    browser.find_element(By.ID, "password").send_keys("salahpassword")
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Assert
    error_msg = wait.wait_for_element(By.CLASS_NAME, "invalid-feedback")
    assert error_msg.is_displayed()

def test_login_empty_email(browser):
    """
    Tujuan: TC.Login.001.002 - Login with empty email and filled password.
    """
    browser.delete_all_cookies()
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/login")
    
    email_input = browser.find_element(By.ID, "email")
    browser.find_element(By.ID, "password").send_keys(TEST_PASSWORD)
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Assert HTML5 validation message
    assert email_input.get_attribute("validationMessage") != ""

def test_login_empty_password(browser):
    """
    Tujuan: TC.Login.001.003 - Login with registered email but empty password.
    """
    browser.delete_all_cookies()
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/login")
    
    browser.find_element(By.ID, "email").send_keys(TEST_EMAIL)
    password_input = browser.find_element(By.ID, "password")
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Assert HTML5 validation message
    assert password_input.get_attribute("validationMessage") != ""

def test_login_unregistered_email(browser):
    """
    Tujuan: TC.Login.001.004 - Login with unregistered email.
    """
    browser.delete_all_cookies()
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/login")
    
    browser.find_element(By.ID, "email").send_keys("notfound@example.com")
    browser.find_element(By.ID, "password").send_keys("anypassword")
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # Assert backend validation message (invalid-feedback)
    error_msg = wait.wait_for_element(By.CLASS_NAME, "invalid-feedback")
    assert error_msg.is_displayed()

def test_access_dashboard_without_login(browser):
    """
    Tujuan: Memastikan halaman dashboard tidak bisa diakses langsung tanpa login.
    """
    # Action
    browser.delete_all_cookies()
    browser.get(f"{BASE_URL}/dashboard")
    
    # Assert
    wait = WaitHelper(browser)
    wait.wait_for_element(By.ID, "email")
    assert "/login" in browser.current_url or browser.current_url.endswith("/")

def test_logout(browser):
    """
    Tujuan: Memastikan fungsi logout berjalan dengan baik.
    """
    browser.delete_all_cookies() # Pastikan sesi baru
    wait = WaitHelper(browser)
    
    # Setup: Login terlebih dahulu
    browser.get(f"{BASE_URL}/login")
    browser.find_element(By.ID, "email").send_keys(TEST_EMAIL)
    browser.find_element(By.ID, "password").send_keys(TEST_PASSWORD)
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    wait.wait_for_element(By.CSS_SELECTOR, ".main-content")
    
    # Atasi SweetAlert yang menutupi layar setelah login sukses
    try:
        swal_confirm = wait.wait_for_clickable(By.CLASS_NAME, "swal2-confirm")
        swal_confirm.click()
        # Tunggu sampai overlay transparan SweetAlert hilang sepenuhnya
        wait.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "swal2-container")))
    except Exception:
        pass
    
    # Submit form logout langsung agar tidak ketutup elemen sidebar
    logout_form = wait.wait_for_element(By.CSS_SELECTOR, "form[action*='logout']")
    browser.execute_script("arguments[0].submit();", logout_form)

    wait.wait_for_element(By.ID, "email")
    assert "/login" in browser.current_url or browser.current_url.endswith("/")
    
    # Assert
    wait.wait_for_element(By.ID, "email")
    assert "/login" in browser.current_url or browser.current_url.endswith("/")
