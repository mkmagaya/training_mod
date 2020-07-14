#-*- coding: utf-8 -*-

from openerp import models, fields, api

class MainChecklistConfig(models.Model):
    _name = 'main.checklist.config'
    
    name = fields.Char(
        string='Course Name',
        required=True,
    )
    main_checklist_ids = fields.Many2many(
        'hr.orientation.checklist.config',
        string='Course Configuration',
    )
    active_id = fields.Boolean(
        string='Active',
        default=True,
    )
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        required=True
    )
    survey_id = fields.Many2one(
        'survey.survey',
        string='Exam/Test',
        required=False,
        store=True,
    )
    response_id = fields.Many2one(
        'survey.user_input',
        "Response",
        ondelete="set null", 
        oldname="response"
    )


    @api.multi
    def action_start_survey(self):
        self.ensure_one()
        # create a response and link it to this applicant
        if not self.response_id:
            response = self.env['survey.user_input'].create({'survey_id': self.survey_id.id, 'partner_id': self.partner_id.id})
            self.response_id = response.id
        else:
            response = self.response_id
        # grab the token of the response and start surveying
        return self.survey_id.with_context(survey_token=response.token).action_start_survey()

    @api.multi
    def action_print_survey(self):
        """ If response is available then print this response otherwise print survey form (print template of the survey) """
        self.ensure_one()
        if not self.response_id:
            return self.survey_id.action_print_survey()
        else:
            response = self.response_id
            return self.survey_id.with_context(survey_token=response.token).action_print_survey()


class HrOrientationChecklistConfig(models.Model):
    _name = 'hr.orientation.checklist.config'
    
    name = fields.Char(
        string='Name',
        required=True
    )

    web_url = fields.Char(
        string='Web URL',
        required=True
    )

    responsible_user_id = fields.Many2one(
        'res.users',
        string='Responsible User',
        required=False,
    )
    survey_id = fields.Many2one(
        'survey.survey',
        string='Mini Test',
        required=False,
        store=True,
    )
    note = fields.Text(
        string='Notes',
        store=True,
    )
    attachment_ids1 = fields.Binary(
        string='First Attachment',
        store=True,
    )
    attachment_ids2 = fields.Binary(
        string='Second Attachment',
        store=True,
    )
    attachment_ids3 = fields.Binary(
        string='Third Attachment',
        store=True,
    )

    @api.multi
    def action_start_survey(self):
        self.ensure_one()
        # create a response and link it to this applicant
        if not self.response_id:
            response = self.env['survey.user_input'].create({'survey_id': self.survey_id.id, 'partner_id': self.partner_id.id})
            self.response_id = response.id
        else:
            response = self.response_id
        # grab the token of the response and start surveying
        return self.survey_id.with_context(survey_token=response.token).action_start_survey()

    @api.multi
    def action_print_survey(self):
        """ If response is available then print this response otherwise print survey form (print template of the survey) """
        self.ensure_one()
        if not self.response_id:
            return self.survey_id.action_print_survey()
        else:
            response = self.response_id
            return self.survey_id.with_context(survey_token=response.token).action_print_survey()


class HrOrientationChecklist(models.Model):
    _name = 'hr.orientation.checklist'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _order = 'id asc'
    _rec_name = 'name'
    _description = "Employee Course Modules"

    name = fields.Char(
        string='Name',
        required=True,
        readonly=True
    )
    responsible_user_id = fields.Many2one(
        'res.users',
        string='Responsible User',
        required=True,
    )
    checklist_state = fields.Selection(
        selection=[('new', 'Ungraded'), \
        ('done', 'Completed'),\
        ('pass', 'Passed'),\
        ('fail', 'Failed'),\
        ('cancel', 'Cancelled')],
        string='Status',
        copy=False,
        default='new',
        track_visibility='onchange'
    )
    checklist_date = fields.Date(
        string='Date',
        readonly=True
    )
    expected_date = fields.Date(
        string='Expected Date',
        default=fields.Date.today(),
        required= True,
    )
    orientation_id = fields.Many2one(
        'hr.orientation',
        string='Training',
        readonly=True,
    )
    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.user.company_id,
        string='Company',
        readonly=True
    )
    note = fields.Text(
        string='Notes',
        #related='orientation_id.main_configuration_id.main_checklist_ids.note',
        readonly=True,
        store=True,
    )
    attachment_ids1 = fields.Binary(
        string='First Attachment',
        #related='orientation_id.main_configuration_id.main_checklist_ids.attachment_ids1',
        readonly=True,
        store=True,
    )
    attachment_ids2 = fields.Binary(
        string='Second Attachment',
        #related='orientation_id.main_configuration_id.main_checklist_ids.attachment_ids2',
        readonly=True,
        store=True,
    )
    attachment_ids3 = fields.Binary(
        string='Third Attachment',
        #related='orientation_id.main_configuration_id.main_checklist_ids.attachment_ids3',
        readonly=True,
        store=True,
    )
    employee_id = fields.Many2one(
        related='orientation_id.employee_id',
        string='Employee User',
        readonly=True,
        store=True,
    )

    x_orientation_checklist_id = fields.Many2one(
        'hr.orientation.checklist.config',
        string='Course Module ID',
        store=True,
        readyonly=True
    )

    web_url = fields.Char(
        string='Web URL',
        readonly=True,
    )

    survey_id = fields.Many2one(
        'survey.survey',
        String='Test/Exam',
        store=True,
        readonly=True
    )
    supervisor = fields.Many2one(
        related='orientation_id.user_id',
        String='Supervisor Name',
        store=True,
        readonly=True
    )
    response_id = fields.Many2one(
        'survey.user_input',
        "Response",
        ondelete="set null", 
        oldname="response",
        store=True,
        readonly = True,
    )
    survey_score = fields.Float(
        related='response_id.quizz_score',
        String='Test Score',
        store=True,
        readonly = True
    )

    @api.one
    def process_survey_result(self):
        if self.survey_score == 0:
            self.write({'checklist_state': 'new',})
        elif (self.survey_score > 0) and (self.survey_score < 8):
            self.write({'checklist_state': 'fail',})
        elif self.survey_score >= 8:
            self.write({'checklist_state': 'pass',})

    @api.multi
    def action_start_survey(self):
        self.ensure_one()
        # create a response and link it to this applicant
        if not self.response_id:
            response = self.env['survey.user_input'].create({'survey_id': self.survey_id.id, 'responsible_user_id': self.responsible_user_id.id})
            self.response_id = response.id
        else:
            response = self.response_id
        # grab the token of the response and start surveying
        return self.survey_id.with_context(survey_token=response.token).action_start_survey()

    @api.multi
    def action_print_survey(self):
        """ If response is available then print this response otherwise print survey form (print template of the survey) """
        self.ensure_one()
        if not self.response_id:
            return self.survey_id.action_print_survey()
        else:
            response = self.response_id
            return self.survey_id.with_context(survey_token=response.token).action_print_survey()

        
class HrOrientation(models.Model):
    _name = 'hr.orientation'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _order = 'id asc'
    _rec_name = 'name'
    _description = 'Employee Courses'

    name = fields.Char(
        string='Number'
    )
    employee_id = fields.Many2one(
        'hr.employee',
        required=True,
        string="Employee",
    )
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        required=True
    )
    job_id = fields.Many2one(
        'hr.job',
        string='Job Title',
        required=True
    )
    parent_id = fields.Many2one(
        'hr.employee',
        string='Manager',
        required=True
    )
    orientation_date = fields.Date(
        string='Date',
        default=fields.Date.today(),
        readonly=True,
        copy=False,
        required=True
    )
    user_id = fields.Many2one(
        'res.users',
        default=lambda self: self.env.user,
        string='Training Supervisor',
        readonly=True,
        required=True,
    )
    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.user.company_id,
        string='Company',
        readonly=True,
        required=True,
    )
    checklist_ids = fields.One2many(
        'hr.orientation.checklist', 
        'orientation_id',
        copy=False
    )
    state = fields.Selection(
        selection=[
        ('draft', 'Draft'), \
        ('confirm', 'Confirmed'), \
        ('pass', 'Passed'), \
        ('fail', 'Failed'), \
        ('cancel', 'Cancelled'), \
        ('done', 'Completed')],
        string='Status',
        readonly=True, 
        default='draft',
        track_visibility='onchange'
    )
    main_configuration_id = fields.Many2one(
        'main.checklist.config',
        string='Courses',
        required=True,
    )

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hr.orientation')
        return super(HrOrientation, self).create(vals)

    @api.onchange('employee_id')
    def get_department(self):
        for line in self:
            line.department_id = line.employee_id.department_id.id
            line.job_id = line.employee_id.job_id.id
            line.parent_id = line.employee_id.parent_id.id
    
    @api.onchange('main_configuration_id')
    def onchange_main_configuration(self):
        vals = []
        for line in self.main_configuration_id.main_checklist_ids:
            vals.append((0,0,{'name': line.name,
                              'web_url': line.web_url,
                              'responsible_user_id':line.responsible_user_id.id ,
                              'survey_id': line.survey_id.id,
                              'checklist_state': 'new',
                              'checklist_date': fields.Date.today(),
                              'note': line.note,
                              'attachment_ids1': line.attachment_ids1,
                              'attachment_ids2': line.attachment_ids2,
                              'attachment_ids3': line.attachment_ids3
                              }))
        self.checklist_ids = vals
    
    
    @api.multi
    def get_confirm(self):
        template = self.env.ref('telco_training.email_template_employee_orientation1')
        for check in self.checklist_ids:
            template.send_mail(check.id, force_send=True)
        self.state = 'confirm'

    @api.one
    def get_done(self):
        self.state = 'done'
    
    @api.one
    def get_repeat(self):
        self.state = 'repeat'

    @api.one
    def get_cancel(self):
        self.state = 'cancel'
    
    @api.one
    def get_reset_to_draft(self):
        self.state = 'draft'

    @api.one
    def get_pass(self):
        self.state = 'pass'

    @api.one
    def get_fail(self):
        self.state = 'fail'

    @api.one
    def process_survey_result(self):
        for check in self.checklist_ids:
            #if self.checklist_ids.survey_score == 0:
            if check.survey_score == 0:
                check.write({'checklist_state': 'new',})
            elif (check.survey_score > 0) and (check.survey_score < 8):
                check.write({'checklist_state': 'fail',})
            elif check.survey_score >= 8:
                check.write({'checklist_state': 'pass',})

    @api.multi
    def action_start_survey(self):
        self.ensure_one()
        # create a response and link it to this applicant
        if not self.response_id:
            response = self.env['survey.user_input'].create({'survey_id': self.survey_id.id, 'partner_id': self.partner_id.id})
            self.response_id = response.id
        else:
            response = self.response_id
        # grab the token of the response and start surveying
        return self.survey_id.with_context(survey_token=response.token).action_start_survey()

    @api.multi
    def action_print_survey(self):
        """ If response is available then print this response otherwise print survey form (print template of the survey) """
        self.ensure_one()
        if not self.response_id:
            return self.survey_id.action_print_survey()
        else:
            response = self.response_id
            return self.survey_id.with_context(survey_token=response.token).action_print_survey()

    @api.multi
    def action_print_survey(self):
        return self.survey_id.action_print_survey()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
