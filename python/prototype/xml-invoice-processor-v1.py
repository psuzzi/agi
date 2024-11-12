import os
import xml.etree.ElementTree as ET
import datetime
from dataclasses import dataclass
from typing import List
import csv
from pathlib import Path

@dataclass
class Fattura:
    cedente_id_fiscale: str
    cedente_denominazione: str
    cedente_regime_fiscale: str
    divisa: str
    data: datetime.date
    numero: str
    data_scadenza_pagamento: datetime.date
    importo_pagamento: float

@dataclass
class TotaleFattureCedente:
    cedente_id_fiscale: str
    cedente_denominazione: str
    totale_pagamenti: float

def parse_date(date_str: str) -> datetime.date:
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

def process_xml_file(file_path: str) -> Fattura:
    """Process a single XML file and return a Fattura object."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Handle namespace
    ns = {'p': 'http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2'}
    
    # Extract Cedente information
    cedente = root.find('.//p:CedentePrestatore', ns)
    id_fiscale = cedente.find('.//p:IdFiscaleIVA/p:IdCodice', ns).text
    denominazione = cedente.find('.//p:Anagrafica/p:Denominazione', ns).text
    regime_fiscale = cedente.find('.//p:RegimeFiscale', ns).text
    
    # Extract DatiGeneraliDocumento information
    dati_generali = root.find('.//p:DatiGeneraliDocumento', ns)
    divisa = dati_generali.find('p:Divisa', ns).text
    data = parse_date(dati_generali.find('p:Data', ns).text)
    numero = dati_generali.find('p:Numero', ns).text
    
    # Extract DatiPagamento information
    dettaglio_pagamento = root.find('.//p:DettaglioPagamento', ns)
    data_scadenza = parse_date(dettaglio_pagamento.find('p:DataScadenzaPagamento', ns).text)
    importo = float(dettaglio_pagamento.find('p:ImportoPagamento', ns).text)
    
    return Fattura(
        cedente_id_fiscale=id_fiscale,
        cedente_denominazione=denominazione,
        cedente_regime_fiscale=regime_fiscale,
        divisa=divisa,
        data=data,
        numero=numero,
        data_scadenza_pagamento=data_scadenza,
        importo_pagamento=importo
    )

def process_folder(folder_path: str, start_date: datetime.date, end_date: datetime.date) -> List[Fattura]:
    """Process all XML files in the folder and subfolders."""
    fatture = []
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.xml'):
                file_path = os.path.join(root, file)
                try:
                    # Quick check if it's a FatturaElettronica file
                    tree = ET.parse(file_path)
                    root_elem = tree.getroot()
                    if 'FatturaElettronica' not in root_elem.tag:
                        continue
                        
                    fattura = process_xml_file(file_path)
                    
                    # Check if the invoice date is within the specified range
                    if start_date <= fattura.data <= end_date:
                        fatture.append(fattura)
                        
                except (ET.ParseError, AttributeError, ValueError) as e:
                    print(f"Error processing file {file_path}: {str(e)}")
                    continue
    
    return fatture

def aggregate_by_cedente(fatture: List[Fattura]) -> List[TotaleFattureCedente]:
    """Aggregate fatture by cedente and calculate totals."""
    totals = {}
    
    for fattura in fatture:
        key = (fattura.cedente_id_fiscale, fattura.cedente_denominazione)
        if key not in totals:
            totals[key] = 0
        totals[key] += fattura.importo_pagamento
    
    return [
        TotaleFattureCedente(
            cedente_id_fiscale=id_fiscale,
            cedente_denominazione=denominazione,
            totale_pagamenti=total
        )
        for (id_fiscale, denominazione), total in totals.items()
    ]

def write_csv(totali: List[TotaleFattureCedente], output_file: str):
    """Write the aggregated data to a CSV file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Cedente.IdFiscaleIVA', 'Cedente.Anagrafica.Denominazione', 'DatiPagamento'])
        
        for totale in totali:
            writer.writerow([
                totale.cedente_id_fiscale,
                totale.cedente_denominazione,
                f"{totale.totale_pagamenti:.2f}"
            ])

def main(folder_path: str, start_date_str: str, end_date_str: str):
    """Main function to process invoices and generate CSV."""
    # Convert date strings to date objects
    start_date = parse_date(start_date_str)
    end_date = parse_date(end_date_str)
    
    # Process all files
    fatture = process_folder(folder_path, start_date, end_date)
    
    # Aggregate by cedente
    totali = aggregate_by_cedente(fatture)
    
    # Write output CSV
    output_file = "fattura-pa-summary.csv"
    write_csv(totali, output_file)
    print(f"Processed {len(fatture)} invoices")
    print(f"Generated summary for {len(totali)} suppliers in {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python script.py <folder_path> <start_date> <end_date>")
        print("Dates should be in YYYY-MM-DD format")
        sys.exit(1)
        
    main(sys.argv[1], sys.argv[2], sys.argv[3])
