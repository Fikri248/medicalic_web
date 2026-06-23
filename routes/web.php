<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Auth;
use App\Http\Controllers\DashboardController;
use App\Http\Controllers\KategoriController;
use App\Http\Controllers\ObatController;
use App\Http\Controllers\TransaksiController;
use App\Http\Controllers\LaporanController;
use App\Http\Controllers\Auth\LoginController;

// Halaman login utama di root
Route::get('/', [LoginController::class, 'showLoginForm'])->name('login.show');

// Route bawaan untuk proses login
Route::get('/login', [LoginController::class, 'showLoginForm'])->name('login');
Route::post('/login', [LoginController::class, 'login'])->name('login.post');

// halaman login hanya dapat diakses di localhost:8000
if (request()->getHttpHost() === 'localhost:8000') {
    Auth::routes(['register' => false]);
} else {
    Auth::routes(['login' => false, 'register' => false]);
}

// route bebas middleware
Route::get('kategori/data', [KategoriController::class, 'getData'])->name('master-data.kategori.data');
Route::get('obat/data', [ObatController::class, 'getData'])->name('master-data.obat.data');
Route::get('transaksi/data', [TransaksiController::class, 'getData'])->name('transaksi.getData');
Route::get('/laporan/obat/pdf', [LaporanController::class, 'cetakObatPdf'])->name('laporan.obat.pdf');
Route::get('/laporan/transaksi/pdf', [LaporanController::class, 'cetakTransaksiPdf'])->name('laporan.transaksi.pdf');
Route::get('/laporan/obat/excel', [LaporanController::class, 'cetakObatExcel'])->name('laporan.obat.excel');
Route::get('/laporan/transaksi/excel', [LaporanController::class, 'cetakTransaksiExcel'])->name('laporan.transaksi.excel');

// middleware autentikasi
Route::middleware(['auth'])->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'index'])->name('dashboard');

    Route::get('/master-data/jenis', function () {
        return view('master_data.jenis');
    })->name('master-data.jenis');

    Route::prefix('master-data/kategori')->group(function () {
        Route::get('/', [KategoriController::class, 'index'])->name('master-data.kategori');
        Route::get('/create', [KategoriController::class, 'create'])->name('master-data.kategori.create');
        Route::post('/', [KategoriController::class, 'store'])->name('master-data.kategori.store');
        Route::delete('/{id}', [KategoriController::class, 'destroy'])->name('master-data.kategori.destroy');
    });

    Route::prefix('master-data/obat')->group(function () {
        Route::get('/', [ObatController::class, 'index'])->name('master-data.obat');
        Route::get('/create', [ObatController::class, 'create'])->name('master-data.obat.create');
        Route::post('/', [ObatController::class, 'store'])->name('master-data.obat.store');
        Route::get('/{id}/edit', [ObatController::class, 'edit'])->name('master-data.obat.edit');
        Route::put('/{id}', [ObatController::class, 'update'])->name('master-data.obat.update');
        Route::delete('/{id}', [ObatController::class, 'destroy'])->name('master-data.obat.destroy');
    });

    Route::prefix('transaksi')->group(function () {
        Route::get('/', [TransaksiController::class, 'index'])->name('transaksi');
        Route::get('/create', [TransaksiController::class, 'create'])->name('transaksi.create');
        Route::post('/', [TransaksiController::class, 'store'])->name('transaksi.store');
        Route::get('/{id}/edit', [TransaksiController::class, 'edit'])->name('transaksi.edit');
        Route::put('/{id}', [TransaksiController::class, 'update'])->name('transaksi.update');
        Route::delete('/{id}', [TransaksiController::class, 'destroy'])->name('transaksi.destroy');
    });

    Route::prefix('laporan')->group(function () {
        Route::get('/', [LaporanController::class, 'index'])->name('laporan.index');
    });

    Route::post('/logout', [LoginController::class, 'logout'])->name('logout');
});

// blokir halaman register
Route::fallback(function () {
    abort(404, 'Page Not Found');
});
