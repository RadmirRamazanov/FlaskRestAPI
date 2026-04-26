from requests import get, post, delete

# гет запросы
# на всех юзеров
print(get("http://localhost:5000/api/v2/users").json())
# на одного юзера
# {'message': 'Users 999 not found'}
print(get("http://localhost:5000/api/v2/users/999").json())
# коррект
print(get("http://localhost:5000/api/v2/users/1").json())

# пост запросы
# {'message': {'surname': 'Missing required parameter in the JSON body or the post body or the query string'}}
print(post("http://localhost:5000/api/v2/users", json={}).json())
# коррект
print(post("http://localhost:5000/api/v2/users",
           json={
                'surname': 'seijuro',
                'name': 'akashi',
                'age': 19,
                'position': 'capitan',
                'speciality': 'sportsmen',
                'address': 'tokyo 23',
                'email': 'akashi@seijuro.tk',
                'hashed_password': '12312313'
           }).json())
# делит запросы
# {'message': 'Internal Server Error'} или {'message': 'Users 999 not found'}
print(delete("http://localhost:5000/api/v2/users/999").json())
# коррект({'success': 'OK'})
print(delete("http://localhost:5000/api/v2/users/2").json())

# гет запросы
# на всех работы
print(get("http://localhost:5000/api/v2/jobs").json())
# на одну работу
# {'message': 'Jobs 999 not found'}
print(get("http://localhost:5000/api/v2/jobs/999").json())
# коррект
print(get("http://localhost:5000/api/v2/jobs/1").json())

# пост запросы
# {'message': {'team_leader': 'Missing required parameter in the JSON body or the post body or the query string'}}
print(post("http://localhost:5000/api/v2/jobs", json={}).json())
# коррект
print(post("http://localhost:5000/api/v2/jobs",
           json={
                'team_leader': 1,
                'job': 'Тестирование модуля авторизации',
                'work_size': 25,
                'collaborators': '2, 3',
                'start_date': '2024-03-20',
                'end_date': '2024-03-27',
                'is_finished': False
            }).json())

# делит запросы
# {'message': 'Jobs 999 not found'}
print(delete("http://localhost:5000/api/v2/jobs/999").json())
# коррект({'success': 'OK'})
print(delete("http://localhost:5000/api/v2/jobs/1").json())


'''
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('hashed_password', required=True)
'''