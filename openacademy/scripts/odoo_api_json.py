import random
import requests
import json

import argparse
from typing import Optional, Union, List
from datetime import date, datetime, timedelta


parser = argparse.ArgumentParser()
parser.add_argument("db", type=str, help="database name")   # 'odoo14'
parser.add_argument("user", type=str, help="user name or email")  # alexander.tarletsky@ventor.tech
parser.add_argument("password", type=str, help="password")
parser.add_argument(
    "-u", "--url",
    type=str, default="http://localhost:8069/jsonrpc",
    help="number of sessions (default=http://localhost:8069/jsonrpc)",
)
parser.add_argument(
    "-ns", "--number_of_sessions",
    type=int, default=1,
    help="number of sessions (default=1)",
)
parser.add_argument(
    "-sd", "--start_date",
    type=str, default=date.today().strftime('%Y-%m-%d'),
    help="start date of session ('YYYY-MM-DD')(default - today)",
)
parser.add_argument("-s", "--seats", type=int, default=10, help="seats of session (default=10)")
cmd_args = parser.parse_args()


class CreateSessions:
    def __init__(self):
        self.url = cmd_args.url
        self.db = cmd_args.db
        self.user = cmd_args.user
        self._password = cmd_args.password
        self.uid = self._auth_uid()
        self.number_of_sessions = cmd_args.number_of_sessions
        self.start_date = datetime.strptime(cmd_args.start_date, '%Y-%m-%d')
        self.seats = cmd_args.seats
    
    def json_rpc(self, method, params):
        headers = {'content-type': 'application/json'}
        re_id = int(round(datetime.now().timestamp()))
        payload = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
            'id': re_id,
        }

        response = requests.post(self.url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        if response.json().get('error'):
            raise Exception(response.json()['error']['message'])

        return response.json()['result']

    def call(self, service, method, *args):
        re_args = (self.db, self.uid, self._password) + args
        params = {
            'service': service,   # common or object
            'method': method,   # execute_kw / login /
            'args': re_args,
        }
        
        return self.json_rpc('call', params=params)

    def _auth_uid(self) -> str:
        uid_args = (self.db, self.user, self._password)
        params = {
            'service': 'common',   # common or object
            'method': 'login',   # execute_kw / login /
            'args': uid_args,
        }
        uid = self.json_rpc('call', params=params)
        if not uid:
            raise AttributeError("Invalid authentication parameters!")
        return uid

    def instructor_ids(self) -> Union[bool, List[str]]:
        instructor_ids = self.call(
            'object', 'execute_kw',
            'res.partner', 'search',
            [[['is_instructor', '=', True]]],
        )
        if instructor_ids:
            return instructor_ids
        return False

    def course_id(self) -> Union[bool, List[str]]:
        course_id = self.call(
            'object', 'execute_kw',
            'openacademy.course', 'search',
            [[['title', 'ilike', 'python']]],
        )
        if course_id:
            return course_id
        return False

    def is_same_session(self) -> List[str]:
        course_id = self.course_id()[0]
        if not course_id:
            raise AttributeError("Course with the same name is not registered!")
        same_session = self.call(
            'object', 'execute_kw',
            'openacademy.session', 'search',
            [[['course_id', '=', course_id]]],
        )
        if not same_session:
            same_session = []
        return same_session

    def check_start_date(self) -> Union[bool, str, List[str]]:
        date_list = []
        same_session = self.is_same_session()
        if not same_session:
            return False
        else:
            start_date_same_session = self.call(
                'object', 'execute_kw',
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

    def create_sessions(self) -> Optional[str]:
        number_of_sessions = self.number_of_sessions
        start_date = self.start_date
        list_start_date = self.check_start_date() if self.check_start_date() else []
        new_sessions_id = None
        while number_of_sessions > 0:
            while start_date.strftime('%Y-%m-%d') in list_start_date:   # exclude start_date matches
                start_date += timedelta(days=1)

            new_sessions_id = self.call(
                'object', 'execute_kw',
                'openacademy.session', 'create',
                [{
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'seats': self.seats,
                    'duration': 10,
                    'course_id': self.course_id()[0],
                    'instructor_id': random.choice(self.instructor_ids()),
                }],
            )
            start_date += timedelta(days=36)
            number_of_sessions -= 1
            print(f"Create session {new_sessions_id} successful!")
        return new_sessions_id


if __name__ == "__main__":
    create_sessions = CreateSessions()
    # print(f"uid: {create_sessions.uid}")
    # print(f"instructor_ids(): {create_sessions.instructor_ids()}")
    # print(f"course_id(): {create_sessions.course_id()}")
    # print(f"is_same_session: {create_sessions.is_same_session()}")
    create_sessions.create_sessions()
