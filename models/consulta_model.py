from database import db
from datetime import datetime

class Consulta(db.Model):
    __tablename__ = "consultas"
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    diagnostico = db.Column(db.String(500), nullable=False)
    tratamiento = db.Column(db.String(500), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    
    medico = db.relationship('Medico', back_populates='consultas')
    paciente = db.relationship('Paciente', back_populates='consultas')
    
    def __init__(self, medico_id, paciente_id, fecha, diagnostico, tratamiento):
        self.medico_id = medico_id
        self.paciente_id = paciente_id
        self.fecha = fecha
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento

    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod
    def get_all():
        return Consulta.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Consulta.query.get(id)
    
    def update(self, medico_id=None, paciente_id=None, fecha=None, diagnostico=None, tratamiento=None):
        if medico_id:
            self.medico_id = medico_id
        if paciente_id:
            self.paciente_id = paciente_id
        if fecha:
            self.fecha = fecha
        if diagnostico:
            self.diagnostico = diagnostico
        if tratamiento:
            self.tratamiento = tratamiento
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    # EXTRA: Filtro de consultas por fecha
    @staticmethod
    def filtrar_por_fecha(fecha_inicio, fecha_fin):
        return Consulta.query.filter(Consulta.fecha >= fecha_inicio, Consulta.fecha <= fecha_fin).all()