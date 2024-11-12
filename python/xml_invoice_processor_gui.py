import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import DateEntry
from datetime import datetime
import xml_invoice_processor

class InvoiceProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("XML Invoice Processor")
        self.root.geometry("600x400")
        
        # Create main frame with padding
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Folder Selection
        ttk.Label(main_frame, text="Select Folder:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.folder_path = tk.StringVar()
        self.folder_entry = ttk.Entry(main_frame, textvariable=self.folder_path, width=50)
        self.folder_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_folder).grid(row=0, column=2, pady=5)
        
        # Start Date
        ttk.Label(main_frame, text="Start Date:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.start_date = DateEntry(main_frame, width=20, background='darkblue',
                                  foreground='white', borderwidth=2)
        self.start_date.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # End Date
        ttk.Label(main_frame, text="End Date:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.end_date = DateEntry(main_frame, width=20, background='darkblue',
                                foreground='white', borderwidth=2)
        self.end_date.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Process Button
        self.process_button = ttk.Button(main_frame, text="Process Invoices", 
                                       command=self.process_invoices)
        self.process_button.grid(row=3, column=0, columnspan=3, pady=20)
        
        # Status Label
        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.grid(row=4, column=0, columnspan=3, pady=5)
        
        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, length=400, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, pady=5)
        
    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        self.folder_path.set(folder_selected)
        
    def process_invoices(self):
        # Get values
        folder = self.folder_path.get()
        start_date = self.start_date.get_date().strftime('%Y-%m-%d')
        end_date = self.end_date.get_date().strftime('%Y-%m-%d')
        
        if not folder:
            self.status_label.config(text="Please select a folder first!", foreground="red")
            return
            
        # Update UI
        self.status_label.config(text="Processing...", foreground="blue")
        self.process_button.config(state='disabled')
        self.progress.start()
        
        # Schedule the processing to run in a separate thread
        self.root.after(100, lambda: self.run_processing(folder, start_date, end_date))
        
    def run_processing(self, folder, start_date, end_date):
        try:
            # Call the main function from your existing script
            xml_invoice_processor.main(folder, start_date, end_date)
            self.status_label.config(
                text="Processing completed! Output file: fattura-pa-summary.xlsx",
                foreground="green"
            )
        except Exception as e:
            self.status_label.config(
                text=f"Error: {str(e)}",
                foreground="red"
            )
        finally:
            # Reset UI
            self.progress.stop()
            self.process_button.config(state='normal')

def main():
    root = tk.Tk()
    app = InvoiceProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()