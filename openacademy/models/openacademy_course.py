from odoo import fields, models, _


class Course(models.Model):
    _name = 'openacademy.course'
    _description = "Open Academy Courses"
    _order = 'title'
    _rec_name = 'title'

    active = fields.Boolean(default=True)

    title = fields.Char(string="Title course", required=True,)
    description = fields.Text(string='Description')

    session_ids = fields.One2many(
        comodel_name='openacademy.session',
        inverse_name='course_id',
        string='Sessions',
    )

    responsible_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsible',
        ondelete='cascade',
    )

    state = fields.Selection(
        string='State',
        selection=[
            ('active', 'Active'),
            ('inactive', 'Not Active'),
        ],
        default="active",
        required=True,
        readonly=True,
        copy=False,
    )

    _sql_constraints = [
        (
            'title_unique',
            'UNIQUE(title)',
            _("The course title must be unique")
        ),
    ]

    def move_to_archive(self):
        """
        Deactive course and remove sessions
        """
        self.ensure_one()
        self.active = False
        self.with_context(active=False).change_state()
        self.session_ids = []

    def restore_from_archive(self):
        """
        Mark course as active
        """
        self.ensure_one()
        self.active = True
        self.with_context(active=True).change_state()

    def change_state(self):
        """
        Change of state field
        """
        if self.env.context.get('active'):
            self.write({'state': 'active'})
        else:
            self.write({'state': 'inactive'})

    def copy(self, default=None):
        if not default:
            default = {}
        title = self.title
        list_title = self.search([('title', 'like', str(title) + '%')])
        if len(list_title) > 1:
            title = 'Duplicate of {} ({})'.format(title, len(list_title))
        else:
            title = 'Duplicate of {}'.format(title)

        default['title'] = title
        return super(Course, self).copy(default)
