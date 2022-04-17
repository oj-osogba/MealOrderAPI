from flask import Blueprint, jsonify, request, abort
from src.settings import conn

conn.set_session(autocommit=True)

bp = Blueprint('names', __name__, url_prefix='/names')
REQUIRED_KEY_FOR_NAMES = ['first_name', 'last_name']

@bp.route('', methods=['POST', 'PUT', 'PATCH'])
def add():
    
    cur = conn.cursor()

    first_name = request.json.get('first_name')
    middle_name = request.json.get('middle_name')
    last_name = request.json.get('last_name')
    user_id = request.json.get('user_id')

    name_dict = {
        'first_name': first_name,
        'last_name': last_name,
        'middle_name': middle_name
    }

    if user_id is None:
        if any(key not in request.json for key in REQUIRED_KEY_FOR_NAMES):
            return jsonify({'message': 'Insufficient Data'})
        cur.execute(
            """
            INSERT INTO names(first_name, last_name, middle_name)
                VALUES(%s, %s, %s)
                RETURNING id;
            """,(first_name, middle_name, last_name))
        name_id = cur.fetchall()[-1][-1]

        return name_id
    else:
        cur.execute("""
            SELECT name_id FROM users
                WHERE id = %s;
        """,(user_id, ))
        name_ids = cur.fetchall()
        if len(name_ids) == 0:
            return jsonify({'message': 'User does not Exist'})
        name_id = name_ids[-1][-1]
    
        for variable in name_dict:
            if name_dict[variable] is not None:
                if variable == 'first_name':
                    cur.execute(
                        """
                        UPDATE names
                            SET first_name = %s
                            WHERE id = %s; 
                        """,(name_dict[variable], name_id)
                    )
                elif variable == 'last_name':
                    cur.execute(
                        """
                        UPDATE names
                            SET last_name = %s
                            WHERE id = %s; 
                        """,(name_dict[variable], name_id)
                    )
                elif variable == 'middle_name':
                    cur.execute(
                        """
                        UPDATE names
                            SET middle_name = %s
                            WHERE id = %s; 
                        """,(name_dict[variable], name_id)
                    )
        return jsonify(True)

