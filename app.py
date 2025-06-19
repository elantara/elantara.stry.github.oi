from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'rahasia_elantara'

ARTIKEL_FILE = 'data/artikel.json'

# Fungsi bantu simpan artikel
def simpan_artikel(data):
    if not os.path.exists(ARTIKEL_FILE):
        with open(ARTIKEL_FILE, 'w') as f:
            json.dump([], f)
    with open(ARTIKEL_FILE, 'r+') as f:
        artikel = json.load(f)
        artikel.append(data)
        f.seek(0)
        json.dump(artikel, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'elantara123':
            session['user'] = request.form['username']
            return redirect('/tulis')
        return "Login gagal"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/tulis', methods=['GET', 'POST'])
def tulis():
    if 'user' not in session:
        return redirect('/login')
    if request.method == 'POST':
        judul = request.form['judul']
        isi = request.form['isi']
        kategori = request.form['kategori']
        artikel = {
            'judul': judul,
            'kategori': kategori,
            'isi': isi,
            'penulis': session['user']
        }
        simpan_artikel(artikel)
        return "Artikel berhasil disimpan!"
    return render_template('tulis.html')

@app.route('/artikel')
def tampilkan_artikel():
    if not os.path.exists(ARTIKEL_FILE):
        return jsonify([])
    with open(ARTIKEL_FILE) as f:
        artikel = json.load(f)
    return jsonify(artikel)

if __name__ == '__main__':
    app.run(debug=True)
