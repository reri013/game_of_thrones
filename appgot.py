import json
import math
from collections import defaultdict
from flask import Flask, abort, request
from flask_basicauth import BasicAuth
import pymysql
from requests.auth import HTTPBasicAuth
from flask_swagger_ui import get_swaggerui_blueprint




app = Flask(__name__)

def remove_null_fields(obj):
    return {k:v for k, v in obj.items() if v is not None}


MAX_PAGE_SIZE = 30

@app.route("/character")
def characters():
    page = int(request.args.get('page', 0))
    page_size = int(request.args.get('page_size', MAX_PAGE_SIZE))
    page_size = min(page_size, MAX_PAGE_SIZE)
    include_book = bool(int(request.args.get('include_book', 0)))
    
    db_conn = pymysql.connect(host="localhost",
                            user="root", 
                            database="GOT",  
                            password = "-1Xy781227@",
                            cursorclass=pymysql.cursors.DictCursor)

    # Get character
    with db_conn.cursor() as cursor:
        cursor.execute("""
                    select name, house from predictions 
                    order by name 
                    LIMIT %s
                    OFFSET %s; 
                    """ , (page_size, page * page_size))
        character = cursor.fetchall()
        character_names = [char['name'] for char in character]

    with db_conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM predictions")
        total = cursor.fetchone()
        last_page = math.ceil(total['total'] / page_size)
        
    if include_book:
    # Get books
        with db_conn.cursor() as cursor:
            placeholder = ','.join(['%s'] * len(character_names))
            cursor.execute(f"""SELECT name, book_of_death,
                    case 
                    when a_game_of_thrones = 1 then 'a_game_of_thrones' else null end as 'inbook1',
                    case
                    when a_clash_of_kings = 1 then 'a_clash_of_kings' else null end as 'inbook2', 
                    case
                    when a_storm_of_swords = 1 then 'a_storm_of_swords' else null end as 'inbook3',
                    case
                    when a_feast_for_crows = 1 then 'a_feast_for_crows' else null end as 'inbook4',
                    case
                    when a_dance_with_dragons = 1 then 'a_dance_with_dragons' else null end as 'inbook5'
                    from death2
                    where name in ({placeholder})""", character_names)
            books = cursor.fetchall()
        books_dict = defaultdict(list)
        for obj in books:
            name = obj['name']
            del obj['name']
            books_dict[name].append(obj)

    
        # Merge books into character
        for char in character:
            name = char['name']
            char['in_the_books'] = books_dict[name]
        
    db_conn.close()
    return {
        'character': character,
        'next_page': f'/character?page={page+1}&page_size={page_size}&include_book={int(include_book)}',
        'last_page': f'/character?page={last_page}&page_size={page_size}&include_book={int(include_book)}',
    }


@app.route("/character/<int:character_id>")
def character(character_id):
    
    db_conn = pymysql.connect(host="localhost",
                            user="root", 
                            database="GOT",  
                            password = "-1Xy781227@",
                            cursorclass=pymysql.cursors.DictCursor)


    with db_conn.cursor() as cursor:
        cursor.execute("""
select p.character_id, p.name, p.father, p.mother, p.house,  d.gender, d.death_chapter, d.book_of_death, p.DateoFdeath,
CASE 
WHEN p.DateoFdeath is null
then 'Alive'
else 'Dead'
end as dead_or_not
from predictions as p
left join death2 as d
	on p.name = d.name
            WHERE p.character_id=%s
        """, (character_id, ))
        charac = cursor.fetchone()
        if not charac:
            abort(404)
        charac = remove_null_fields(charac)
            
    db_conn.close()
    return charac


