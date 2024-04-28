import redis
import hashlib
 
r = redis.Redis(host='localhost', port=6379, db=0)

def hash_encrypt(text, algorithm='sha256'):
    hash_object = hashlib.new(algorithm, text.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig

def add_user(username, password, email):
    if r.exists(f'username:{username}'):
        return 0
    # user_id = r.incr('user_id')
    # r.hset(f'user:{user_id}', 'username', username)
    # r.hset(f'user:{user_id}', 'password', password)
    # r.hset(f'user:{user_id}', 'email', email)

    hased_password = hash_encrypt(password)
    r.hset(f'username:{username}', mapping={'username': username, 'password': hased_password, 'email': email})

    # handle the case where the connection to the database is lost

    return 1
 
def authenticate_user(username, password):
    if r.exists(f'username:{username}'):
        stored_password = r.hget(f'username:{username}', 'password')
        # print(stored_password)
        if stored_password.decode('utf-8') == hash_encrypt(password):
            ##### TODO: Generate a token #####
            token = r.incr('token_id')
            r.set(f'token:{token}', user_id)
            return True
    return False
 
def get_user(username):
    user_data = r.hgetall(f'username:{username}')
    return {key.decode('utf-8'): value.decode('utf-8') for key, value in user_data.items()}

# test
# is_equal = b'password123'.decode('utf-8') == 'password123'
# print(is_equal)

user_id = add_user('yiheng', 'password123', 'yiheng@example.com')
print(f'User added with ID: {user_id}')
 
authenticated = authenticate_user('yiheng', 'password123')
print(f'Authentication result: {authenticated}')
 
user_info = get_user('yiheng')
print(f'User information: {user_info}')