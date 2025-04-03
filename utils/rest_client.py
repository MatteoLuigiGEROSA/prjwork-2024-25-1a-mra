import requests

from urllib3 import disable_warnings, exceptions

class RestClient:

    #--------------------------------------------------------------------------
    def __init__(self, base_url, verify_server_sslcert=True):
        """
        Inizializza il client REST per comunicare con API esterne.
        :param base_url: URL base del server REST (es. http://localhost:5010 o https://remote-server)
        :param verify_server_sslcert: Richiesta di verifica di validità certificato SSL del server invocato (default: True)
        """
        self.base_url = base_url.rstrip("/")  # Rimuove eventuali slash finali
        self.verify_server_sslcert = verify_server_sslcert

        self._initialize_client()

    #--------------------------------------------------------------------------
    def _initialize_client(self):
        """
        Crea una sessione HTTP persistente e imposta gli headers.
        """
        self.session = requests.Session()
        self.headers = {"User-Agent": "MyFlaskClient/1.0"}

        print(f"✅ REST-API Client inizializzato con BASE-URL: {self.base_url}.")

        if self.verify_server_sslcert:
            print(f"✅ Verifica certificato SSL del Server REST-API remoto ABILITATA.")
        else:
            # Disabilita WARNING per cerficicati-server SSL self-signed od insicuri (es.: senza CA):
            disable_warnings(exceptions.InsecureRequestWarning)
            print(f"⚠️ Verifica certificato SSL del Server REST-API remoto DISABILITATA, prestare attenzione!")

    #--------------------------------------------------------------------------
    def get_data(self, rest_query, timeout=5):
        """
        Recupera i dati dall'API REST esterna con gestione degli errori e auto-restart in caso di errore.
        :param endpoint: Endpoint specifico dell'API (es. /api/atleti)
        :param timeout: Tempo in secondi di attesa per la connessione (default: 5 sec)
        """
        api_url = f"{self.base_url}/{rest_query.lstrip('/')}"  # Costruisce l'URL finale
        print(f"  Chiamata API esterna [GET]: {api_url}")

        try:
            response = self.session.get(
                url = api_url,
                headers = self.headers, timeout = timeout,
                verify = self.verify_server_sslcert)
            response.raise_for_status()
            guaranteed_response = response.json()
            # guaranteed_response = response.json() if response.status_code == 200 else []
            return guaranteed_response, response.status_code

        except requests.exceptions.Timeout:
            print("  ⚠️ Timeout nell'accesso all'API")
            return {"error": "Timeout nella comunicazione con l'API"}, 504

        except requests.exceptions.ConnectionError:
            print("  ⚠️ Impossibile connettersi all'API")
            return {"error": "Server API non raggiungibile"}, 503

        except requests.exceptions.HTTPError as http_err:
            print(f"  ❌ Errore HTTP: {http_err}")
            return {"error": f"Errore HTTP: {http_err}"}, response.status_code

        except requests.exceptions.RequestException as req_err:
            print(f"  ❌ Errore generico nella richiesta: {req_err}")
            return {"error": "Errore imprevisto nella comunicazione con il server"}, 500

        except requests.exceptions.SSLError as ssl_err:
            print(f"  ❌ Errore SSL: {ssl_err}")
            return {"error": "Errore SSL durante la connessione al server"}, 495

        except Exception as e:
            print(f"  ❌ Errore critico non gestito: {e}")
            return {"error": "Errore interno del server"}, 500

