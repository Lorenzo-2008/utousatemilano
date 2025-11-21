from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Configurazione database
DB_PATH = "autonoleggio.db"

def init_db():
    """Inizializza il database se non esiste"""
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Crea tabella clienti
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cognome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                telefono TEXT,
                data_nascita TEXT,
                codice_fiscale TEXT,
                indirizzo TEXT,
                citta TEXT,
                cap TEXT,
                password TEXT,
                piva TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crea tabella prenotazioni
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                vehicle_type TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                pickup_location TEXT NOT NULL,
                total_amount REAL NOT NULL,
                payment_method TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        conn.commit()
        conn.close()

def save_customer_to_db(customer_data):
    """Salva i dati del cliente nel database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO customers (nome, cognome, email, telefono, data_nascita, 
                                 codice_fiscale, indirizzo, citta, cap, password, piva)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            customer_data['nome'],
            customer_data['cognome'],
            customer_data['email'],
            customer_data['telefono'],
            customer_data['data_nascita'],
            customer_data['codice_fiscale'],
            customer_data['indirizzo'],
            customer_data['citta'],
            customer_data['cap'],
            customer_data['password'],
            customer_data.get('piva', '')
        ))
        
        conn.commit()
        customer_id = cursor.lastrowid
        return customer_id
    except sqlite3.IntegrityError:
        return None  # Email già esistente
    finally:
        conn.close()

def save_booking_to_db(booking_data):
    """Salva la prenotazione nel database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO bookings (customer_id, vehicle_type, start_date, end_date, 
                                pickup_location, total_amount, payment_method)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            booking_data['customer_id'],
            booking_data['vehicle_type'],
            booking_data['start_date'],
            booking_data['end_date'],
            booking_data['pickup_location'],
            booking_data['total_amount'],
            booking_data['payment_method']
        ))
        
        conn.commit()
        booking_id = cursor.lastrowid
        return booking_id
    except Exception as e:
        print(f"Errore nel salvare la prenotazione: {e}")
        return None
    finally:
        conn.close()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint per verificare che il server funzioni"""
    return jsonify({"status": "ok", "message": "Backend funzionante"})

@app.route('/api/register', methods=['POST'])
def register():
    """Endpoint per la registrazione utenti"""
    try:
        data = request.get_json()
        
        # Valida i dati richiesti
        required_fields = ['nome', 'cognome', 'email', 'telefono', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Campo {field} mancante"}), 400
        
        # Salva nel database
        customer_id = save_customer_to_db(data)
        
        if customer_id:
            return jsonify({
                "success": True,
                "message": "Registrazione completata",
                "customer_id": customer_id
            })
        else:
            return jsonify({"error": "Email già esistente"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Endpoint per il login utenti"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"error": "Email e password richiesti"}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, nome, cognome, email FROM customers 
            WHERE email = ? AND password = ?
        ''', (email, password))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return jsonify({
                "success": True,
                "user": {
                    "id": user[0],
                    "nome": user[1],
                    "cognome": user[2],
                    "email": user[3]
                }
            })
        else:
            return jsonify({"error": "Credenziali non valide"}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/upload-documents', methods=['POST'])
def upload_documents():
    """Endpoint per caricare documenti (simulazione Google Drive)"""
    try:
        # In una implementazione reale, qui caricheresti su Google Drive
        customer_data = request.form.get('customer_data')
        files = request.files
        
        # Simula il caricamento
        print(f"Caricamento documenti per: {customer_data}")
        print(f"File ricevuti: {list(files.keys())}")
        
        return jsonify({
            "success": True,
            "message": "Documenti caricati con successo su Google Drive",
            "files_uploaded": list(files.keys())
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/process-payment', methods=['POST'])
def process_payment():
    """Endpoint per processare i pagamenti"""
    try:
        data = request.get_json()
        payment_method = data.get('payment_method')
        amount = data.get('amount')
        
        # Simula il processamento del pagamento
        print(f"Processamento pagamento: {payment_method} - €{amount}")
        
        # In una implementazione reale, qui integreresti con Stripe, PayPal, etc.
        return jsonify({
            "success": True,
            "payment_id": f"PAY_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "message": f"Pagamento di €{amount} processato con {payment_method}"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/save-booking', methods=['POST'])
def save_booking():
    """Endpoint per salvare le prenotazioni"""
    try:
        data = request.get_json()
        
        # Estrai i dati della prenotazione
        booking_data = {
            'customer_id': data.get('customer_id'),
            'vehicle_type': data.get('vehicle_type'),
            'start_date': data.get('start_date'),
            'end_date': data.get('end_date'),
            'pickup_location': data.get('pickup_location'),
            'total_amount': data.get('total_amount'),
            'payment_method': data.get('payment_method')
        }
        
        # Salva nel database
        booking_id = save_booking_to_db(booking_data)
        
        if booking_id:
            return jsonify({
                "success": True,
                "message": "Prenotazione salvata con successo",
                "booking_id": booking_id
            })
        else:
            return jsonify({"error": "Errore nel salvare la prenotazione"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/vehicles', methods=['GET'])
def get_vehicles():
    """Endpoint per ottenere la lista dei veicoli disponibili"""
    vehicles = [
        {
            "id": 1,
            "name": "Fiat Panda",
            "type": "auto",
            "price_per_day": 25,
            "image": "https://www.media.stellantis.com/cache/9/f/e/6/c/9fe6ce14090f69572fb47bc9910e935ed5be0d23.jpeg",
            "available": True
        },
        {
            "id": 2,
            "name": "Lancia Ypsilon",
            "type": "auto",
            "price_per_day": 30,
            "image": "https://foto.newsauto.it/wp-content/uploads/2023/01/Lancia-Ypsilon-2023-10.jpg",
            "available": True
        },
        {
            "id": 3,
            "name": "DR 6",
            "type": "auto",
            "price_per_day": 35,
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSsxyst6nAvU-JWAWBxGAvvD80Uflx2dFn91Q&s",
            "available": True
        }
    ]
    
    return jsonify({"vehicles": vehicles})

if __name__ == '__main__':
    # Inizializza il database
    init_db()
    
    # Configurazione per Railway
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)