from flask import Flask, render_template, jsonify, request

import requests

import traceback

import urllib.parse

from flask_swagger_ui import get_swaggerui_blueprint
from flasgger import Swagger

from utils.config import config, env
from utils.rest_client import RestClient
from model import atleti

app = Flask(__name__)

swagger = Swagger(app)

# Inizializza il client REST con parametri dinamici:
mra_rest_api = RestClient(
    base_url = config[env].REST_API_URL,
    verify_server_sslcert = False
    )

# -----------------------------------------------------------------------------

# Configurazione Swagger-UI (generatore automatico documentaz. API):
SWAGGER_DOC_ENDPOINT = "/api/docs"         # URL accesso documentaz. in formato Swagger
SWAGGER_JSONFILE = "/static/swagger.json"  # Percorso al file Swagger JSON

# Inizializzazione Swagger-UI:
swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_DOC_ENDPOINT, SWAGGER_JSONFILE)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_DOC_ENDPOINT)


# -----------------------------------------------------------------------------
# --- Definizione Frontend web-site Endpoint(s)
# -----------------------------------------------------------------------------

@app.route("/mra-web/atleti")
def pg_atleti():
    # DEBUG: print(api_base_url)
    try:
        # Lista anagrafiche Atleti:
        qry_lista_atleti = "/api/mra/v1.0.0/atleti"
        lista_atleti, resp_status_code = mra_rest_api.get_data(rest_query = qry_lista_atleti)
        # DEBUG: print(lista_atleti)

        return render_template(
            "mra/mra_atleti.html",
            atleti = lista_atleti)

    except Exception as e:
        return f"Errore durante la richiesta: {e}", 500

# -----------------------------------------------------------------------------

@app.route("/mra-web/atleti/<id_atleta>/tipologie-esercizi-svolti")
def pg_tipologie_esercizi_svolti(id_atleta):

    try:
        # Anagrafica atleta:
        qry_atleta = f"/api/mra/v1.0.0/atleti/{id_atleta}"
        atleta, resp_status_code = mra_rest_api.get_data(rest_query = qry_atleta)
        # DEBUG: print(atleta)

        # Lista tipologie esercizi svolti:
        qry_lista_tipologie = f"/api/mra/v1.0.0/atleti/{id_atleta}/tipologie-esercizi-svolti"
        lista_tipologie, resp_status_code = mra_rest_api.get_data(rest_query = qry_lista_tipologie)
        # DEBUG: print(lista_tipologie)

        return render_template(
            "mra/mra_tipologie_esercizi_svolti.html",
            id_atleta = id_atleta, atleta = atleta,
            tipologie = lista_tipologie)

    except Exception as e:
        return f"Errore durante la richiesta: {e}", 500

# -----------------------------------------------------------------------------

@app.route("/mra-web/atleti/<id_atleta>/tipologie-esercizi-svolti/<id_tipologia>/sessioni")
def pg_sessioni(id_atleta, id_tipologia):

    try:
        # Anagrafica atleta:
        qry_atleta = f"/api/mra/v1.0.0/atleti/{id_atleta}"
        atleta, resp_status_code = mra_rest_api.get_data(rest_query = qry_atleta)
        # DEBUG: print(atleta)

        # Tipologia esercizi svolti:
        qry_tipologia = f"/api/mra/v1.0.0/atleti/{id_atleta}/tipologie-esercizi-svolti/{id_tipologia}"
        tipologia, resp_status_code = mra_rest_api.get_data(rest_query = qry_tipologia)
        # DEBUG: print(tipologia)

        # Lista sessioni:
        qry_lista_sessioni = f"/api/mra/v1.0.0/atleti/{id_atleta}/tipologie-esercizi-svolti/{id_tipologia}/sessioni"
        lista_sessioni, resp_status_code = mra_rest_api.get_data(rest_query = qry_lista_sessioni)
        # DEBUG: print(lista_sessioni)

        return render_template(
            "mra/mra_sessioni.html",
            id_atleta = id_atleta, atleta = atleta,
            id_tipologia = id_tipologia, tipologia = tipologia,
            sessioni = lista_sessioni)

    except Exception as e:
        return f"Errore durante la richiesta: {e}", 500

# -----------------------------------------------------------------------------

@app.route("/mra-web/atleti/<id_atleta>/tipologie-esercizi-svolti/<id_tipologia>/sessioni/<id_sessione_encoded>")
def pg_rilevazioni(id_atleta, id_tipologia, id_sessione_encoded):

    try:
        # Anagrafica atleta:
        qry_atleta = f"/api/mra/v1.0.0/atleti/{id_atleta}"
        atleta, resp_status_code = mra_rest_api.get_data(rest_query = qry_atleta)
        # DEBUG: print(atleta)

        # Tipologia esercizi svolti:
        qry_tipologia = f"/api/mra/v1.0.0/atleti/{id_atleta}/tipologie-esercizi-svolti/{id_tipologia}"
        tipologia, resp_status_code = mra_rest_api.get_data(rest_query = qry_tipologia)
        # DEBUG: print(tipologia)

        # Sessione:
        qry_sessione = f"/api/mra/v1.0.0/atleti/{id_atleta}/tipologie-esercizi-svolti/{id_tipologia}/sessioni/{id_sessione_encoded}"
        sessione, resp_status_code = mra_rest_api.get_data(rest_query = qry_sessione)
        # DEBUG: print(sessione)

        # Lista rilevazioni:
        qry_lista_rilevazioni = f"/api/mra/v1.0.0/atleti/{id_atleta}/tipologie-esercizi-svolti/{id_tipologia}/sessioni/{id_sessione_encoded}/rilevazioni"
        lista_rilevazioni, resp_status_code = mra_rest_api.get_data(rest_query = qry_lista_rilevazioni)
        # DEBUG: print(rilevazioni)

        return render_template(
            "mra/mra_rilevazioni.html",
            id_atleta = id_atleta, atleta = atleta,
            id_tipologia = id_tipologia, tipologia = tipologia,
            id_sessione_encoded = id_sessione_encoded, sessione = sessione,
            rilevazioni = lista_rilevazioni)

    except Exception as e:
        return f"Errore durante la richiesta: {e}", 500


#==============================================================================

# @app.route('/lista_atleti')
# def pg_lista_atleti():
#     #atleti = atleti[0]
#     return render_template("lista_atleti.html", atleti=atleti)

# # -----------------------------------------------------------------------------

# @app.route('/')
# def pg_home():
#     #atleti = atleti[0]
#     return render_template("index.html", atleti=atleti)
#     #return "LISTA DEGLI ATLETI"

# # -----------------------------------------------------------------------------

# @app.route('/test01')
# def pg_test01():
#     return render_template("test01.html", atleti=atleti)

# # -----------------------------------------------------------------------------

# @app.route('/esercizi_atleta/<int:index_atleta>')
# def pg_esercizi_atleta(index_atleta):
#     return render_template("indax.html", atleta=atleti[index_atleta])
#     #return "LISTA DEGLI ESERCIZI PER SINGOLO ATLETA"

# # -----------------------------------------------------------------------------

# # paginaWeb_datiTEST_OK.html
# @app.route('/test_database_01')
# def pg_test_database_01():
#     return render_template("paginaWeb_datiTEST_OK.html", env=env, cfg=config)

# # -----------------------------------------------------------------------------

# # http://127.0.0.1:5000/conteggio_pulsanti_per_tipologia_esercizio?id=111
# @app.route('/conteggio_pulsanti_per_tipologia_esercizio')
# def pg_conteggio_pulsanti_per_tipologia_esercizio():
#     return render_template("count_pulsanti.html")

# # -----------------------------------------------------------------------------

# @app.route('/catalogo_atleti', methods=['GET'])
# def pg_catalogo_atleti():
#     """
#     Recupera la lista degli atleti mediante apposita API
#     """
#     try:
#         target_template = "index.html"
#         data, status_code = main_database_rest_client.get_data("/mra/api/atleti", verify_server_sslcert=False)

#         if status_code == 200:
#             # Se la richiesta è OK, popola la lista degli atleti
#             atleti_list = [{"id": atleta_id, "nome": atleta_info.get("nickname", "Sconosciuto")} for atleta_id, atleta_info in data.items()]
#             return render_template(target_template, atleti=atleti_list, error_code=200)

#         elif 400 <= status_code < 500:
#             # Se l'errore è 40X (es. 404 Not Found)
#             return render_template(target_template, atleti=[], error_code=status_code)

#         else:
#             # Se l'errore è 50X o altro errore grave
#             return render_template(target_template, atleti=[], error_code=500)

#     except Exception as e:
#         print(f"❌ Errore imprevisto: {e}")
#         return render_template(target_template, atleti=[], error_code=500)

#     return render_template(target_template, atleti=atleti_list)


# # -----------------------------------------------------------------------------
# # --- Definizione Backend API(s)
# # -----------------------------------------------------------------------------

# @app.route('/api/atleti', methods=['GET'])
# def pg_get_atleti():
#     """
#     Ritorna la lista completa di tutti gli Atleti - Returns all Athletes full list
#     ---
#     responses:
#       200:
#         description: "Atleta trovato con successo (lista con almeno un elemento)"
#       404:
#         description: "Nessun Atleta trovato, lista vuota"
#         examples:
#           application/json:
#             { "error": "Nessun atleta trovato" }
#       500:
#         description: Errore interno del server
#         examples:
#           application/json:
#             { "error": "Errore interno del server, riprovare più tardi" }
#     """
#     try:
#         ref = db.reference("/tempiDiReazione/utenti")
#         get_reply = ref.get()

#         # Se il database non contiene atleti, restituisci 404
#         if not get_reply:
#             return jsonify({"error": "Nessun atleta trovato"}), 404

#         return jsonify(get_reply), 200

#     except Exception as e:
#         return jsonify({"error": "Errore interno del server, riprovare più tardi"}), 500
#     # return f"config[env].MAIN_DATABASE_URL: {config[env].MAIN_DATABASE_URL} - config[env].MAIN_DATABASE_CREDENTIALS: {config[env].MAIN_DATABASE_CREDENTIALS}"

# # -----------------------------------------------------------------------------

# @app.route('/api/atleti/<string:id_atleta>', methods=['GET'])
# def pg_get_atleta_by_id(id_atleta):
#     """
#     Ottiene i dettagli di un atleta specifico per ID
#     ---
#     parameters:
#       - name: id_atleta
#         in: path
#         type: string
#         required: true
#         description: "L'ID univoco dell'atleta da recuperare"
#         example: "1"
#     responses:
#       200:
#         description: "Atleta trovato con successo (risposta con dati informativi)"
#       404:
#         description: "Atleta non trovato"
#         examples:
#           application/json:
#             { "error": "Atleta non trovato" }
#       500:
#         description: "Errore interno del server"
#         examples:
#           application/json:
#             { "error": "Errore interno del server, riprovare più tardi" }
#     """
#     try:
#         ref = db.reference(f"/tempiDiReazione/utenti/{id_atleta}")
#         get_reply = ref.get()
#         if not get_reply:
#             return jsonify({"error": "Atleta non trovato"}), 404
#         return jsonify(get_reply), 200
#     except Exception:
#         return jsonify({"error": "Errore interno del server, riprovare più tardi"}), 500

# # -----------------------------------------------------------------------------

# @app.route('/api/atleti/<string:id_atleta>/esercizi', methods=['GET'])
# def pg_get_esercizi_atleta_for_atleta_by_id(id_atleta):
#     """
#     Ottiene la lista di esercizi di un atleta specifico
#     ---
#     parameters:
#       - name: id_atleta
#         in: path
#         type: string
#         required: true
#         description: "L'ID univoco dell'atleta"
#     responses:
#       200:
#         description: "Esercizi trovati con successo"
#       404:
#         description: "Nessun esercizio trovato per questo atleta"
#         examples:
#           application/json:
#             { "error": "Nessun esercizio trovato" }
#       500:
#         description: "Errore interno del server"
#         examples:
#           application/json:
#             { "error": "Errore interno del server, riprovare più tardi" }
#     """
#     try:
#         ref = db.reference(f"/tempiDiReazione/utenti/{id_atleta}/esercizi")
#         get_reply = ref.get()
#         if not get_reply:
#             return jsonify({"error": "Nessun esercizio trovato"}), 404
#         return jsonify(get_reply), 200
#     except Exception:
#         return jsonify({"error": "Errore interno del server, riprovare più tardi"}), 500

# # -----------------------------------------------------------------------------

# @app.route('/api/atleti/<string:id_atleta>/esercizi/<string:id_esercizio>', methods=['GET'])
# def pg_get_esercizio_atleta_by_id_for_atleta_by_id(id_atleta, id_esercizio):
#     """
#     Ottiene i dettagli di un esercizio specifico per un atleta
#     ---
#     parameters:
#       - name: id_atleta
#         in: path
#         type: string
#         required: true
#         description: "L'ID univoco dell'atleta"
#       - name: id_esercizio
#         in: path
#         type: string
#         required: true
#         description: "L'ID dell'esercizio dell'atleta"
#     responses:
#       200:
#         description: "Esercizio trovato con successo"
#       404:
#         description: "Esercizio non trovato per questo atleta"
#         examples:
#           application/json:
#             { "error": "Esercizio non trovato per questo atleta" }
#       500:
#         description: "Errore interno del server"
#         examples:
#           application/json:
#             { "error": "Errore interno del server, riprovare più tardi" }
#     """
#     try:
#         ref = db.reference(f"/tempiDiReazione/utenti/{id_atleta}/esercizi/{id_esercizio}")
#         get_reply = ref.get()

#         if not get_reply:
#             return jsonify({"error": "Esercizio non trovato per questo atleta"}), 404

#         return jsonify(get_reply), 200

#     except Exception:
#         return jsonify({"error": "Errore interno del server, riprovare più tardi"}), 500

# # -----------------------------------------------------------------------------

# @app.route("/api/atleti/<int:id_atleta>/esercizi/<int:id_esercizio>/sessioni/<path:id_sessione_encoded>", methods=["GET"])
# def pg_get_sessione_by_id(id_atleta, id_esercizio, id_sessione_encoded):
#     try:
#         # Decodifica del valore encoded di id_sessione ricevuto da query-string,
#         #   ad esempio da "10-3-2025_11%3A59%3A2" a "10-3-2025_11:59:2" :
#         #
#         id_sessione = urllib.parse.unquote(id_sessione_encoded)

#         ref = db.reference(f"/tempiDiReazione/utenti/{id_atleta}/esercizi/{id_esercizio}/{id_sessione}")
#         get_reply = ref.get()
#         if not get_reply:
#             return jsonify({"error": "Identificativo di Sessione non trovato per questo set esercizio/atleta"}), 404

#         return jsonify(get_reply), 200
#     except Exception:
#         return jsonify({"error": "Errore interno del server, riprovare più tardi"}), 500

# #------------------------------------------------------------------------------

# @app.route("/api/atleti/<int:id_atleta>/esercizi/<int:id_esercizio>/sessioni", methods=["GET"])
# def pg_get_sessione_by_ord(id_atleta, id_esercizio):
#     try:
#         # Recupera il valore dell'indice dalla query string (es. ?index=2), se fornito in query-string:
#         index = request.args.get("index", type = int)

#         ref = db.reference(f"/tempiDiReazione/utenti/{id_atleta}/esercizi/{id_esercizio}")
#         get_reply = ref.get()

#         if index is None:
#           if not get_reply:
#             return jsonify({"error": "Lista Sessioni non trovata per questo set esercizio/atleta"}), 404
#           else:
#             return jsonify(get_reply), 200
#         else: # Indice ricevuto da query-string:
#           if not get_reply:
#             return jsonify({"error": "Sessione non trovata ad indice inserito per questo set esercizio/atleta"}), 404
#           else:
#             keys = list(get_reply.keys())  # Conversione in list per generare struttura di ordinamento
#             if index < 0 or index >= len(keys):
#               return jsonify({"error": "Indice non valido (out of range)"}), 400
#             else:
#               key = keys[index]  # Get the indexed key
#               return jsonify({key: get_reply[key]}), 200

#     except Exception:
#         return jsonify({"error": "Errore interno del server, riprovare più tardi"}), 500

# #------------------------------------------------------------------------------

# @app.route('/api/catalogo_esercizi', methods=['GET'])
# def pg_get_tipologie_esercizi():
#     """
#     Ottiene l'elenco delle tipologie di esercizi disponibili
#     ---
#     responses:
#       200:
#         description: "Elenco delle tipologie di esercizi recuperato con successo"
#       404:
#         description: "Nessuna tipologia di esercizio trovata"
#         examples:
#           application/json:
#             { "error": "Nessuna tipologia di esercizio trovata" }
#       500:
#         description: "Errore interno del server"
#         examples:
#           application/json:
#             { "error": "Errore interno del server, riprovare più tardi" }
#     """
#     try:
#         ref = db.reference("/tempiDiReazione/tipoEsercizio")
#         get_reply = ref.get()
#         if not get_reply:
#             return jsonify({"error": "Nessuna tipologia di esercizio trovata (lista vuota)"}), 404
#         return jsonify(get_reply), 200
#     except Exception:
#         return jsonify({"error": "Errore interno del server, riprovare più tardi"}), 500

# # -----------------------------------------------------------------------------

# @app.route('/api/catalogo_esercizi/<string:id_tipologia_esercizio>', methods=['GET'])
# def pg_get_tipologia_esercizio_by_id(id_tipologia_esercizio):
#     """
#     Ottiene i dettagli di una tipologia di esercizio specifica per ID
#     ---
#     parameters:
#       - name: id_tipologia_esercizio
#         in: path
#         type: string
#         required: true
#         description: "L'ID della tipologia di esercizio"
#     responses:
#       200:
#         description: "Tipologia di esercizio trovata con successo"
#       404:
#         description: "Tipologia di esercizio non trovata"
#         examples:
#           application/json:
#             { "error": "Tipologia di esercizio non trovata" }
#       500:
#         description: "Errore interno del server"
#         examples:
#           application/json:
#             { "error": "Errore interno del server, riprovare più tardi" }
#     """
#     try:
#         ref = db.reference(f"/tempiDiReazione/tipoEsercizio/{id_tipologia_esercizio}")
#         get_reply = ref.get()
#         if not get_reply:
#             return jsonify({"error": "Tipologia di esercizio non trovata"}), 404
#         return jsonify(get_reply), 200
#     except Exception:
#         return jsonify({"error": "Errore interno del server, riprovare più tardi"}), 500

# # -----------------------------------------------------------------------------

# @app.route('/api/catalogo_esercizi/<string:id_tipologia_esercizio>/count_pulsanti', methods=['GET'])
# def pg_get_count_pulsanti_for_tipologia_esercizio_by_id(id_tipologia_esercizio):
#     """
#     Ottiene il numero totale di pulsanti richiesti per una tipologia di esercizio
#     ---
#     parameters:
#       - name: id_tipologia_esercizio
#         in: path
#         type: string
#         required: true
#         description: "L'ID della tipologia di esercizio"
#     responses:
#       200:
#         description: "Numero di pulsanti trovato con successo"
#       404:
#         description: "Tipologia di esercizio non trovata o nessun numero di pulsanti associato"
#         examples:
#           application/json:
#             { "error": "Tipologia di esercizio non trovata o nessun numero di pulsanti associato" }
#       500:
#         description: "Errore interno del server"
#         examples:
#           application/json:
#             { "error": "Errore interno del server, riprovare più tardi" }
#     """
#     try:
#         ref = db.reference(f"/tempiDiReazione/tipoEsercizio/{id_tipologia_esercizio}/sequenza/totalePulsanti")
#         get_reply = ref.get()

#         if get_reply is None:
#             return jsonify({"error": "Tipologia di esercizio non trovata o nessun numero di pulsanti associato"}), 404

#         return jsonify({"totPulsanti": get_reply}), 200

#     except Exception:
#         return jsonify({"error": "Errore interno del server, riprovare più tardi"}), 500

# # -----------------------------------------------------------------------------

# @app.route('/api/catalogo_esercizi/<string:id_tipologia_esercizio>/seq_max_tempi_reazione', methods=['GET'])
# def pg_get_seq_max_tempi_reazione_for_tipologia_esercizio_by_id(id_tipologia_esercizio):
#     """
#     Ottiene la sequenza massima dei tempi di reazione per una tipologia di esercizio
#     ---
#     parameters:
#       - name: id_tipologia_esercizio
#         in: path
#         type: string
#         required: true
#         description: "L'ID della tipologia di esercizio"
#     responses:
#       200:
#         description: "Sequenza massima dei tempi di reazione trovata con successo"
#       404:
#         description: "Tipologia di esercizio non trovata o nessuna sequenza di tempi di reazione disponibile"
#         examples:
#           application/json:
#             { "error": "Tipologia di esercizio non trovata o nessuna sequenza di tempi di reazione disponibile" }
#       500:
#         description: "Errore interno del server"
#         examples:
#           application/json:
#             { "error": "Errore interno del server, riprovare più tardi" }
#     """
#     try:
#         ref = db.reference(f"/tempiDiReazione/tipoEsercizio/{id_tipologia_esercizio}/sequenza/sequenzaTempo")
#         get_reply = ref.get()

#         if get_reply is None:
#             return jsonify({"error": "Tipologia di esercizio non trovata o nessuna sequenza di tempi di reazione disponibile"}), 404

#         return jsonify({"SaquenzaTempo": get_reply}), 200

#     except Exception:
#         return jsonify({"error": "Errore interno del server, riprovare più tardi"}), 500

# # -----------------------------------------------------------------------------

# @app.route('/api/catalogo_esercizi/<string:id_tipologia_esercizio>/seq_id_pulsanti', methods=['GET'])
# def pg_get_seq_id_pulsanti_for_tipologia_esercizio_by_id(id_tipologia_esercizio):
#     """
#     Ottiene la sequenza degli ID dei pulsanti per una tipologia di esercizio
#     ---
#     parameters:
#       - name: id_tipologia_esercizio
#         in: path
#         type: string
#         required: true
#         description: "L'ID della tipologia di esercizio"
#     responses:
#       200:
#         description: "Sequenza ID pulsanti trovata con successo"
#       404:
#         description: "Tipologia di esercizio non trovata o nessuna sequenza ID pulsanti disponibile"
#         examples:
#           application/json:
#             { "error": "Tipologia di esercizio non trovata o nessuna sequenza ID pulsanti disponibile" }
#       500:
#         description: "Errore interno del server"
#         examples:
#           application/json:
#             { "error": "Errore interno del server, riprovare più tardi" }
#     """
#     try:
#         ref = db.reference(f"/tempiDiReazione/tipoEsercizio/{id_tipologia_esercizio}/sequenza/sequenzaPulsanti")
#         get_reply = ref.get()

#         if get_reply is None:
#             return jsonify({"error": "Tipologia di esercizio non trovata o nessuna sequenza ID pulsanti disponibile"}), 404

#         return jsonify({"SequenzaPulsanti": get_reply}), 200

#     except Exception:
#         return jsonify({"error": "Errore interno del server, riprovare più tardi"}), 500

# # -----------------------------------------------------------------------------

# @app.route('/api/catalogo_esercizi/<string:id_tipologia_esercizio>/seq_tempi_pausa', methods=['GET'])
# def pg_get_seq_tempi_pausa_for_tipologia_esercizio_by_id(id_tipologia_esercizio):
#     """
#     Ottiene la sequenza dei tempi di pausa per una tipologia di esercizio
#     ---
#     parameters:
#       - name: id_tipologia_esercizio
#         in: path
#         type: string
#         required: true
#         description: "L'ID della tipologia di esercizio"
#     responses:
#       200:
#         description: "Sequenza tempi di pausa trovata con successo"
#       404:
#         description: "Tipologia di esercizio non trovata o nessuna sequenza tempi di pausa disponibile"
#         examples:
#           application/json:
#             { "error": "Tipologia di esercizio non trovata o nessuna sequenza tempi di pausa disponibile" }
#       500:
#         description: "Errore interno del server"
#         examples:
#           application/json:
#             { "error": "Errore interno del server, riprovare più tardi" }
#     """
#     try:
#         ref = db.reference(f"/tempiDiReazione/tipoEsercizio/{id_tipologia_esercizio}/sequenza/sequenzaWait")
#         get_reply = ref.get()

#         if get_reply is None:
#             return jsonify({"error": "Tipologia di esercizio non trovata o nessuna sequenza tempi di pausa disponibile"}), 404

#         return jsonify({"SequenzaWai": get_reply}), 200

#     except Exception:
#         return jsonify({"error": "Errore interno del server, riprovare più tardi"}), 500

# # -----------------------------------------------------------------------------

# # Endpoint per esposizione standard dello schema Swagger JSON
# @app.route('/swagger.json', methods=['GET'])
# def swagger_json():
#     """
#     Restituisce la documentazione Swagger JSON dell'API
#     ---
#     responses:
#       200:
#         description: "Swagger JSON generato con successo"
#       500:
#         description: "Errore interno del server durante la generazione della documentazione"
#         examples:
#           application/json:
#             { "error": "Errore interno del server, impossibile generare Swagger JSON" }
#     """
#     try:
#         return jsonify(swagger.get_apispecs()), 200
#     except Exception as e:
#         return jsonify({
#           "error": "Errore interno del server, impossibile generare Swagger JSON",
#           "exception": str(e),                 # Converts the exception message to string
#           "traceback": traceback.format_exc()  # Optional: Provides full stack trace
#           }), 500
#     #     return jsonify({"error": "Errore interno del server, impossibile generare Swagger JSON", "exception": " + Exception + "}), 500

# =============================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# =============================================================================
