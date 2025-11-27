# RentShare

**RentShare** è una piattaforma web moderna per la gestione e la condivisione di proprietà immobiliari attraverso un sistema di quote azionarie. Gli utenti possono visualizzare proprietà, acquistare quote, monitorare rendimenti e gestire il proprio portafoglio in tempo reale.

## 🌟 Funzionalità Principali

### Dashboard
- Visualizzazione interattiva delle proprietà su mappa con Leaflet.js
- Gestione completa delle proprietà con immagini e coordinate GPS
- Aggiunta e rimozione di proprietà tramite interfaccia intuitiva
- Visualizzazione automatica di tutte le proprietà sulla mappa

### Analytics
- KPI cards animate con grafici e statistiche in tempo reale
- Grafici interattivi per analisi dei dati (Line Chart, Bar Chart, Pie Chart)
- Tabelle ordini con stile moderno e gradiente viola/rosa
- Tabella rendimenti dettagliata per monitoraggio performance

### Contratti
- Visualizzazione delle quote azionarie possedute
- Cards eleganti con informazioni dettagliate su ogni proprietà
- Calcolo automatico delle percentuali di possesso
- Design responsive e animato

### Marketplace
- Catalogo proprietà disponibili per l'acquisto
- Sistema di acquisto quote con integrazione wallet crypto
- Supporto per MetaMask (ETH) e Phantom (SOL)
- Conversione automatica prezzi USD/BTC
- Modal di acquisto con selezione wallet

### Impostazioni
- Gestione profilo utente con upload foto
- Configurazione notifiche personalizzate
- Gestione sicurezza e autenticazione a due fattori
- Gestione wallet crypto collegati
- Storico transazioni e sessioni attive

### Modalità Notturna
- Toggle globale per modalità chiara/scura
- Persistenza delle preferenze con localStorage
- Stili ottimizzati per tutti i componenti
- Mappa con tema scuro integrato

## 🛠️ Tecnologie Utilizzate

- **Backend**: Django 5.2.8
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Autenticazione**: Django Allauth
- **Mappe**: Leaflet.js con tiles CartoDB
- **Database**: SQLite3 (sviluppo)
- **Immagini**: Pillow per gestione upload
- **Design**: Custom CSS con tema viola (#8a5cf6)

## 📋 Prerequisiti

- Python 3.8 o superiore
- pip (gestore pacchetti Python)
- Git (opzionale, per clonare il repository)

## 🚀 Installazione

### 1. Clona il Repository (o estrai lo ZIP)

```bash
git clone https://github.com/tuousername/RentShare.git
cd RentShare
```

Oppure se hai ricevuto il file ZIP:
```bash
# Estrai lo ZIP in una cartella
cd RentShare
```

### 2. Crea un Ambiente Virtuale (Raccomandato)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installa le Dipendenze

```bash
pip install -r requirements.txt
```

### 4. Configura il Database

```bash
python manage.py migrate
```

### 5. Crea un Superuser (Admin)

```bash
python manage.py createsuperuser
```

Segui le istruzioni per creare il tuo account amministratore.

### 6. (Opzionale) Popola il Database con Dati di Test

```bash
python populate_db.py
python add_orders.py
```

Questo creerà:
- Aree geografiche (Milano Centro, Roma EUR, Torino Crocetta)
- Proprietà di esempio con immagini
- Transazioni di esempio
- Ordini di esempio

### 7. Avvia il Server di Sviluppo

```bash
python manage.py runserver
```

Il sito sarà disponibile all'indirizzo: **http://127.0.0.1:8000/login/**

## 👤 Credenziali di Accesso

Dopo aver eseguito `populate_db.py`, puoi accedere con:

- **Username**: `admin`
- **Password**: `admin123`

Oppure utilizza le credenziali del superuser che hai creato al punto 5.

## 📁 Struttura del Progetto

```
RentShare/
├── config/                 # Configurazioni Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── dashboard/              # App Dashboard
│   ├── models.py          # Modelli Area e Property
│   ├── views.py           # Views e logica
│   └── urls.py
├── contracts/              # App Contratti
├── ownership/              # App Analytics/Ownership
├── marketplace/            # App Marketplace
├── user_settings/          # App Impostazioni Utente
├── templates/              # Template HTML
│   ├── base.html          # Template base con navbar
│   ├── dashboard/
│   ├── contracts/
│   ├── ownership/
│   ├── marketplace/
│   └── user_settings/
├── static/                 # File statici
│   ├── css/
│   │   └── style.css      # Stili principali
│   ├── icons/             # Icone (marker, phantom, etc.)
│   └── images/            # Immagini statiche
├── media/                  # Upload utenti (immagini proprietà)
├── db.sqlite3             # Database SQLite
├── manage.py              # Script di gestione Django
├── populate_db.py         # Script per popolare il DB
├── add_orders.py          # Script per aggiungere ordini
└── requirements.txt       # Dipendenze Python
```

## 🎨 Caratteristiche del Design

### Palette Colori
- **Primario**: Viola (#8a5cf6)
- **Secondario**: Rosa/Fucsia
- **Background Chiaro**: Gradiente viola pastello
- **Background Scuro**: Gradiente blu scuro (#1a1a2e → #0f0f1e)
- **Testo Chiaro**: #f3f4f6
- **Bordi Scuri**: #374151

### Componenti Stilizzati
- Navbar trasparente con bordo inferiore
- Cards con shadow e border-radius
- Tabelle con header gradiente viola
- KPI cards con colori preservati in modalità notturna
- Modal con sfondo scuro e bordi
- Bottoni con hover effects

## 🔧 Configurazione Avanzata

### Modifica Configurazioni Django

Edita `config/settings.py` per:
- Cambiare SECRET_KEY (obbligatorio per produzione!)
- Configurare database PostgreSQL o MySQL
- Aggiungere domini in ALLOWED_HOSTS
- Configurare email per notifiche

### Database di Produzione

Per passare a PostgreSQL:

1. Installa psycopg2:
```bash
pip install psycopg2-binary
```

2. Modifica `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rentshare_db',
        'USER': 'tuo_user',
        'PASSWORD': 'tua_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Gestione File Statici in Produzione

```bash
python manage.py collectstatic
```

Configura un server web (Nginx, Apache) per servire i file statici.

## 🌐 Deploy in Produzione

### Passaggi Principali:

1. **Disabilita DEBUG** in `settings.py`:
```python
DEBUG = False
ALLOWED_HOSTS = ['tuodominio.com', 'www.tuodominio.com']
```

2. **Cambia SECRET_KEY** con una chiave casuale sicura

3. **Configura un database di produzione** (PostgreSQL raccomandato)

4. **Usa un server WSGI** come Gunicorn:
```bash
pip install gunicorn
gunicorn config.wsgi:application
```

5. **Configura un reverse proxy** (Nginx o Apache)

6. **Abilita HTTPS** con certificati SSL (Let's Encrypt)

7. **Configura file statici e media** su CDN o storage separato

## 📝 Note Importanti

- Il database SQLite3 incluso contiene dati di esempio
- Le immagini delle proprietà sono in `media/properties/`
- La modalità notturna è salvata in localStorage del browser
- Gli wallet crypto sono in modalità DEMO (non connessioni reali)
- Per produzione, implementare connessioni wallet reali (vedi commenti in `marketplace.html`)

## 🔐 Sicurezza

Per produzione:
- Cambia SECRET_KEY in `settings.py`
- Usa variabili d'ambiente per credenziali sensibili
- Abilita HTTPS
- Configura CSRF e CORS correttamente
- Implementa rate limiting
- Usa database con password sicure

## 🐛 Risoluzione Problemi

### Errore: "No module named 'django'"
```bash
pip install -r requirements.txt
```

### Errore: "Port already in use"
```bash
# Cambia porta
python manage.py runserver 8001
```

### Immagini non caricate
```bash
# Verifica che la cartella media esista
python manage.py migrate
```

### Stili non applicati
```bash
# Svuota cache del browser
# Riavvia il server
python manage.py runserver
```

## 📞 Supporto

Per problemi o domande:
- Controlla la documentazione Django: https://docs.djangoproject.com/
- Verifica i log del server per errori specifici
- Controlla la console del browser per errori JavaScript

## 📄 Licenza

Questo progetto è proprietario. Tutti i diritti riservati.

## 🙏 Ringraziamenti

- Django Framework
- Leaflet.js per le mappe
- CartoDB per le tiles
- Icons8 per le icone
- MetaMask e Phantom per i loghi wallet
