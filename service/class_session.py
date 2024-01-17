from datetime import datetime, timedelta

from database.connection_db import JobDb
import database.sql_requests as sql

import uuid


class Sessions():
    def __init__(self):
        self.user_id: int = None
        self.uid_user: str = None
        self.uid_session: str = None
        self.email: str = None
        self.ip_client: str = None
        self.device: str = None
        self.update: bool = False

    async def create_session_db(self):
        async with JobDb() as pool:

            check_uid = await pool.fetchrow(sql.SHECK_SESSION_ID, self.user_id, self.uid_session, self.email)
            if check_uid and check_uid['exp_date'] > datetime.now():
                self.user_id = check_uid['profile_id']
                self.uid_session = check_uid['uid']
                return {'user_id': self.user_id, 'uid_session': self.uid_session, 'email': self.email, 'update': self.update}
            elif check_uid:
                self.user_id = check_uid['profile_id']
                self.uid_session = check_uid['uid']
                return False

            session_code = await Sessions.generate_uuid4()
            date = datetime.now()
            exp_date = date + timedelta(seconds=7200)
            if self.email:
                self.user_id = await pool.fetchval(sql.SHECK_USER_ID, self.email)
            self.uid_session = await pool.fetchval(sql.NEW_SESSION, self.user_id, self.ip_client, session_code, date, exp_date, True, self.device)
            self.update = True
            return {'user_id': self.user_id, 'uid_session': self.uid_session, 'email': self.email, 'update': self.update}


    @classmethod
    async def generate_uuid4(cls):
        return str(uuid.uuid4())

    async def updata_session_db(self):
        async with JobDb() as pool:
            check_uid = await pool.fetchrow(sql.SHECK_SESSION, self.uid_session)
            if check_uid:
                if datetime.now() > check_uid['exp_date']:
                    await pool.execute(sql.APDATE_SESSION, self.uid_session)
                    return False
                else:
                    return {'user_id': self.user_id, 'uid_session': self.uid_session, 'email': self.email, 'update': self.update}