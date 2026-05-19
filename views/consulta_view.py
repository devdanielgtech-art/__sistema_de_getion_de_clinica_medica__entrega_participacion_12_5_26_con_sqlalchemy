from flask import render_template

def list(consultas):
    return render_template('consultas/index.html', consultas=consultas)

def create(medicos, pacientes):
    return render_template('consultas/create.html', medicos=medicos, pacientes=pacientes)

def edit(consulta, medicos, pacientes):
    return render_template('consultas/edit.html', consulta=consulta, medicos=medicos, pacientes=pacientes)

# EXTRA: Filtro de consultas por fecha
def filtrar(consultas, fecha_inicio, fecha_fin):
    return render_template('consultas/filtrar.html', consultas=consultas, 
                          fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)