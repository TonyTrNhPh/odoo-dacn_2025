from odoo import models, fields

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Information'

    name = fields.Char(string='Họ và Tên', required=True)
    age = fields.Integer(string='Tuổi')
    gender = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác')
    ], string='Giới tính', required=True)
    phone = fields.Char(string='Số điện thoại')
    address = fields.Text(string='Địa chỉ')
