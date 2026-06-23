from helpers.wait_helper import WaitHelper
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL

class AuthHelper:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WaitHelper(driver)

    def login(self, email, password):
        # Selalu pastikan sesi bersih sebelum login agar tidak ter-redirect
        self.driver.delete_all_cookies()
        self.driver.get(f"{BASE_URL}/login")
        
        email_field = self.wait.wait_for_element(By.ID, "email")
        email_field.clear()
        email_field.send_keys(email)
        
        password_field = self.wait.wait_for_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)
        
        submit_btn = self.wait.wait_for_clickable(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()
        
        # Wait for dashboard to load
        self.wait.wait_for_element(By.CSS_SELECTOR, ".main-content")
        
        # Tangani SweetAlert "Selamat Datang!" yang muncul setelah login sukses
        try:
            swal_confirm = self.wait.wait_for_clickable(By.CLASS_NAME, "swal2-confirm")
            swal_confirm.click()
            # Tunggu hingga animasi overlay SweetAlert benar-benar menghilang
            self.wait.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "swal2-container")))
        except Exception:
            pass # Lanjutkan jika SweetAlert tidak muncul
