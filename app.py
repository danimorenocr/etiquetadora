from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import io
from datetime import datetime, timedelta

app = Flask(__name__)

class PDF(FPDF):
    def header(self):
        pass  # Elimina cualquier título o margen extra

def generate_pdf(etiquetas):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=5)  # Margen inferior reducido
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    col_width = 62   # Ancho de cada etiqueta
    row_height = 25  # Altura de cada etiqueta
    etiquetas_por_fila = 3  # 3 columnas
    etiquetas_por_pagina = 27  # 9 filas * 3 columnas

    count = 0
    x_start = 8  # Margen izquierdo
    y_start = 10  # **Margen superior ajustado**

    for idx, et in enumerate(etiquetas):
        col = count % etiquetas_por_fila
        row = (count // etiquetas_por_fila) % 9  # 7 filas por página

        x = x_start + col * (col_width + 5)  # Espaciado horizontal
        y = y_start + row * (row_height + 5)  # **Posición vertical corregida**

        pdf.set_xy(x, y)  # Posiciona correctamente la etiqueta
        pdf.multi_cell(col_width, 5, f"Carnes San Agustin\nEmpaque: {et['fecha']}\n"
                                      f"Vence: {et['vencimiento']}\nLote: {et['lote']}\n"
                                      f"Peso: {et['peso']}g", border=1, align="C")

        count += 1

        if count % etiquetas_por_pagina == 0:
            pdf.add_page()  # Nueva página cada 21 etiquetas

    # Guardar en archivo
    pdf_filename = "etiquetas_temp.pdf"
    pdf.output(pdf_filename)

    return pdf_filename


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        fecha_empaque = request.form['fecha_empaque']
        lote = request.form['lote']
        etiquetas = []
        
        try:
            fecha_dt = datetime.strptime(fecha_empaque, "%d-%m-%Y")
            fecha_vencimiento = fecha_dt + timedelta(days=30)
        except ValueError:
            return "Error: Formato de fecha incorrecto. Use DD-MM-YYYY"
        
        for i in range(1, 6):
            peso = request.form.get(f'peso_{i}')
            cantidad = request.form.get(f'cantidad_{i}')
            if peso and cantidad:
                for _ in range(int(cantidad)):
                    etiquetas.append({
                        'fecha': fecha_empaque,
                        'vencimiento': fecha_vencimiento.strftime('%d-%m-%Y'),
                        'lote': lote,
                        'peso': peso
                    })
        
        pdf_filename = generate_pdf(etiquetas)
        
        return send_file(
            pdf_filename,
            as_attachment=True,
            download_name="etiquetas.pdf",
            mimetype="application/pdf"
        )
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
