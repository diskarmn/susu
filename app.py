
import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template,request,send_file,Response,url_for,redirect
from pymongo import MongoClient
import jwt  #token bukti akun verifikasi
import hashlib #mengacak kata menjadi kode random
from datetime import datetime,timedelta 

app = Flask(__name__)


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")
client = MongoClient(MONGODB_URI)
db=client[DB_NAME]
# client = MongoClient('mongodb://diskarmn:Diska123@ac-sjiapka-shard-00-00.3lnlkgx.mongodb.net:27017,ac-sjiapka-shard-00-01.3lnlkgx.mongodb.net:27017,ac-sjiapka-shard-00-02.3lnlkgx.mongodb.net:27017/?ssl=true&replicaSet=atlas-vnije0-shard-0&authSource=admin&retryWrites=true&w=majority')
# db = client.susu_mbak_siska

SECRET_KEY = 'kunci_token' 

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/pesan')
def pesan():
    return render_template('pesan.html')
@app.route('/online')
def online():
    return render_template('online.html')
#pembelian
@app.route('/beli', methods=['POST'])
def beli():
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')  
    nomor=db.pelanggan.count_documents({})
    urutan=nomor + 1
    file = request.files['file_give']
    nama=request.form.get('nama')
    nohp=request.form.get('nohp')
    pesan=request.form.get('pesan')
    fullcream=request.form.get('fullcream')
    coklat=request.form.get('coklat')
    strawberry=request.form.get('strawberry')
    taro=request.form.get('taro')
    red=request.form.get('red')
    total=request.form.get('total')
    waktu_beli=today.strftime('%Y-%m-%d-%H')  
    extension=file.filename.split('.')[-1]#jenis file
    namagambar= f'static/{mytime}.{extension}'#nama file
    file.save(namagambar)#save ke static
    db.pelanggan.insert_one({'nomor':urutan,'nama':nama,
    'nohp':nohp,'pesan':pesan,'fullcream':fullcream,
    'coklat':coklat,'strawberry':strawberry,'taro':taro,
    'redvelvet':red,'total':total,'waktu beli':waktu_beli,
    'file':namagambar,'status':'belum'})
    return jsonify({'message':'success','nama':nama,
    'nohp':nohp,'pesan':pesan,'fullcream':fullcream,
    'coklat':coklat,'strawberry':strawberry,'waktu_beli':waktu_beli,
    'taro':taro,'redvelvet':red,'total':total,'file':namagambar})

@app.route('/beli2', methods=['POST'])
def beli2():
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')  
    nomor=db.pelanggan.count_documents({})
    urutan=nomor + 1
    nama=request.form['nama']
    nohp=request.form['nohp']
    pesan=request.form['pesan']
    fullcream=request.form['fullcream']
    coklat=request.form['coklat']
    strawberry=request.form['strawberry']
    taro=request.form['taro']
    red=request.form['red']
    total=request.form['total']
    waktu_beli=today.strftime('%Y-%m-%d-%H')  
    db.pelanggan.insert_one({'nomor':urutan,'nama':nama,
    'nohp':nohp,'pesan':pesan,'fullcream':fullcream,
    'coklat':coklat,'strawberry':strawberry,'taro':taro,
    'redvelvet':red,'total':total,'waktu beli':waktu_beli,
    'file':'https://cdn-icons-png.flaticon.com/128/126/126122.png','status':'belum'})
    return jsonify({'message':'success','nama':nama,
    'nohp':nohp,'pesan':pesan,'fullcream':fullcream,
    'coklat':coklat,'strawberry':strawberry,'waktu_beli':waktu_beli,
    'taro':taro,'redvelvet':red,'total':total,'file':'kosong'})


@app.route("/admin")
def admin():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive,
                 SECRET_KEY, algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        return render_template("admin.html",
            nickname=user_info["nick"],file=user_info["file"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login",
            msg="Your login token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login",
            msg="There was an issue logging you in"))
@app.route('/login',methods=['GET'])
def login():
    msg=request.args.get('msg')
    return render_template('login.html',mgs=msg)
@app.route('/register',methods=['GET'])
def register():
    return render_template('register.html')


#tampil pesanan
@app.route('/tampilpesanan',methods=['GET'])
def tampilpesanan():
    pelanggan=list(db.pelanggan.find({},{'_id':False}))
    return jsonify({'pelanggan':pelanggan})
#update kirim pesanan
@app.route('/kirim',methods=['POST'])
def kirim():
    nomor=request.form['nomor']
    db.pelanggan.update_one(
        {'nomor':int(nomor)},
        {'$set':{'status':'sudah'}})
    return jsonify({'message':'success'})
#hapus pesanan
@app.route('/hapus',methods=['POST'])
def hapus():
    nomor2=request.form['nomor2']
    db.pelanggan.delete_one(
        {'nomor':int(nomor2)}) 
    return jsonify({'message':'success delete'})

    
#route api register
@app.route('/api/register',methods=['POST'])
def api_register():
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')  
    file = request.files['file_give']
    extension=file.filename.split('.')[-1]#jenis file
    namagambar= f'static/{mytime}.{extension}'#nama file
    file.save(namagambar)#save ke static

    id_receive=request.form.get('id_give')
    pw_receive=request.form.get('pw_give')
    nickname_receive=request.form.get('nickname_give')

    pw_hash=hashlib.sha256(pw_receive.encode('utf-8')).hexdigest() #mengenskripsi pw

    db.user.insert_one({
         'file':namagambar,
        'id':id_receive,
        'pw':pw_hash,
        'nick':nickname_receive})
    return  jsonify({'result':'success'})

#route api login
@app.route("/api/login", methods=["POST"])
def api_login():
    id_receive = request.form["id_give"]
    pw_receive = request.form["pw_give"]

    pw_hash = hashlib.sha256(pw_receive.encode("utf-8")).hexdigest()

    result = db.user.find_one({"id": id_receive, "pw": pw_hash})

    if result is not None:
        payload = {
                "id": id_receive,
                "exp": datetime.utcnow() + timedelta(days=1),}
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"result": "success", "token": token})
    else:
        return jsonify({"result": "fail", "msg": "Either your email or your password is incorrect"})
    
@app.route('/api/nick',methods=['GET'])
def api_valid():
    token_receive=request.cookies.get('mytoken')
    try:
        payload=jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256'] )
        print (payload)
        user_info=db.user.find_one({'id':payload.get('id')},{'_id':0})
        return jsonify({'result':'success',
                        'nickname':user_info.get('nick')})
    except jwt.ExpiredSignatureError:
        msg='token exp'
        return jsonify({'result':'fail', 'msg':msg})
    except jwt.exceptions.DecodeError:
        msg='issue login/problem'
        return jsonify({'result':'fail', 'msg':msg})
    


if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)