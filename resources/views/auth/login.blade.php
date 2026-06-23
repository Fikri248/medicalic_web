<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Admin Apotek</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }

        body {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #00b4d8, #0077b6);
            padding: 20px;
        }

        .login-container {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
            width: 100%;
            max-width: 400px;
        }

        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }

        .login-header h1 {
            color: #0077b6;
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        .login-header svg {
            margin-bottom: 1rem;
        }

        .pulse {
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        .login-form {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .form-group {
            position: relative;
        }

        .form-group input {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        .form-group input:focus {
            border-color: #0077b6;
            outline: none;
        }

        .form-group label {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            background: white;
            padding: 0 5px;
            color: #666;
            font-size: 0.9rem;
            pointer-events: none;
            transition: all 0.3s ease;
        }

        .form-group input:focus + label,
        .form-group input:not(:placeholder-shown) + label {
            top: 0;
            font-size: 0.8rem;
            color: #0077b6;
        }

        .login-btn {
            background: #0077b6;
            color: white;
            padding: 12px;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .login-btn:hover {
            background: #00b4d8;
            transform: translateY(-2px);
        }

        .copyright {
            text-align: center;
            margin-top: 1rem;
            color: #666;
            font-size: 0.8rem;
        }

        @media (max-width: 480px) {
            .login-container {
                padding: 1.5rem;
            }

            .login-header h1 {
                font-size: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <svg width="100" height="100" viewBox="0 0 100 100" fill="none" class="pulse">
                <circle cx="50" cy="50" r="45" stroke="#0077b6" stroke-width="4"/>
                <circle cx="50" cy="50" r="35" stroke="#00b4d8" stroke-width="4"/>
                <circle cx="50" cy="50" r="25" stroke="#00b4d8" stroke-width="4"/>
                <rect x="35" y="45" width="30" height="10" fill="#22c55e" rx="2"/>
                <rect x="45" y="35" width="10" height="30" fill="#22c55e" rx="2"/>
            </svg>
            <h1>Medicalic</h1>
            <p>Admin Login Form</p>
        </div>

        <form class="login-form" method="POST" action="{{ url('/login') }}">
            @csrf

            <div class="form-group">
                <input type="email" id="email" name="email" placeholder=" " value="{{ old('email') }}" required>
                <label for="email">Email</label>
                @error('email')
                <span class="invalid-feedback" role="alert" style="color: red; font-size: 0.8rem;">
                    <strong>{{ $message }}</strong>
                </span>
                @enderror
            </div>

            <div class="form-group">
                <input type="password" id="password" name="password" placeholder=" " required>
                <label for="password">Password</label>
                @error('password')
                <span class="invalid-feedback" role="alert" style="color: red; font-size: 0.8rem;">
                    <strong>{{ $message }}</strong>
                </span>
                @enderror
            </div>

            <button type="submit" class="login-btn">Login</button>
        </form>

        <div class="copyright">
            © 2025 Apotek Medicalic. All rights reserved.
        </div>
    </div>
</body>
</html>
