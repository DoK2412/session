from fastapi import APIRouter, Request

from service.class_session import Sessions


servis_router = APIRouter(
    prefix='/session'
)


@servis_router.post('/new')
async def naw_session(requests: Request):
    session = Sessions()
    if session.user_id is None:
        if len(requests.query_params['user_id']) == 0:
            session.user_id = None
        else:
            session.user_id = int(requests.query_params['user_id'])
    if session.email is None:
        if len(requests.query_params['email']) == 0:
            session.email = None
        else:
            session.email = requests.query_params['email']
    if session.uid_session is None:
        if len(requests.query_params['uid_session']) == 0:
            session.uid_session = None
        else:
            session.uid_session = requests.query_params['uid_session']

    session.ip_client = requests.client.host

    session.device = requests.headers.get('user-agent', 'None')

    result_new = await session.create_session_db()
    if result_new is False:
        result_update = await session.updata_session_db()
        if result_update is False:
            new_session = await session.create_session_db()
            return new_session
        else:
            return result_update
    else:
        return result_new
