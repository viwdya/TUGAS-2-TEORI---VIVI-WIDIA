from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)

# Fungsi untuk membaca data dari CSV
def load_data():
    try:
        print("Memulai proses membaca file CSV...")  # Debug log
        df = pd.read_csv('jumlah_sd_smp_lab.csv')  # Pastikan nama file sesuai
        print("File CSV berhasil dimuat.")
        print(df.head())  # Menampilkan beberapa baris pertama untuk debugging
        return df
    except Exception as e:
        print(f"Error saat membaca file CSV: {e}")
        return pd.DataFrame()  # Kembalikan DataFrame kosong jika terjadi error

# Fungsi untuk prediksi menggunakan Monte Carlo
def monte_carlo_prediction(df, year, num_simulations=1000):
    try:
        # Ambil data jumlah sekolah
        data = df['jumlah_sekolah'].values
        mean = np.mean(data)
        std_dev = np.std(data)

        # Simulasi Monte Carlo
        simulated_data = np.random.normal(mean, std_dev, num_simulations)
        prediction = simulated_data.mean()
        print(f"Hasil prediksi Monte Carlo untuk tahun {year}: {prediction}")
        return prediction
    except Exception as e:
        print(f"Error di monte_carlo_prediction: {e}")
        return 0

# Route untuk halaman utama
@app.route('/')
def index():
    try:
        print("Route / dipanggil")
        df = load_data()
        if df.empty:
            return "<h1>Data CSV kosong atau tidak ditemukan.</h1>"

        table_html = df.to_html(classes='table table-striped', index=False)
        return render_template('index.html', table_html=table_html)
    except Exception as e:
        print(f"Error di route /: {e}")
        return f"<h1>Error: {e}</h1>"

# Route untuk prediksi
@app.route('/predict', methods=['POST'])
def predict():
    try:
        print("Route /predict dipanggil")
        year = request.form.get('year')
        if not year:
            return "<h1>Error: Tahun harus diisi.</h1>"

        year = int(year)
        df = load_data()
        if df.empty:
            return "<h1>Data CSV kosong atau tidak ditemukan.</h1>"

        prediction = monte_carlo_prediction(df, year)
        return render_template('prediction.html', year=year, prediction=round(prediction, 2))
    except Exception as e:
        print(f"Error di route /predict: {e}")
        return f"<h1>Error: {e}</h1>"

if __name__ == '__main__':
    print("Memulai aplikasi Flask...")
    app.run(host='0.0.0.0', port=2001, debug=True)
    print("Aplikasi Flask berhenti.")
