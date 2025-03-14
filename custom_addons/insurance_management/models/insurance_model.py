from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class ClinicPatientInsurance(models.Model):
    _name = 'clinic.patient.insurance'
    _description = 'Thông tin bảo hiểm y tế của bệnh nhân'

    # Xóa patient_id vì không cần thiết trong quan hệ một-một
    # patient_id = fields.Many2one('clinic.patient', string='Bệnh nhân', required=True, ondelete='cascade')
    insurance_number = fields.Char(string='Số thẻ BHYT', required=True, unique=True)
    initial_facility = fields.Char(string='Nơi ĐKKCB', required=True)
    tier = fields.Selection([
        ('central', 'Trung ương'),
        ('province', 'Tỉnh'),
        ('district', 'Quận/Huyện'),
        ('commune', 'Xã')
    ], string='Tuyến', required=True)
    expiry_date = fields.Date(string='Thời hạn', required=True)
    state = fields.Selection([
        ('valid', 'Hợp lệ'),
        ('expired', 'Hết hạn')
    ], string='Trạng thái', compute='_compute_state', store=True)

    @api.depends('expiry_date')
    def _compute_state(self):
        today = date.today()
        for record in self:
            if record.expiry_date and record.expiry_date < today:
                record.state = 'expired'
            else:
                record.state = 'valid'

    @api.constrains('insurance_number')
    def _check_insurance_number_length(self):
        for record in self:
            if len(record.insurance_number) != 15:  # Giả định số thẻ BHYT là 15 ký tự
                raise ValidationError("Số thẻ BHYT phải có đúng 15 ký tự!")

    # Đảm bảo chỉ một bệnh nhân có thể liên kết với một insurance_number
    @api.constrains('insurance_number')
    def _check_unique_insurance_per_patient(self):
        for record in self:
            if record.insurance_number:
                patients = self.env['clinic.patient'].search_count([('insurance_number', '=', record.insurance_number)])
                if patients > 1:
                    raise ValidationError("Số thẻ BHYT đã được gán cho một bệnh nhân khác! Mỗi bệnh nhân chỉ được có một bảo hiểm.")