from flask import Flask, request, make_response, render_template, send_file
from werkzeug.utils import secure_filename
from os.path import isfile, splitext
from time import time
import sqlite3 as sql
from datetime import datetime
from pytz import timezone
from shutil import rmtree
from os import mkdir
tz = timezone('Asia/Kolkata')
ftime = '%m-%d %I:%M %p'

app = Flask(__name__)
static = app.root_path + r'/static/'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    try:
        file=request.files['file']
        name=file.filename
        size=request.form['size']
        date = datetime.now(tz).strftime(ftime).lstrip('0')
        f,ext=splitext(name)
        con,c=connect()
        if not existDB(c):
            createDB(c)
            print('database created')
        ind = c.execute("select max(ind) from nn").fetchone()[0]
        if ind==None:
            ind=1
        else:
            ind+=1
        realname='f'+str(ind)+ext
        fname=static+r'files/'+realname
        file.save(fname)
        insert(c,ind,name,size,date,realname)
        print('inserted ',ind,name,size,date,realname)
        close(con)
        
        rep = make_response({'code':0, 'msg':'f'+str(ind)+ext, 'date':date})
    except Exception as e:
        rep = make_response({'code':1, 'msg':str(e)})
    rep.headers['Access-Control-Allow-Origin']='*';
    return rep

@app.route('/load/<x>')
def myicon(x):
    rep = make_response(send_file(static+r'files/'+x))
    rep.headers['Access-Control-Allow-Origin']='*';
    return rep

@app.route('/allfiles')
def allfiles():
    try:
        con, c = connect()
        if not existDB(c):
            ans=[]
        else:
            ans = c.execute("select * from nn order by ind desc").fetchall()
        close(con)
        rep = make_response({'code':0, 'msg':ans})
    except Exception as e:
        rep = make_response({'code':1, 'msg':str(e)})
    rep.headers['Access-Control-Allow-Origin']='*';
    return rep


@app.route('/query', methods=['POST'])
def askme():
    try:
        q=request.form['q']
        con, c = connect()
        ans = query(c,q)
        close(con)
        rep = make_response({'code':0, 'msg':ans})
    except Exception as e:
        rep = make_response({'code':1, 'msg':str(e)})
    rep.headers['Access-Control-Allow-Origin']='*';
    return rep

@app.route('/clear')
def deleteAllFies():
    rmtree(static+r'files')
    mkdir(static+r'files')
    con,c=connect()
    clearDB(c)
    close(con)
    rep = make_response('deleted all files')
    rep.headers['Access-Control-Allow-Origin']='*';
    return rep

def connect():
    con = sql.connect('nn')
    return con, con.cursor()
def close(conn):
    conn.commit()
    conn.close()

def existDB(c):
    return c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='nn'").fetchone()
def createDB(c):
    c.execute("create table nn (ind integer, name text, size text, date text, realname text)")
def clearDB(c):
    c.execute("drop table nn");
    createDB(c);

def insert(c,ind,name,size,date,rname):
    c.execute("insert into nn values (?,?,?,?,?)",(ind,name,size,date,rname))

def query(c,q):
    return c.execute(q).fetchall()



    
