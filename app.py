import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
from datetime import datetime, timedelta

class EtiquetaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Etiquetas")
        self.datos_temp = []
        
        tk.Label(root, text="Fecha de Empaque (DD-MM-YYYY):").grid(row=0, column=0)
        self.fecha_empaque_entry = tk.Entry(root)
        self.fecha_empaque_entry.grid(row=0, column=1)
        
        tk.Label(root, text="Número de Lote:").grid(row=1, column=0)
        self.lote_entry = tk.Entry(root)
        self.lote_entry.grid(row=1, column=1)
        
        tk.Label(root, text="Peso (g):").grid(row=2, column=0)
        self.peso_entry = tk.Entry(root)
        self.peso_entry.grid(row=2, column=1)
        
        tk.Label(root, text="Cantidad:").grid(row=3, column=0)
        self.cantidad_entry = tk.Entry(root)
        self.cantidad_entry.grid(row=3, column=1)
        
        tk.Button(root, text="Agregar", command=self.agregar_dato).grid(row=4, columnspan=2)
        
        self.resumen_label = tk.Label(root, text="")
        self.resumen_label.grid(row=5, columnspan=2)
        
        tk.Button(root, text="Generar Etiquetas", command=self.confirmar_datos).grid(row=6, columnspan=2)
    
    def agregar_dato(self):
        try:
            peso = int(self.peso_entry.get())
            cantidad = int(self.cantidad_entry.get())
            self.datos_temp.append((peso, cantidad))
            self.actualizar_resumen()
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
    
    def actualizar_resumen(self):
        texto = "Resumen de etiquetas:\n"
        for i, (peso, cantidad) in enumerate(self.datos_temp):
            texto += f"{i+1}. Peso: {peso}g - Cantidad: {cantidad}\n"
        self.resumen_label.config(text=texto)
    
    def confirmar_datos(self):
        fecha_empaque = self.fecha_empaque_entry.get()
        lote = self.lote_entry.get()
        try:
            datetime.strptime(fecha_empaque, "%d-%m-%Y")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido.")
            return
        
        etiquetas = []
        for peso, cantidad in self.datos_temp:
            for _ in range(cantidad):
                etiquetas.append({"fecha_empaque": fecha_empaque, "lote": lote, "peso": peso})
        
        self.generar_etiquetas(etiquetas)
    
    def generar_etiquetas(self, datos_etiquetas, archivo_salida="etiquetas.pdf"):
        pdf = FPDF('P', 'mm', 'Letter')
        pdf.set_auto_page_break(auto=True, margin=10)
        pdf.set_font("Arial", style="B", size=10)
        pdf.add_page()
        
        cols = 4
        rows = 5
        cell_width = 48
        cell_height = 40
        margin_x = 10
        margin_y = 10
        
        count = 0
        for datos in datos_etiquetas:
            if count % (cols * rows) == 0 and count != 0:
                pdf.add_page()
            
            fecha_empaque = datetime.strptime(datos['fecha_empaque'], "%d-%m-%Y")
            fecha_vencimiento = fecha_empaque + timedelta(days=30)
            empresa = "Carnes San Agustín"
            
            col = count % cols
            row = (count // cols) % rows
            x = margin_x + col * cell_width
            y = margin_y + row * cell_height
            
            pdf.set_xy(x, y)
            pdf.set_line_width(1.1)
            pdf.multi_cell(cell_width, 6, f"Empresa: {empresa}\nFecha Empaque: {fecha_empaque.strftime('%d-%m-%Y')}\nFecha Vencimiento: {fecha_vencimiento.strftime('%d-%m-%Y')}\nLote: {datos['lote']}\nPeso: {datos['peso']}g", border=1, align='C')
            count += 1
        
        pdf.output(archivo_salida)
        messagebox.showinfo("Éxito", f"Etiquetas generadas en {archivo_salida}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EtiquetaApp(root)
    root.mainloop()
