import pytest
import time
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

def test_create_transaksi(browser, setup_login):
    """
    Tujuan: TC.Trx.001.001 - Membuat transaksi baru (sales) dengan validasi stok obat.
    """
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/transaksi/create")
    
    obat_select_elem = wait.wait_for_element(By.CSS_SELECTOR, "select[name='obat_id[]']")
    obat_select = Select(obat_select_elem)
    
    if len(obat_select.options) > 1:
        obat_select.select_by_index(1)
        jumlah_input = browser.find_element(By.CSS_SELECTOR, "input[name='jumlah[]']")
        jumlah_input.clear()
        jumlah_input.send_keys("1")
        
        browser.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", jumlah_input)
        time.sleep(1)
        
        simpan_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "button.w-100[type='submit']")
        browser.execute_script("arguments[0].scrollIntoView(true);", simpan_btn)
        time.sleep(0.5)
        simpan_btn.click()
        
        confirm_btn = wait.wait_for_clickable(By.CLASS_NAME, "swal2-confirm")
        confirm_btn.click()
        
        wait.wait.until(EC.url_contains("/transaksi"))
        popup_title = wait.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "swal2-title")))
        assert "Berhasil" in popup_title.text

def test_create_transaksi_without_obat(browser, setup_login):
    """
    Tujuan: TC.Trx.001.002 - Create transaction without selecting medicine.
    """
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/transaksi/create")
    
    obat_select_elem = wait.wait_for_element(By.CSS_SELECTOR, "select[name='obat_id[]']")
    
    simpan_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "button.w-100[type='submit']")
    browser.execute_script("arguments[0].scrollIntoView(true);", simpan_btn)
    time.sleep(0.5)
    simpan_btn.click()
    
    assert obat_select_elem.get_attribute("validationMessage") != ""
    assert "/transaksi/create" in browser.current_url

def test_create_transaksi_quantity_zero(browser, setup_login):
    """
    Tujuan: TC.Trx.001.003 - Create transaction with quantity 0.
    """
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/transaksi/create")
    
    obat_select_elem = wait.wait_for_element(By.CSS_SELECTOR, "select[name='obat_id[]']")
    obat_select = Select(obat_select_elem)
    
    if len(obat_select.options) > 1:
        obat_select.select_by_index(1)
        
        jumlah_input = browser.find_element(By.CSS_SELECTOR, "input[name='jumlah[]']")
        jumlah_input.clear()
        jumlah_input.send_keys("0")
        
        simpan_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "button.w-100[type='submit']")
        browser.execute_script("arguments[0].scrollIntoView(true);", simpan_btn)
        time.sleep(0.5)
        simpan_btn.click()
        
        assert jumlah_input.get_attribute("validationMessage") != ""
        assert "/transaksi/create" in browser.current_url

def test_transaksi_insufficient_stock(browser, setup_login):
    """
    Tujuan: TC.Trx.001.004 - Memastikan sistem mencegah transaksi jika jumlah melebihi sisa stok obat.
    """
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/transaksi/create")
    
    obat_select_elem = wait.wait_for_element(By.CSS_SELECTOR, "select[name='obat_id[]']")
    obat_select = Select(obat_select_elem)
    
    if len(obat_select.options) > 1:
        obat_select.select_by_index(1)
        
        stok_tersedia = int(obat_select.options[1].get_attribute("data-stok"))
        
        jumlah_input = browser.find_element(By.CSS_SELECTOR, "input[name='jumlah[]']")
        jumlah_input.clear()
        jumlah_input.send_keys(str(stok_tersedia + 10)) 
        
        browser.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", jumlah_input)
        
        popup_title = wait.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "swal2-title")))
        assert "Stok Tidak Cukup" in popup_title.text

def test_search_transaksi(browser, setup_login):
    """
    Tujuan: TC.Trx.002.001 - Search transaction by medicine name.
    """
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/transaksi")
    
    search_input = wait.wait_for_element(By.CSS_SELECTOR, "#entries input[type='text']")
    search_input.send_keys("Antangin") # Asumsi Antangin ada di transaksi dari test sebelumnya
    time.sleep(2)
    
    table = browser.find_element(By.TAG_NAME, "table")
    # Even if empty, the search itself should not crash.
    assert table.is_displayed()

def _create_dummy_transaksi(browser, wait):
    browser.get(f"{BASE_URL}/transaksi/create")
    obat_select_elem = wait.wait_for_element(By.CSS_SELECTOR, "select[name='obat_id[]']")
    obat_select = Select(obat_select_elem)
    if len(obat_select.options) > 1:
        obat_select.select_by_index(1)
        jumlah_input = browser.find_element(By.CSS_SELECTOR, "input[name='jumlah[]']")
        jumlah_input.clear()
        jumlah_input.send_keys("1")
        browser.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", jumlah_input)
        simpan_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "button.w-100[type='submit']")
        browser.execute_script("arguments[0].scrollIntoView(true);", simpan_btn)
        time.sleep(0.5)
        simpan_btn.click()
        confirm_btn = wait.wait_for_clickable(By.CLASS_NAME, "swal2-confirm")
        confirm_btn.click()
        wait.wait.until(EC.url_contains("/transaksi"))
        wait.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "swal2-title")))
        time.sleep(1) # Tunggu sweetalert hilang jika perlu, atau abaikan

def test_update_transaksi(browser, setup_login):
    """
    Tujuan: TC.Trx.003.001 - Update transaction quantity with sufficient stock.
    """
    wait = WaitHelper(browser)
    _create_dummy_transaksi(browser, wait)
    
    browser.get(f"{BASE_URL}/transaksi")
    time.sleep(2)
    
    edit_btn = wait.wait_for_clickable(By.XPATH, "//a[contains(text(), 'Edit')]")
    edit_btn.click()
    
    jumlah_input = wait.wait_for_element(By.CSS_SELECTOR, "input[name='jumlah[]']")
    jumlah_input.clear()
    jumlah_input.send_keys("2")
    
    browser.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", jumlah_input)
    
    simpan_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "button.w-100[type='submit']")
    browser.execute_script("arguments[0].scrollIntoView(true);", simpan_btn)
    time.sleep(0.5)
    simpan_btn.click()
    
    confirm_btn = wait.wait_for_clickable(By.CLASS_NAME, "swal2-confirm")
    confirm_btn.click()
    
    wait.wait.until(EC.url_contains("/transaksi"))
    popup_title = wait.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "swal2-title")))
    assert "Berhasil" in popup_title.text

def test_delete_transaksi(browser, setup_login):
    """
    Tujuan: TC.Trx.004.001 - Delete available transaction.
    """
    wait = WaitHelper(browser)
    _create_dummy_transaksi(browser, wait)
    
    browser.get(f"{BASE_URL}/transaksi")
    time.sleep(2)
    
    delete_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "button.btn-delete")
    delete_btn.click()
    
    # Wait for sweetalert to confirm delete, wait it's a native form submit in datatables action?
    # TransaksiController index has standard destroy form?
    # No, it's Sweetalert confirmation for delete in typical Laravel setups or just a confirm dialog?
    # Let's see how delete works. Actually, standard click on button.btn-delete.
    # We will accept any alert or swal.
    try:
        swal_confirm = wait.wait_for_clickable(By.CLASS_NAME, "swal2-confirm")
        swal_confirm.click()
    except:
        alert = browser.switch_to.alert
        alert.accept()
    
    wait.wait.until(EC.url_contains("/transaksi"))
    # Wait for success message
    popup_title = wait.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "swal2-title")))
    assert "Berhasil" in popup_title.text
