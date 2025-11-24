# 🚗 AutoUsateMilanoRent - Sistema Integrato

## 📋 PANORAMICA
Sistema completo per gestione prenotazioni online con integrazione database del programma principale.

## 🎯 FUNZIONALITÀ IMPLEMENTATE

### ✅ **Sistema Iscrizione**
- Form completo con tutti i dati richiesti
- Validazione campi obbligatori
- Accettazione privacy policy

### ✅ **Sistema Prenotazione**
- Selezione veicolo automatica
- Date ritiro/riconsegna
- Sede di ritiro
- Note aggiuntive

### ✅ **Integrazione Database**
- Salvataggio clienti con suffisso "WEB"
- Creazione prenotazioni nel database
- Visualizzazione nel programma principale

## 🚀 AVVIO SISTEMA

### **1. Avvio Backend Server**
```bash
# Metodo 1: Script automatico
start_server.bat

# Metodo 2: Manuale
pip install -r requirements.txt
python backend_server.py
```

### **2. Apertura Sito Web**
Apri il file: `AutousateMilanoRent.html` nel browser

## 🔧 CONFIGURAZIONE

### **Database**
- **Percorso**: `G:\Il mio Drive\Backup Database\RentSuitePro360\autonoleggio.db`
- **Tabelle utilizzate**: `customers`, `bookings`, `cars`

### **Server**
- **Porta**: 5000
- **URL**: http://localhost:5000
- **CORS**: Abilitato per integrazione frontend

## 📊 FLUSSO PRENOTAZIONE

1. **Utente clicca "Prenota"** su un veicolo
2. **Apertura form iscrizione** con dati completi
3. **Salvataggio cliente** nel database con suffisso "WEB"
4. **Apertura form prenotazione** con veicolo preselezionato
5. **Salvataggio prenotazione** nel database
6. **Conferma** con ID prenotazione

## 🎨 INTERFACCIA UTENTE

### **Modali Responsive**
- Design moderno con Tailwind CSS
- Validazione real-time
- Chiusura con click esterno
- Scroll per contenuti lunghi

### **Feedback Utente**
- Messaggi di successo/errore
- ID prenotazione per riferimento
- Conferme visive

## 🔍 ENDPOINTS API

### **POST /api/save-booking**
Salva iscrizione e prenotazione
```json
{
  "nome": "Mario",
  "cognome": "Rossi",
  "email": "mario@email.com",
  "telefono": "1234567890",
  "data_nascita": "1990-01-01",
  "codice_fiscale": "RSSMRA90A01H501U",
  "indirizzo": "Via Roma 1",
  "citta": "Milano",
  "cap": "20100",
  "vehicle": "Fiat Panda",
  "data_ritiro": "2024-01-15T10:00",
  "data_riconsegna": "2024-01-20T18:00",
  "sede_ritiro": "Aeroporto Milano Malpensa",
  "note": "Note aggiuntive"
}
```

### **POST /api/check-availability**
Verifica disponibilità veicoli
```json
{
  "start_date": "2024-01-15T10:00",
  "end_date": "2024-01-20T18:00"
}
```

### **GET /api/vehicles**
Lista veicoli disponibili

### **GET /health**
Health check server

## 🎯 VISUALIZZAZIONE NEL PROGRAMMA

### **Clienti WEB**
- Nome: "Mario"
- Cognome: "Rossi WEB"
- Fonte: "WEB"
- Data registrazione: automatica

### **Prenotazioni WEB**
- Status: "PENDING"
- Fonte: "WEB"
- Data creazione: automatica
- Note: include sede ritiro

## 🛠️ TROUBLESHOOTING

### **Errore Connessione Database**
- Verifica percorso database
- Controlla permessi file
- Verifica struttura tabelle

### **Errore Server**
- Controlla porta 5000 libera
- Verifica dipendenze Python
- Controlla log errori

### **Errore Frontend**
- Verifica CORS abilitato
- Controlla console browser
- Verifica URL endpoint

## 📝 NOTE TECNICHE

- **Backend**: Flask + SQLite
- **Frontend**: HTML5 + JavaScript + Tailwind CSS
- **Database**: SQLite (stesso del programma principale)
- **CORS**: Abilitato per integrazione
- **Validazione**: Lato client e server

## 🔄 AGGIORNAMENTI FUTURI

- [ ] Sistema email automatiche
- [ ] Pagamenti online
- [ ] Dashboard admin
- [ ] Notifiche push
- [ ] App mobile





