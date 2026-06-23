@extends('layouts.app')

@section('title', 'Dashboard')

@section('content')
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="stats-card blue-card">
                <h6>Total Obat Tersedia</h6>
                <div class="d-flex justify-content-between align-items-center">
                    <i class="fas fa-download fa-2x"></i>
                    <h3>{{ $totalObatTersedia ?? 0 }}</h3>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stats-card green-card">
                <h6>Total Obat Terjual</h6>
                <div class="d-flex justify-content-between align-items-center">
                    <i class="fas fa-upload fa-2x"></i>
                    <h3>{{ $totalObatTerjual ?? 0 }}</h3>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stats-card orange-card">
                <h6>Total Semua Obat</h6>
                <div class="d-flex justify-content-between align-items-center">
                    <i class="fas fa-box fa-2x"></i>
                    <h3>{{ $totalSemuaObat ?? 0 }}</h3>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="stats-card purple-card">
                <h6>Total Pendapatan + PPN</h6>
                <div class="d-flex justify-content-between align-items-center">
                    <i class="fas fa-money-bill fa-2x"></i>
                    <h3 style="font-size: 24px;">Rp {{ number_format($totalPendapatan ?? 0, 0, ',', '.') }}</h3>
                </div>
            </div>
        </div>
    </div>

    <div class="card mt-4">
        <div class="card-body">
            <h5 class="card-title">
                <i class="fas fa-chart-line me-2"></i>
                Statistik Daftar Obat
            </h5>
            <canvas id="salesChart" style="max-height: 400px;"></canvas>
        </div>
    </div>

    <div class="card mt-4">
        <div class="card-body">
            <h5 class="card-title">Selamat Datang di Website Apotek Medicalic</h5>
            <p class="card-text text-muted">Anda adalah anggota kelompok 2 yang memiliki akses penuh terhadap sistem.</p>
        </div>
    </div>
@endsection

@push('scripts')
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        const labels = @json($chartLabels);
        const data = @json($chartData);

        const ctx = document.getElementById('salesChart').getContext('2d');
        const salesChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Jumlah Stok Obat',
                    data: data,
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            font: {
                                size: 14
                            }
                        },
                        onClick: null
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    </script>
@endpush
