NEW_SESSION = '''
--создание новой сессии в базе данных
INSERT INTO sessions
    (profile_id, ip_address, uid, created_date, exp_date, active, user_device)
VALUES 
    ($1, $2, $3, $4, $5, $6, $7) RETURNING uid
'''

SHECK_SESSION = '''
--проверка наличия сессии
SELECT profile_id, uid, exp_date, active FROM sessions WHERE uid = $1 AND active = TRUE
'''

APDATE_SESSION = '''
-- обновление статуса сесии
UPDATE sessions SET active =FALSE, blocked=TRUE WHERE uid = $1 RETURNING uid
'''

SHECK_USER_ID = '''
--получение id пользователя
SELECT p.id FROM profile p WHERE  p.email = $1
'''

SHECK_SESSION_ID = '''
--проверка наличия сессии
SELECT s.profile_id, s.uid, s.exp_date, s.active 
FROM sessions s
INNER JOIN profile p ON p.id = s.profile_id
WHERE s.active = TRUE AND s.blocked = FALSE
AND CASE WHEN bool($1::int is not null) THEN s.profile_id = $1::int ELSE true END
AND CASE WHEN bool($2::varchar is not null) THEN s.uid = $2::varchar ELSE true END
AND CASE WHEN bool($3::varchar is not null) THEN p.email = $3::varchar ELSE true END

'''

BLOCK_SESSION = '''
-- блокировка сдохшей сессии
UPDATE 
'''