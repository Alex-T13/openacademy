import xmlrpc.client as xmlrpclib
import random
import argparse
from datetime import date, timedelta

parser = argparse.ArgumentParser()
parser.add_argument("db", type=str, help="database name")   # 'odoo14'
parser.add_argument("user", type=str, help="user name or email")  # alexander.tarletsky@ventor.tech
parser.add_argument("password", type=str, help="password")
parser.add_argument(
    "-u", "--url",
    type=str, default="http://localhost:8069",
    help="number of sessions (default=http://localhost:8069)",
)
parser.add_argument(
    "-ns", "--number_of_sessions",
    type=int, default=1,
    help="number of sessions (default=1)",
)
parser.add_argument(
    "-sd", "--start_date",
    type=date, default=date.today(),
    help="start date of session (default - today)",
)
parser.add_argument("-s", "--seats", type=int, default=10, help="seats of session (default=10)")
args = parser.parse_args()


class CreateSessions:
    def __init__(self):
        self.url = args.url
        self.db = args.db
        self.user = args.user
        self._password = args.password
        self.ODOO_API_COMMON = f"{self.url}/xmlrpc/2/common"
        self.ODOO_API_OBJECT = f"{self.url}/xmlrpc/2/object"
        self._common = xmlrpclib.ServerProxy(self.ODOO_API_COMMON)
        self.uid = self._auth_uid()
        self.models = xmlrpclib.ServerProxy(self.ODOO_API_OBJECT)
        self.number_of_sessions = args.number_of_sessions
        self.start_date = args.start_date
        self.seats = args.seats

    def _auth_uid(self):
        uid = self._common.authenticate(self.db, self.user, self._password, {})
        if not uid:
            raise AttributeError("Invalid authentication parameters!")
        return uid

    def instructor_ids(self):
        instructor_ids = self.models.execute_kw(
            self.db, self.uid, self._password,
            'res.partner', 'search',
            [[['is_instructor', '=', True]]],
        )
        if instructor_ids:
            return instructor_ids
        return False

    def course_id(self):
        course_id = self.models.execute_kw(
            self.db, self.uid, self._password,
            'openacademy.course', 'search',
            [[['title', 'ilike', 'javascript']]],
        )
        if course_id:
            return course_id
        return False

    def is_same_session(self):
        course_id = self.course_id()[0]
        if not course_id:
            raise AttributeError("Course with the same name is not registered!")
        same_session = self.models.execute_kw(
            self.db, self.uid, self._password,
            'openacademy.session', 'search',
            [[['course_id', '=', course_id]]],
        )
        if not same_session:
            return False
        return same_session

    def check_start_date(self):
        date_list = []
        same_session = self.is_same_session()
        if not same_session:
            return False
        else:
            start_date_same_session = self.models.execute_kw(
                self.db, self.uid, self._password,
                'openacademy.session', 'read',
                [same_session],
                {'fields': ['start_date']}
            )
            if len(same_session) == 1:
                return start_date_same_session[0]['start_date']
            else:
                for item in start_date_same_session:
                    date_list.append(item['start_date'])
                return date_list

    def create_weekly_sessions(self):
        number_of_sessions = self.number_of_sessions
        start_date = self.start_date
        while number_of_sessions > 0:
            while str(start_date) in self.check_start_date():   # exclude start_date matches
                start_date += timedelta(days=1)
            if len(self.is_same_session()) >= 30:
                raise AttributeError(
                    "Limit is exceeded! You can no longer create sessions for this course."
                )
            new_weekly_sessions_id = self.models.execute_kw(
                self.db, self.uid, self._password,
                'openacademy.session', 'create',
                [{
                    'start_date': str(start_date),
                    'seats': self.seats,
                    'duration': 7,
                    'course_id': self.course_id()[0],
                    'instructor_id': random.choice(self.instructor_ids()),
                }],
            )
            start_date += timedelta(days=15)
            number_of_sessions -= 1
            print(f"Create session {new_weekly_sessions_id} sucsefull!")
        return new_weekly_sessions_id


if __name__ == "__main__":
    create_sessions = CreateSessions()
    create_sessions.create_weekly_sessions()
