from database import db
from datetime import datetime

class Cita(db.Model):
    __tablename__ = "citas"
    
    id = db.Column(db.Integer, primary_key=True)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    motivo = db.Column(db.String(300), nullable=False)
    estado = db.Column(db.String(20), default="pendiente")
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    
    medico = db.relationship('Medico', back_populates='citas')
    paciente = db.relationship('Paciente', back_populates='citas')
    
    def __init__(self, medico_id, paciente_id, fecha_hora, motivo, estado="pendiente"):
        self.medico_id = medico_id
        self.paciente_id = paciente_id
        self.fecha_hora = fecha_hora
        self.motivo = motivo
        self.estado = estado

    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod
    def get_all():
        return Cita.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Cita.query.get(id)
    
    def update(self, medico_id=None, paciente_id=None, fecha_hora=None, motivo=None, estado=None):
        if medico_id:
            self.medico_id = medico_id
        if paciente_id:
            self.paciente_id = paciente_id
        if fecha_hora:
            self.fecha_hora = fecha_hora
        if motivo:
            self.motivo = motivo
        if estado:
            self.estado = estado
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    # EXTRA: Agenda de citas
    @staticmethod
    def get_agenda(medico_id=None, fecha=None):
        query = Cita.query
        if medico_id:
            query = query.filter(Cita.medico_id == medico_id)
        if fecha:
            fecha_inicio = datetime.combine(fecha, datetime.min.time())
            fecha_fin = datetime.combine(fecha, datetime.max.time())
            query = query.filter(Cita.fecha_hora >= fecha_inicio, Cita.fecha_hora <= fecha_fin)
        return query.all()