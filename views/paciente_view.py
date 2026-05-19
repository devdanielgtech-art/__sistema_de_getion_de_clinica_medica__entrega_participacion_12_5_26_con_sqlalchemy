from flask import render_template

def list(pacientes):
    return render_template('pacientes/index.html', pacientes=pacientes)

def create():
    return render_template('pacientes/create.html')

def edit(paciente):
    return render_template('pacientes/edit.html', paciente=paciente)

# EXTRA: Historial médico del paciente
def historial(paciente, consultas):
    return render_template('pacientes/historial.html', paciente=paciente, consultas=consultas)