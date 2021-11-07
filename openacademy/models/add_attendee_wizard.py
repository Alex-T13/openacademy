from odoo import fields, models, exceptions, _


class AddAttendeeWizard(models.TransientModel):
    _name = 'openacademy.add_attendee_wizard'
    _description = "Wizard: Add Attendee to Sessions"

    session_ids = fields.Many2many(
        comodel_name='openacademy.session',
        string="Sessions",
        required=True,
        default=lambda self: self._default_sessions(),
    )

    attendee_ids = fields.Many2many(
        comodel_name='res.partner',
        string="Attendees",
        required=True,
        domain=[('is_instructor', '=', False)],
    )

    def _default_sessions(self):
        return self.env['openacademy.session'].browse(self.env.context.get('active_ids'))

    def add_attendee(self):

        for session in self.session_ids:
            if session.number_attendees >= session.seats:
                raise exceptions.ValidationError(
                    _(
                        "Error adding attendee. The number of seats for this session in the \
                        {} programming course has been exceeded.".format(session.course_id.title)
                    )
                )
            session.attendee_ids += self.attendee_ids
        return {}
