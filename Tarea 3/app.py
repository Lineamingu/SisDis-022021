from flask import render_template, request, redirect, url_for, Flask
import sys
import os
import psycopg2
from config import config
from config2 import configb 

app = Flask(__name__)




def connect(a,b,c,d):
    a=a.lower()
    b=b.lower()
    d=d.lower()
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        cur.execute("insert into products (brand_name, items_description, prices, category) values (%s,%s,%s,%s)", (a,b,c,d))
        conn.commit()

        # display the PostgreSQL database server version
        #db_response= cur.fetchall()
        #print(db_response)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')




def connect2(search):
    """ Connect to the PostgreSQL database server """
    conn = None
    search=search.lower()
    search='%'+search+'%'      
    try:
        # read connection parameters
        params = configb()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        cur.execute("SELECT * FROM products WHERE brand_name  LIKE %s OR items_description  LIKE %s OR category LIKE %s",(search,search,search))
        #cur.execute("SELECT * FROM products WHERE brand_name  LIKE %"+'%s'+"% OR items_description  LIKE %"+'%s'+"%  OR category LIKE %"+'%s'+"% ",(search,search,search))
        #conn.commit()

        # display the PostgreSQL database server version
        db_response= list(cur.fetchall())
        #print(db_response)
        result=db_response
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return result


@app.route("/main", methods=["GET", "POST"])
def main_page():
    pid = os.getpid()
    if request.method == 'POST':
        # ------------solicitud de ingreso---------------
        brand_name = request.form['brand_name']
        items_description = request.form['items_description']
        prices = request.form['prices']
        category = request.form['category']
        #print(brand_name, items_description, prices, category)

        connect(brand_name,items_description,prices,category)

        return redirect(url_for('main_page'))

    return render_template('index.html', nro=pid)


@app.route("/search_results", methods=["GET", "POST"])
def product_search():
    # print('a')
    if request.method == 'GET':
        # print('b')
        # ------------solicitud de busqueda-------------
        search = request.args.get('search')
        #print(search)

        results=connect2(search)
        final_results={}
        a=0
        for i in results:
            final_results[a]=i
            a+=1
        print (final_results)

        return render_template('results.html', final_results=final_results)

    return "No hay nada para buscar"
