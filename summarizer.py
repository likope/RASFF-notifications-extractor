import requests

def build_prompt(notification: dict) -> str:
    """Build a prompt for the summarization of a notification."""
    prompt = f"""Sei un esperto di sicurezza alimentare. Analizza questa notifica RASFF e produci un brief operativo in italiano.

REGOLE:
- Basati SOLO sui dati forniti. Non inventare informazioni non presenti.
- Se non hai abbastanza dati per una sezione, scrivi "Dati insufficienti."
- Massimo 5 righe per sezione.
- Rispondi esclusivamente in italiano.

DATI NOTIFICA:
- Riferimento: {notification['reference']}
- Oggetto: {notification['subject']}
- Categoria prodotto: {notification['productCategory']['description']}
- Classificazione: {notification['notificationClassification']['description']}
- Rischio: {notification['riskDecision']['description']}
- Paese notificante: {notification['notifyingCountry']['organizationName']}
- Paesi di origine: {', '.join(c['isoCode'] for c in notification['originCountries'])}

BRIEF OPERATIVO(in italiano):
1. Cosa è successo
2. Chi è impattato
3. Azione consigliata per il consulente

Solo in italiano"""
    return prompt


def call_ollama(prompt: str):
    """Call the Ollama API with the specified prompt and return the response."""
    try:
        response = requests.post("http://localhost:11434/api/generate",
                                 json={"model": "deepseek-r1:14b", 
                                       "prompt": prompt, 
                                       "system": "Rispondi SEMPRE e SOLO in italiano.",
                                       "stream": False,
                                       "options": {"temperature": 0.1}},
                                       timeout=300)
        response.raise_for_status()
        return response.json().get("response", "")  # Return the response text from the API
    except requests.exceptions.RequestException as e:
        print(f"Error during the request: {e}")
        return "Errore durante la richiesta all'API di Ollama."
    
def summarize_notification(notification: dict) -> str:
    """Summarize a notification using the Ollama API."""
    prompt = build_prompt(notification)
    return call_ollama(prompt)


if __name__ == "__main__":
    from fetcher import fetch_notifications

    print("=== Test Summarizer RASFF ===\n")
    notifications = fetch_notifications(max_pages=1, per_page=5)
    print(f"Fetched {len(notifications)} notifications\n")
    
    for n in notifications:
        print(f"  [{n['reference']}] {n['subject']}")
        summary = summarize_notification(n)
        print("Summary:")
        print(summary)
        print()