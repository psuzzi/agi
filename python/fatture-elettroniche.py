import requests
import xml.etree.ElementTree as ET
from zeep import Client
from datetime import datetime
import base64
import json

class SDIClient:
    def __init__(self, certificato_path, password, ambiente="test"):
        self.certificato_path = certificato_path
        self.password = password
        
        # URL dei servizi (esempio)
        self.urls = {
            "test": "https://servizi.fatturapa.it/test/ServizioSDI",
            "prod": "https://servizi.fatturapa.it/ServizioSDI"
        }
        
        self.url = self.urls[ambiente]
        self.setup_client()
    
    def setup_client(self):
        """Configura il client SOAP con certificato"""
        self.client = Client(
            self.url + '?wsdl',
            transport=self._get_transport_with_cert()
        )
    
    def _get_transport_with_cert(self):
        """Configura il trasporto con il certificato"""
        session = requests.Session()
        session.cert = (self.certificato_path, self.password)
        return zeep.Transport(session=session)
    
    def scarica_fatture(self, data_inizio, data_fine):
        """
        Scarica le fatture per il periodo specificato
        
        Args:
            data_inizio (datetime): Data inizio periodo
            data_fine (datetime): Data fine periodo
            
        Returns:
            list: Lista di fatture in formato XML
        """
        try:
            # Parametri della richiesta
            params = {
                "DataInizio": data_inizio.isoformat(),
                "DataFine": data_fine.isoformat()
            }
            
            # Chiamata al servizio
            response = self.client.service.RicercaFatture(**params)
            
            fatture = []
            for fattura_response in response:
                # Decodifica il contenuto XML della fattura
                xml_content = base64.b64decode(fattura_response.File).decode('utf-8')
                fatture.append(xml_content)
            
            return fatture
            
        except Exception as e:
            print(f"Errore durante lo scaricamento delle fatture: {str(e)}")
            raise

    def parse_fattura(self, xml_content):
        """
        Parsing base di una fattura XML
        
        Args:
            xml_content (str): Contenuto XML della fattura
            
        Returns:
            dict: Dati principali della fattura
        """
        try:
            root = ET.fromstring(xml_content)
            
            # Namespace della fattura elettronica
            ns = {'p': 'http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2'}
            
            # Estrai informazioni base
            dati = {
                'numero': root.find('.//p:NumeroFattura', ns).text,
                'data': root.find('.//p:Data', ns).text,
                'importo_totale': float(root.find('.//p:ImportoTotaleDocumento', ns).text),
                'partita_iva': root.find('.//p:IdCodice', ns).text
            }
            
            return dati
            
        except Exception as e:
            print(f"Errore durante il parsing della fattura: {str(e)}")
            raise

# Esempio di utilizzo
if __name__ == "__main__":
    # Configurazione
    cert_path = "path/al/tuo/certificato.p12"
    password = "password_certificato"
    
    # Inizializzazione client
    client = SDIClient(cert_path, password, ambiente="test")
    
    # Date di esempio
    data_inizio = datetime(2024, 1, 1)
    data_fine = datetime(2024, 3, 31)
    
    # Scarica fatture
    fatture = client.scarica_fatture(data_inizio, data_fine)
    
    # Processa le fatture
    for fattura_xml in fatture:
        dati_fattura = client.parse_fattura(fattura_xml)
        print(json.dumps(dati_fattura, indent=2))
