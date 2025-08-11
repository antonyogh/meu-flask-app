from flask import Flask, jsonify, render_template
import requests
import threading
import time

app = Flask(__name__, template_folder='templates')

# Dados em cache para evitar chamadas excessivas à API
cached_data = {
    'prices': [],
    'gainers': [],
    'last_updated': 0
}

# Lista de símbolos de criptomoedas para exibir no topo
main_symbols = [
    'BTCUSDT',
    'ETHUSDT',
    'BNBUSDT',
    'SOLUSDT',
    'XRPUSDT',
    'ADAUSDT',
    'DOGEUSDT',
    'SHIBUSDT',
    'DOTUSDT',
    'LTCUSDT',
    'SUIUSDT',
    'DIAUSDT',
]

def fetch_crypto_data():
    """Busca dados da API da Binance e armazena em cache."""
    try:
        response = requests.get('https://api.binance.com/api/v3/ticker/24hr')
        response.raise_for_status()  # Lança um erro se a resposta não for 200 OK
        data = response.json()

        # Filtra e formata os dados das principais criptomoedas
        main_crypto_prices = [
            {
                'symbol': ticker['symbol'],
                'price': f"{float(ticker['lastPrice']):.2f}",
                'priceChangePercent': f"{float(ticker['priceChangePercent']):.2f}"
            }
            for ticker in data if ticker['symbol'] in main_symbols
        ]

        # Encontra os 5 maiores ganhadores com base na porcentagem de mudança em 24h
        top_gainers = sorted(
            [
                {
                    'symbol': ticker['symbol'],
                    'price': f"{float(ticker['lastPrice']):.2f}",
                    'priceChangePercent': f"{float(ticker['priceChangePercent']):.2f}"
                }
                for ticker in data if float(ticker['priceChangePercent']) > 0
            ],
            key=lambda x: float(x['priceChangePercent']),
            reverse=True
        )[:10]

        cached_data['prices'] = main_crypto_prices
        cached_data['gainers'] = top_gainers
        cached_data['last_updated'] = time.time()
        print("Dados da Binance atualizados com sucesso.")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar dados da Binance: {e}")

# Inicia a busca inicial e configura o agendamento em um thread separado
def schedule_data_fetch():
    fetch_crypto_data()
    # Chama a função novamente a cada 30 segundos
    threading.Timer(60.0, schedule_data_fetch,).start()

schedule_data_fetch()

@app.route('/')
def index():
    """Renderiza a página principal."""
    return render_template('index.html')

@app.route('/api/prices')
def api_prices():
    """Endpoint da API que retorna os dados de cotação em JSON."""
    return jsonify(cached_data)

if __name__ == '__main__':
    # Define o host para '0.0.0.0' para ser acessível externamente
    app.run(host='0.0.0.0', port=5000)
