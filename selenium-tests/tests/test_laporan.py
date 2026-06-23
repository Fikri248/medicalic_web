import os
import time
import glob
import pytest
from selenium.webdriver.common.by import By
from helpers.wait_helper import WaitHelper
from helpers.auth_helper import AuthHelper
from config import BASE_URL, TEST_EMAIL, TEST_PASSWORD, DOWNLOAD_DIR

@pytest.fixture(scope="module")
def setup_login(browser):
    auth = AuthHelper(browser)
    auth.login(TEST_EMAIL, TEST_PASSWORD)
    yield

def clear_download_dir():
    """Helper to ensure the download directory is clean before asserting new downloads."""
    download_path = os.path.abspath(DOWNLOAD_DIR)
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    for f in glob.glob(os.path.join(download_path, "*")):
        try:
            os.remove(f)
        except OSError:
            pass

def wait_for_download(file_pattern, timeout=15):
    """Helper to poll the download directory until the file appears and finishes downloading."""
    download_path = os.path.abspath(DOWNLOAD_DIR)
    end_time = time.time() + timeout
    while time.time() < end_time:
        files = glob.glob(os.path.join(download_path, file_pattern))
        if files:
            file_path = files[0]
            if not file_path.endswith('.crdownload'):
                if os.path.getsize(file_path) > 0:
                    return file_path
        time.sleep(0.5)
    return None

def test_export_pdf_obat_download(browser, setup_login):
    """
    Tujuan: End-to-End Test Export PDF Obat. Menguji klik tombol, proses download, dan validitas file.
    """
    clear_download_dir()
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/laporan")
    
    pdf_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "a[href*='/laporan/obat/pdf']")
    browser.execute_script("arguments[0].click();", pdf_btn)
    
    downloaded_file = wait_for_download("laporan_daftar_obat.pdf")
    
    assert downloaded_file is not None, "File PDF Obat tidak terunduh dalam batas waktu."
    assert downloaded_file.endswith(".pdf")
    assert os.path.getsize(downloaded_file) > 0, "File PDF Obat terunduh tetapi ukurannya 0 bytes (kosong/corrupt)."

def test_export_excel_obat_download(browser, setup_login):
    """
    Tujuan: End-to-End Test Export Excel Obat. Menguji klik tombol, proses download, dan validitas file.
    """
    clear_download_dir()
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/laporan")
    
    excel_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "a[href*='/laporan/obat/excel']")
    browser.execute_script("arguments[0].click();", excel_btn)
    
    expected_filename = "laporan_obat-*.xlsx"
    
    downloaded_file = wait_for_download(expected_filename)
    
    assert downloaded_file is not None, f"File Excel Obat ({expected_filename}) tidak terunduh dalam batas waktu."
    assert downloaded_file.endswith(".xlsx")
    assert os.path.getsize(downloaded_file) > 0, "File Excel Obat terunduh tetapi ukurannya 0 bytes."

def test_export_pdf_transaksi_download(browser, setup_login):
    """
    Tujuan: End-to-End Test Export PDF Transaksi.
    """
    clear_download_dir()
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/laporan")
    
    pdf_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "a[href*='/laporan/transaksi/pdf']")
    browser.execute_script("arguments[0].click();", pdf_btn)
    
    downloaded_file = wait_for_download("laporan-transaksi.pdf")
    
    assert downloaded_file is not None, "File PDF Transaksi tidak terunduh."
    assert downloaded_file.endswith(".pdf")
    assert os.path.getsize(downloaded_file) > 0, "File PDF Transaksi kosong."

def test_export_excel_transaksi_download(browser, setup_login):
    """
    Tujuan: End-to-End Test Export Excel Transaksi.
    """
    clear_download_dir()
    wait = WaitHelper(browser)
    browser.get(f"{BASE_URL}/laporan")
    
    excel_btn = wait.wait_for_clickable(By.CSS_SELECTOR, "a[href*='/laporan/transaksi/excel']")
    browser.execute_script("arguments[0].click();", excel_btn)
    
    expected_filename = "laporan_transaksi-*.xlsx"
    
    downloaded_file = wait_for_download(expected_filename)
    
    assert downloaded_file is not None, "File Excel Transaksi tidak terunduh."
    assert downloaded_file.endswith(".xlsx")
    assert os.path.getsize(downloaded_file) > 0, "File Excel Transaksi kosong."
