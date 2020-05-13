from openerp import api, models, fields
from datetime import datetime


class hr_timesheet_karty_wizard(models.TransientModel):
    _name = 'hr.timesheet.karty.wizard'

    employee_id = fields.Many2one(comodel_name="hr.employee", required=True)
    date_from = fields.Date(default=fields.Datetime.now, required=True)
    date_to = fields.Date(default=fields.Datetime.now, required=True)

    @api.multi
    def print_report(self):
        self.ensure_one()
        datas = {'wizard_id': self.id}
        return self.env['report'].get_action(self, 'hr_timesheet_karty.template_hr_timesheet_karty', data=datas)


class HrTimesheetKartyReport(models.AbstractModel):
    _name = 'report.hr_timesheet_karty.template_hr_timesheet_karty'

    @api.multi
    def render_html(self, data=None):
        hr_analytic_timesheet = self.env['hr.analytic.timesheet']
        if data and 'wizard_id' in data:
            wizard = self.env['hr.timesheet.karty.wizard'].browse(
                data['wizard_id'])
            records = hr_analytic_timesheet.search([('employee_id', '=', wizard.employee_id.id),
                                                    ('date_from', '>=', wizard.date_from),
                                                    ('date_to', '<=', wizard.date_to)])
        else:
            records = hr_analytic_timesheet.browse(self._ids)
        # sum records hours if date is the same (group by date)

        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'hr_timesheet_karty.template_hr_timesheet_karty')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': records,
        }
        return report_obj.render('hr_timesheet_karty.template_hr_timesheet_karty', docargs)
