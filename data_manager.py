from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import random
import database_common
import time


@database_common.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT * FROM question
        ORDER BY submission_time DESC
        """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_last_questions(cursor: RealDictCursor) -> list:
    query = """
        SELECT * FROM question
        ORDER BY submission_time DESC FETCH first 5 rows only """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_tabel_comment(cursor: RealDictCursor) -> list:
    query="""
        SELECT * FROM comment"""
    cursor.execute(query)
    return cursor.fetchall() 


@database_common.connection_handler
def get_comments_by_question_id(cursor: RealDictCursor,question_id:int) -> list:
    query="""
        SELECT * FROM comment 
        WHERE question_id=%(question_id)s"""
    args={'question_id':question_id}
    cursor.execute(query,args)
    return cursor.fetchall()

@database_common.connection_handler
def get_answer(cursor: RealDictCursor) -> list:
    query = """
        SELECT * FROM answer
        """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_all_tags(cursor: RealDictCursor) -> list:
    query = """
        SELECT * FROM tag
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def all_question_tag(cursor: RealDictCursor) -> list:
    query = """
        SELECT * FROM question_tag
        """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_tag_id(cursor: RealDictCursor, name) -> list:
    query = """
                SELECT id FROM tag WHERE name = %s
                """
    cursor.execute(query, (name,))
    return cursor.fetchone()




@database_common.connection_handler
def add_question(cursor: RealDictCursor, submission_time: int, view_number: int, vote_number: int, title, message: str,
                 image: str) -> list:
    query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
            VALUES (%(submission_time)s,%(view_number)s,%(vote_number)s,%(title)s,%(message)s,%(image)s)
        """
    data = {'submission_time': submission_time, 'view_number': view_number, 'vote_number': vote_number,
            'title': title, 'message': message, 'image': image
            }
    cursor.execute(query, data)
    update_query = """
            SELECT * FROM question
            """
    cursor.execute(update_query)
    return cursor.fetchall()


@database_common.connection_handler
def new_answer(cursor: RealDictCursor, submission_time: str, vote_number: int, question_id: int, message: str,
               image: str) -> list:
    query = """
            INSERT INTO answer(submission_time,vote_number, question_id,message, image)
                VALUES (%(submission_time)s,%(vote_number)s,%(question_id)s,%(message)s,%(image)s)
            """
    data = {'submission_time': submission_time, 'vote_number': vote_number, 'question_id': question_id,
            'message': message, 'image': image
            }
    cursor.execute(query, data)
    update_query = """
                SELECT * FROM answer
                """
    cursor.execute(update_query)
    return cursor.fetchall()


@database_common.connection_handler
def find_question(cursor: RealDictCursor, id: int) -> list:
    query = """
        SELECT * FROM question
        WHERE id=%(id)s
        """
    data = {'id': id}
    cursor.execute(query, data)
    return cursor.fetchall()

@database_common.connection_handler
def find_comment(cursor: RealDictCursor, id: int) -> list:
    query = """
        SELECT * FROM comment
        WHERE id=%(id)s
        """
    data = {'id': id}
    cursor.execute(query, data)
    return cursor.fetchall()


@database_common.connection_handler
def find_answer(cursor: RealDictCursor, id: int) -> list:
    query = """
        SELECT * FROM answer
        WHERE id = %(id)s
        """
    data = {'id': id}
    cursor.execute(query, data)
    return cursor.fetchall()


@database_common.connection_handler
def find_answer_by_question_id(cursor: RealDictCursor, question_id: int) -> list:
    query = """
        SELECT * 
        FROM answer
        WHERE question_id= %(question_id)s
        """
    data = {'question_id': question_id}
    cursor.execute(query, data)
    return cursor.fetchall()


@database_common.connection_handler
def edit_question(cursor: RealDictCursor, id: int, title: str, message: str, image: str) -> list:
    query = """
        UPDATE question 
        SET title=%(title)s,message=%(message)s,image=%(image)s
        WHERE id=%(id)s
        """
    data = {'id': id, 'title': title, 'message': message, 'image': image}
    cursor.execute(query, data)
    update_query = """
        SELECT * FROM question
        WHERE id=%(id)s
        """
    data = {'id': id}
    cursor.execute(update_query, data)
    return cursor.fetchall()
    return cursor.fetchall()


@database_common.connection_handler
def delete_question(cursor: RealDictCursor, id: str) -> list:
    query = """
        DELETE FROM question
        WHERE id=%(id)s
        """
    data = {'id': id}
    cursor.execute(query, data)
    update_query = """
            SELECT * FROM question
            WHERE id=%(id)s
            """
    data = {'id': id}
    cursor.execute(update_query, data)
    return cursor.fetchall()

@database_common.connection_handler
def delete_answer_by_id(cursor: RealDictCursor, id: str) -> list:
    query = """
            DELETE FROM answer
            WHERE id=%(id)s
            """
    data = {'id': id}
    cursor.execute(query, data)
    update_query = """
                SELECT * FROM answer
                WHERE id=%(id)s
                """
    data = {'id': id}
    cursor.execute(update_query, data)
    return cursor.fetchall()

@database_common.connection_handler
def vote_up_question(cursor: RealDictCursor, id) -> list:
    query = """
                UPDATE question
                SET vote_number = vote_number+1
                WHERE id = %s
                """
    cursor.execute(query,(id,))

@database_common.connection_handler
def vote_down_question(cursor: RealDictCursor, id) -> list:
    query = """
                UPDATE question
                SET vote_number = vote_number-1
                WHERE id = %s
                """
    cursor.execute(query,(id,))

@database_common.connection_handler
def vote_up_answer(cursor: RealDictCursor, id) -> list:
    query = """
                UPDATE answer
                SET vote_number = vote_number+1
                WHERE id = %s
                """
    cursor.execute(query,(id,))

@database_common.connection_handler
def vote_down_answer(cursor: RealDictCursor, id) -> list:
    query = """
                UPDATE answer
                SET vote_number = vote_number-1
                WHERE id = %s
                """
    cursor.execute(query,(id,))

@database_common.connection_handler
def sort_questions(cursor: RealDictCursor, param, direction) -> list:
    query = """
            SELECT * FROM question ORDER BY {} {}
            """.format(param, direction)
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def view_question(cursor: RealDictCursor, id, view_number) -> list:
    query="""
        UPDATE question
                SET view_number = %(view_number)s+1
                WHERE id=%(id)s
                """
    data={'id':id, 'view_number':view_number}
    cursor.execute(query, data)

@database_common.connection_handler
def add_comment_question(cursor: RealDictCursor, question_id, message,submission_time) -> list:
    query = """
        INSERT INTO comment (question_id, message,submission_time)
        VALUES (%(question_id)s, %(message)s,%(submission_time)s)
        """
    data={'question_id':question_id,'message':message, 'submission_time':submission_time}
    cursor.execute(query, data)
    return "Comment added"

@database_common.connection_handler
def delete_coment_by_id_qu(cursor: RealDictCursor, comment_id) -> list:
      query = """
              DELETE FROM comment  
              WHERE id = %(comment_id)s
       """
      args = {'comment_id': comment_id}
      cursor.execute(query, args)
      return "Comment deleted"

@database_common.connection_handler
def search(cursor: RealDictCursor, phrase) -> list:
#     """
# another safer option
#      query = """
#             SELECT DISTINCT question.id AS id, question.submission_time AS submission_time ,
# question.view_number AS view_number, question.vote_number AS vote_number, question.title AS title,
# question.message AS message, question.image AS image, answer.id AS answer_id,
# answer.question_id AS answer_question_id, answer.submission_time AS answer_submission_time,
# answer.vote_number AS answer_vote_number, answer.message AS answer_message, answer.image AS answer_image
#             FROM question
#             LEFT OUTER JOIN answer
#             ON question.id = answer.question_id
#             WHERE question.title LIKE %(phrase)s
#             OR question.message LIKE %(phrase)s
#             OR answer.message LIKE %(phrase)s;
#             """
#     args = ({'phrase': '%' + phrase + '%'})
#     cursor.execute(query, args)
#     """

    query="""
        SELECT * FROM question WHERE title ILIKE '%{}%' OR message ILIKE '%{}%'
        """.format(phrase,phrase)
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def edit_answer(cursor: RealDictCursor, answer_id,message,image) -> list:
   query="""
        UPDATE answer
        SET message=%(message)s,image=%(image)s
        WHERE id = %(answer_id)s
        """
   args={'answer_id':answer_id,'message':message, 'image':image}
   cursor.execute(query,args)

@database_common.connection_handler
def edit_comment(cursor: RealDictCursor, comment_id,message,edited_count) -> list:
   query="""
        UPDATE comment
        SET message=%(message)s, edited_count=%(edited_count)s
        WHERE id = %(comment_id)s
        """
   args={'comment_id':comment_id,'message':message, 'edited_count':edited_count}
   cursor.execute(query,args)

@database_common.connection_handler
def add_answer_comment(cursor: RealDictCursor, answer_id,message,submission_time) -> list:
    query="""
         INSERT INTO comment (answer_id, message,submission_time)
        VALUES ( %(answer_id)s, %(message)s,%(submission_time)s)
        """
    data={'answer_id':answer_id,'message':message, 'submission_time':submission_time}
    cursor.execute(query, data)
    return "Comment added"

@database_common.connection_handler
def add_tag(cursor: RealDictCursor,name) -> list:
    query="""
        INSERt INTO tag (name) VALUES (%(name)s)
        """
    data={'name':name}
    cursor.execute(query, data)
    return "tag added"

@database_common.connection_handler
def add_tag_in_question_tag(cursor: RealDictCursor, question_id, tag_id) -> list:
    query = """
    INSERT INTO question_tag (question_id, tag_id)
    VALUES (%s, %s);
    """
    cursor.execute(query, (question_id, tag_id,))

@database_common.connection_handler
def delete_tag(cursor: RealDictCursor, question_id, tag_id) -> list:
    query = """
           DELETE FROM question_tag
           WHERE question_id = %(question_id)s AND tag_id = %(tag_id)s
       """
    args = {'question_id': question_id, 'tag_id': tag_id}
    cursor.execute(query, args)
    return "Tag deleted"





