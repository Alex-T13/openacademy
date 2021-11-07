from datetime import timedelta
from odoo import fields, models, api, exceptions, _


class Session(models.Model):
    _name = 'openacademy.session'
    _description = "Open Academy Sessions"
    _order = 'course_id'
    _rec_name = 'course_id'

    active = fields.Boolean(default=True)

    color = fields.Integer()

    start_date = fields.Date(
        string='Start Date',
        default=lambda self: fields.datetime.now(),
    )

    seats = fields.Integer(string='Seats', required=True)
    duration = fields.Integer(string='Duration of days')

    course_id = fields.Many2one(
        comodel_name='openacademy.course',
        string='Course',
        ondelete='cascade',
        required=True,
    )

    instructor_id = fields.Many2one(
        comodel_name='res.partner',
        string='Instructor',
        ondelete='cascade',
        domain=[('is_instructor', '=', True), ('is_company', '=', False)],
        required=True,
        default=lambda self: self.env.uid,   # _uid
    )

    attendee_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Attendees',
    )

    number_attendees = fields.Integer(
        string='Number of attendees',
        compute='_compute_number_attendees',
        store=True,
    )

    taken_percentage = fields.Float(
        string='Occipied places',
        compute='_compute_taken_percentage',
        store=True,
    )

    end_date = fields.Date(
        string='End Date',
        compute='_compute_end_date',
        inverse='_inverse_end_date',
        store=True,
    )

    @api.depends('seats', 'attendee_ids',)
    def _compute_taken_percentage(self):
        for session in self:
            if len(session.attendee_ids) > 0:
                occupancy = len(session.attendee_ids) / session.seats * 100
                session.taken_percentage = occupancy
            else:
                session.taken_percentage = 0

    @api.depends('start_date', 'duration',)
    def _compute_end_date(self):
        for session in self:
            session.end_date = session.start_date + timedelta(days=session.duration)

    def _inverse_end_date(self):
        for session in self:
            duration = session.end_date - session.start_date
            session.duration = duration.days

    @api.depends('attendee_ids')
    def _compute_number_attendees(self):
        for record in self:
            record.number_attendees = len(record.attendee_ids)

    @api.onchange('seats', 'attendee_ids')
    def _check_seats(self):
        """
        Do not allowed to set the number of seats less than the number participants
        """
        for record in self:
            if record.seats < len(record.attendee_ids):
                raise exceptions.UserError(
                    _("Number of seats should be more than number of participants")
                )

    @api.onchange('end_date', 'duration', )
    def _check_date(self):
        """
        Do not allowed to set negative session duration
        """
        for session in self:
            duration = session.end_date - session.start_date

            if session.duration < 0 or duration.days < 0:
                raise exceptions.UserError(_("Duration cannot be negative"))

    @api.constrains('attendee_ids')
    def _check_attendee(self):
        for record in self.attendee_ids:
            if record.is_instructor:
                raise exceptions.ValidationError(
                    _("Error adding session attendee! Instructor cannot be a attendee")
                )

    @api.constrains('instructor_id')
    def _check_instructor(self):
        for record in self.instructor_id:
            if not record.is_instructor:
                raise exceptions.ValidationError(
                    _("Error adding session instructor! This participant is not an instructor")
                )
