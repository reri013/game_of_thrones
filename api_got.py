import json
import math
import os
from collections import defaultdict, Counter

from flask import Flask, request, abort, jsonify
from flask_basicauth import BasicAuth
from flask_swagger_ui import get_swaggerui_blueprint

import pymysql


app = Flask(__name__)
#app.config.from_file("flask_config.json", load=json.load)
#auth = BasicAuth(app)

def remove_null_fields(obj):
    return {k:v for k, v in obj.items() if v is not None}


@app.route("/character/<int:character_id>")
#@auth.required
def character(character_id):
    db_conn = pymysql.connect(host="localhost"
                            , user="root"
                            ,  password='1Azertyuiop@'
                            , database="GOT",
                            cursorclass=pymysql.cursors.DictCursor)
    with db_conn.cursor() as cursor:
        cursor.execute("""
                        SELECT
                            p.character_id,
                            p.name,
                            p.title,
                            p.culture,
                            p.house,
                            p.dateOfBirth,
                            p.DateoFdeath,
                            p.father,
                            p.mother,
                            p.heir,
                            p.spouse,
                            CASE
                                WHEN p.DateoFdeath IS NULL THEN 'Alive'
                                ELSE 'Dead'
                            END AS dead_or_not,
                            CASE
                                WHEN p.DateoFdeath IS NOT NULL THEN p.DateoFdeath - p.dateOfBirth
                                ELSE NULL
                            END AS AgeDeath,
                            CASE
                                WHEN d2.book_of_death = '1' THEN 'a_game_of_thrones'
                                WHEN d2.book_of_death = '2' THEN 'a_clash_of_kings'
                                WHEN d2.book_of_death = '3' THEN 'a_storm_of_swords'
                                WHEN d2.book_of_death = '4' THEN 'a_feast_for_crows'
                                WHEN d2.book_of_death = '5' THEN 'a_dance_with_dragons'
                                ELSE NULL
                            END AS Book_of_dead
                        FROM predictions AS p
                        LEFT JOIN death2 AS d2 ON d2.name = p.name
                        WHERE p.character_id=%s""", (character_id, ))
        character = cursor.fetchone()
        if character is not None:
            character = remove_null_fields(character)
        else:
            abort(404)  # Aucun personnage trouvé, retourner une erreur 404
        #if not character:
            #abort(404)
        #character = [remove_null_fields(c) for c in character]
    db_conn.close() 
    return character 

MAX_PAGE_SIZE = 10

@app.route("/characters")
def characters():
    page = int(request.args.get('page', 0))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)
    include_details = int(request.args.get('include_details', 0))

    db_conn = pymysql.connect(host="localhost", 
                            user="root",
                            password='1Azertyuiop@', 
                            database="GOT",
                            cursorclass=pymysql.cursors.DictCursor)
    #get the character
    with db_conn.cursor() as cursor:
        cursor.execute(""" SELECT 
                            p.character_id,
                            p.name, 
                            p.title, 
                            p.culture, 
                            p.house, 
                            p.dateOfBirth, 
                            p.DateoFdeath,
                            CASE 
                                WHEN p.DateoFdeath is null
                                then 'Alive'
                                ELSE 'Dead'
                            end as dead_or_not
                        FROM predictions as p  
            ORDER BY p.name
            LIMIT %s
            OFFSET %s
        """, (page_size, page * page_size))
        characters = cursor.fetchall()
        character_ids = [char['name'] for char in characters]
        characters = [remove_null_fields(char) for char in characters]
    

    # Get the total characters count   
    with db_conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM predictions")
        total = cursor.fetchone()
        last_page = math.ceil(total['total'] / page_size)

    db_conn.close()
    return {
        'characters': characters,
        'next_page': f'/movies?page={page+1}&page_size={page_size}',
        'last_page': f'/movies?page={last_page}&page_size={page_size}',
    }

