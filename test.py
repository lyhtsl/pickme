from flask import Flask,request
from flask import request
import time
import json
import pymssql
import traceback
from time import sleep


class PYSQL(object):


    def __init__(self, host1, user1, password1, database1):
        self.conn = pymssql.connect(host1, user1, password1,database1)
        self.cursor = self.conn.cursor()

    def insert_date(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except:
            print(traceback.format_exc())
            self.conn.rollback()
            return False

    def update_data(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            print(traceback.format_exc())
            self.conn.rollback()

    def delete_data(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            print(traceback.format_exc())
            self.conn.rollback()

    def select_data(self, sql):
        self.cursor.execute(sql)

        all_data = self.cursor.fetchall()
        return all_data

    def close(self):
        self.cursor.close()
        self.conn.close()
        print("关闭数据库")



user = 'test'
pwd = 'test'
app = Flask(__name__)
order_number = 1
# 查询是否有订单未完成
# 反馈实时位置
# 查询订单状态

#查询订单记录（type为0是租客，为1是车主）
@app.route('/users/record')
def getusers_record():
    username = request.args.get('user')
    type = request.args.get('type')
    my = PYSQL('127.0.0.1', 'sa', 'lin123456.', 'pickme')
    data = []
    if int(type) == 0:
        sql = "SELECT * FROM orders WHERE susername = '{}' ORDER BY orderid DESC".format(username)
        data1 = my.select_data(sql)
        for vi in data1:
            data2 = {"oid": vi[0], "duser": vi[2], "fast_car": vi[3], "free_car": vi[4], "rent_car": vi[5], "finish": vi[6], "saddress": vi[7], "eaddress": vi[8], "sdate": vi[9], "stime": vi[10], "edate": vi[11], "etime": vi[12], "price": vi[13], "cycle": vi[14]}
            data.append(data2)

    else:
        sql = "SELECT * FROM orders WHERE dusername = '{}' ORDER BY orderid DESC".format(username)
        data1 = my.select_data(sql)
        for vi in data1:
            data2 = {"oid": vi[0], "suser": vi[1], "fast_car": vi[3], "free_car": vi[4], "rent_car": vi[5],
                     "finish": vi[6], "saddress": vi[7], "eaddress": vi[8], "sdate": vi[9], "stime": vi[10],
                     "edate": vi[11], "etime": vi[12], "price": vi[13], "cycle": vi[14]}
            data.append(data2)
    status = 0
    res = {
        "status": status,
        "data": data
        }
    my.close()
    return json.dumps(res, ensure_ascii=False)

#短租车查询未完成订单（type为0是租客，为1是车主）
@app.route('/rentcar/finish')
def getRentcar_finish():
    username = request.args.get('user')
    type = request.args.get('type')
    my = PYSQL('127.0.0.1', 'sa', 'lin123456.', 'pickme')

    if int(type) == 1:
        sql = "select * from orders where finish is NULL and dusername='{}'".format(username)
        result = my.select_data(sql)
        # print(result)
        if result:
            status = 1
            data = []
            if result[0][1]:

                msg = '你有未完成订单'
                dd = result[0]
                sql1 = "select sname,stel from student where susername='{}'".format(dd[1])
                dn = my.select_data(sql1)
                print(dn)
                if dn:
                    data = {"oid": dd[0], "sname": dn[0][0] ,"stel": dn[0][1],"address": dd[7],"sdate": dd[9],
                            "edate": dd[11], "cycle":dd[14],"price": dd[13] }
            else:
                msg = '你的订单待匹配'
                dd = result[0]
                data = {"oid": dd[0],  "address": dd[7], "sdate": dd[9],
                        "edate": dd[11], "cycle": dd[14], "price": dd[13]}
            res = {
                "status": status,
                "msg": msg,
                "data": data
            }
        else:
            status = -1
            msg = "没有进行中订单"
            res = {
                "status": status,
                "msg": msg,
            }
    else:
        sql = "select * from orders where finish is NULL and susername='{}'".format(username)
        result = my.select_data(sql)
        print(result)
        if result:
            status = 1
            msg = '你有未完成订单'
            dd = result[0]
            sql1 = "select dname,dtel from driver where dusername='{}'".format(dd[2])
            dn = my.select_data(sql1)
            print(dn)
            data = {"oid": dd[0], "dname": dn[0][0], "dtel": dn[0][1], "address": dd[7], "sdate": dd[9], "edate": dd[11], "cycle": dd[14], "price": dd[13]}
            res = {
                "status": status,
                "msg": msg,
                "data": data
            }
        else:
            status = -1
            msg = "没有进行中订单"
            res = {
                "status": status,
                "msg": msg,
            }
    my.close()
    return json.dumps(res, ensure_ascii=False)

# passager get driver rentcar data 乘客获取可租信息
@app.route('/rentcar/data')
def getRentcar_data():
    sdate = request.args.get("sdate")
    edate = request.args.get("edate")
    data = []
    my = PYSQL('127.0.0.1', 'sa', 'lin123456.', 'pickme')
    sql = "SELECT orderid,dusername,startpoint,cycle ,price FROM orders WHERE susername is NULL AND rent_car = 1 AND  sdate = '{}' AND edate = '{}'".format(sdate, edate)
    data1 = my.select_data(sql)
    for vi in data1:
        sql = "SELECT dname,dtel FROM driver WHERE dusername = '{}'".format(vi[1])
        data2 = my.select_data(sql)
        data3 = data2[0]
        data4 = {"oid": vi[0], "address": vi[2], "cycle": vi[3], "price": vi[4], "name": data3[0], "tel": data3[1]}
        data.append(data4)


    '''
    requery database
    '''
    my.close()
    res = {
        "status": 0,#0请求成功
        "data": data
    }
    return json.dumps(res)

# passager take rent car order 乘客租车
@app.route('/driver/rentcar/tkod')
def takeRentOrder():
    oid = request.args.get("oid")
    user = request.args.get("user")
    my = PYSQL('127.0.0.1', 'sa', 'lin123456.', 'pickme')
    sql = "UPDATE orders SET susername ='{}' WHERE orderid = '{}'".format(user,oid)
    my.update_data(sql)
    my.close()
    '''
    updata database
    '''
    res = {
        "status": 0,
        "msg": "seccess",
        "data": {

        }
    }
    return json.dumps(res)


# passager release rent car order 车主发布租车订单
@app.route('/rentcar/release')
def releaseRentar():
    did = request.args.get("did")
    sdate = request.args.get("sdate")
    #stime = request.args.get("stime")
    edate = request.args.get("edate")
    #etime = request.form.get("etime")
    adress = request.args.get("adr")
    price = request.args.get("price")
    cycle = request.args.get("cycle")
    my = PYSQL('127.0.0.1', 'sa', 'lin123456.', 'pickme')
    sql = "INSERT INTO orders(dusername,rent_car,sdate,edate,startpoint,price,cycle) VALUES ('{}',1 ,'{}','{}','{}','{}','{}')".format(did, sdate, edate, adress, price, cycle)
    my.insert_date(sql)
    sql = "SELECT orderid FROM orders WHERE dusername = '{}' AND rent_car=1 AND sdate = '{}' AND edate = '{}' AND startpoint = '{}' AND price = '{}' AND cycle ='{}'".format(did, sdate, edate, adress, price, cycle)
    data1 = my.select_data(sql)
    data = data1[0]
    my.close()

    '''
    add into database
    '''
    res = {
        "status": 0,
        "msg": "success",
        "oid": data[0]
    }
    return json.dumps(res)

# owner take rent car order 乘客接出租订单并返回乘客信息
@app.route('/driver/rentcar/tkod', methods=['POST'])
def takerentdata():
    oid = request.args.get("oid")
    driver_id = request.args.get("did")
    '''
    updata database
    '''
    res = {
        "status": 0,
        "data": {
            "msg": "seccess"
        }
    }
    return json.dumps(res)

# owner get tail wind car order data 车主获取订单数据
@app.route('/driver/rentcar/data')
def getRent_data():
    oid = request.args.get("oid")
    my = PYSQL('127.0.0.1', 'sa', 'lin123456.', 'pickme')
    sql ="SELECT susername FROM orders WHERE orderid = '{}'".format(oid)
    data1 = my.select_data(sql)
    data2 = data1[0]
    print(data2)
    if data2[0] == None:
        res = {
            "status": 0,
            "msg": "Nobody rents this car"
        }

    else:
        sql ="SELECT sname,ssex,stel FROM student WHERE susername = '{}'".format(data2[0])
        data3 = my.select_data(sql)
        data4 = data3[0]
        data5 = {"name": data4[0], "sex": data4[1], "tel": data4[2]}
        res = {
            "status": 0,
            "msg": "seccess",
            "data": data5
        }

    my.close()
    return json.dumps(res)

# passager get driver data 乘客获取司机信息
@app.route('/quikcar/data')
def getquikcar_data():
    oid = request.args.get("oid")
    '''
    requery database
    '''
    my = PYSQL('127.0.0.1', 'sa', 'lin123456.', 'pickme')
    sql = "SELECT dusername FROM orders WHERE orderid = '{}'".format(oid)
    did1 = my.select_data(sql)
    did2 = did1[0]
    did = did2[0]
    sql = "SELECT dname,dsex,year(getdate())-year(dbirth),cycletype,dtel FROM driver WHERE dusername = '{}'".format(did)
    suer1 = my.select_data(sql)
    suer = suer1[0]
    res = {
        "status": 0,
        "data": {
            "msg": "seccess",
            "username": did,
            "name": suer[0],
            "sex": suer[1],
            "age": suer[2],
            "type": suer[3],
            "tel":suer[4]
        }
    }
    return json.dumps(res, ensure_ascii=False)
# driver take quik car order 司机接快车订单
@app.route('/driver/quikcar/tkod')
def takeQcOrder():
    oid = request.args.get("oid")
    driverid = request.args.get("did")
    print(oid)
    print(driverid)
    '''
    updata database
    '''
    my = PYSQL('127.0.0.1', 'sa', 'lin123456.', 'pickme')
    sql = "UPDATE orders SET dusername ='{}' WHERE orderid ='{}'".format(driverid, oid)
    my.update_data(sql)
    sql = "SELECT susername FROM orders WHERE orderid = '{}'".format(oid)
    susername1 = my.select_data(sql)
    susername2 = susername1[0]
    susername = susername2[0]
    sql = "SELECT sname,ssex,year(getdate())-year(sbirth),stel FROM student WHERE susername = '{}'".format(susername)
    suer1 = my.select_data(sql)
    suer = suer1[0]
    res = {
        "status": 0,
        "data": {
            "msg": "seccess",
            "username": susername,
            "name": suer[0],
            "sex": suer[1],
            "age": suer[2],
            "tel": suer[3]
        }
    }
    return json.dumps(res, ensure_ascii=False)


# passager release quik car order 乘客发布快车订单  价钱待加
@app.route('/quikcar/release')
def releaseQcar():
    username = request.args.get("user")
    startPlace = request.args.get("stp")
    destination = request.args.get("des")
    date = request.args.get("date")
    time = request.args.get("time")

    '''
    add into database
    '''
    my = PYSQL('127.0.0.1', 'sa', 'lin123456.', 'pickme')
    sql = "INSERT INTO orders(susername,fast_car,startpoint,endpoint,sdate,stime) VALUES('{}',1,'{}','{}','{}','{}')".format(username,startPlace,destination, date,time)
    my.insert_date(sql)
    sql =  "SELECT orderid FROM orders WHERE susername='{}' AND startpoint ='{}' AND endpoint = '{}'AND sdate ='{}'AND stime ='{}'".format(username, startPlace, destination, date,time)
    orderid1 = my.select_data(sql)

    my.close()
    orderid2 = orderid1[0]
    orderid = orderid2[0]
    res = {
        "status": 0,
        "msg": "success",
        "data": {"oid": orderid}
        }
    return json.dumps(res)

# driver get tail wind car order data 司机获取订单数据(order 代表订单类型1是快车，2是顺风车)
@app.route('/driver/twc/data')
def getTwc_data():
    order = request.args.get("order")
    date = request.args.get("date")
    time1 = request.args.get("time1")
    time2 = request.args.get("time2")
    data =[]
    '''
    requery database
    '''
    if order[0] =='1':
        my = PYSQL('127.0.0.1', 'sa', 'lin123456.', 'pickme')
        sql = "SELECT orderid,susername,startpoint,endpoint, price FROM orders WHERE dusername is NULL AND fast_car = 1 AND  sdate = '{}' AND stime BETWEEN '{}' AND '{}'".format(
            date, time1, time2)
        data1 = my.select_data(sql)
        for vi in data1:
            susername = vi[1]
            sql = "SELECT sname ,ssex,year(getdate())-year(sbirth)FROM student WHERE susername = '{}'".format(susername)
            data2 = my.select_data(sql)
            data3 = data2[0]
            data4 = {"oid": vi[0], "startpoint": vi[2], "endpoint": vi[3], "price":vi[4], "name": data3[0], "sex": data3[1],
                     "age": data3[2]}
            data.append(data4)
    else:
        my = PYSQL('127.0.0.1', 'sa', 'lin123456.', 'pickme')
        sql = "SELECT orderid,susername,startpoint,endpoint ,price FROM orders WHERE dusername is NULL AND free_ride = 1 AND  sdate = '{}' AND stime BETWEEN '{}' AND '{}'".format(
            date, time1, time2)
        data1 = my.select_data(sql)
        for vi in data1:
            susername = vi[1]
            sql = "SELECT sname ,ssex,year(getdate())-year(sbirth)FROM student WHERE susername = '{}'".format(susername)
            data2 = my.select_data(sql)
            data3 = data2[0]
            data4 = {"oid": vi[0], "startpoint": vi[2], "endpoint": vi[3], "price": vi[4], "name": data3[0], "sex": data3[1],
                     "age": data3[2]}
            data.append(data4)
    res = {
        "status": 0,
        "data": data
    }
    my.close()
    return json.dumps(res, ensure_ascii=False)
# driver take tail wind car order 司机接顺风车订单并返回乘客信息
@app.route('/driver/twc/tkod', methods=['POST'])
def takeTwcOrder():
    oid = request.form.get("oid")
    driverid = request.form.get("did")
    '''
    updata database
    '''
    my = PYSQL('127.0.0.1', 'sa', 'lin123456.', 'pickme')
    sql = "UPDATE orders SET dusername ='{}' WHERE orderid ='{}'".format(driverid,oid)
    my.update_data(sql)
    sql = "SELECT susername FROM orders WHERE orderid = '{}'".format(oid)
    susername1 = my.select_data(sql)
    susername2 =susername1[0]
    susername = susername2[0]
    sql = "SELECT sname,ssex,year(getdate())-year(sbirth),stel FROM student WHERE susername = '{}'".format(susername)
    suer1 = my.select_data(sql)
    suer = suer1[0]
    res = {
        "status": 0,
        "data": {
            "msg": "seccess",
            "username":susername,
            "name":suer[0],
            "sex":suer[1],
            "age":suer[2],
            "tel":suer[3]
        }
    }
    return json.dumps(res, ensure_ascii=False)

# passager Release tail wind car order 乘客发布顺风车订单   价钱待加
@app.route('/twcar/release')
def releaseTwcOrder():
    username = request.args.get("user")
    startPlace = request.args.get("stp")
    destination = request.args.get("des")
    date = request.args.get("date")
    time = request.args.get("time")
    '''
    add into database
    '''
    my = PYSQL('127.0.0.1', 'sa', 'lin123456.', 'pickme')
    sql = "INSERT INTO orders(susername,free_ride,startpoint,endpoint,sdate,stime) VALUES('{}',1,'{}','{}','{}','{}')".format(username,startPlace,destination, date,time)
    my.insert_date(sql)
    sql =  "SELECT orderid FROM orders WHERE susername='{}' AND startpoint ='{}' AND endpoint = '{}'AND sdate ='{}'AND stime ='{}'".format(username, startPlace, destination, date,time)
    orderid1 = my.select_data(sql)

    my.close()
    orderid2 = orderid1[0]
    orderid = orderid2[0]
    res = {
        "status": 0,
        "msg": "success",
        "data": {"oid": orderid}
    }
    return json.dumps(res)

# get adress and position 获取地址和坐标
@app.route('/pos')
def get_pos():

    return "Function not completed"

# refund 退押金
@app.route('/refund')
def refund():
    oid = request.args.get("oid")
    '''
    query database
    '''
    my = PYSQL('127.0.0.1', 'sa', 'lin123456.', 'pickme')
    sql = "SELECT deposit FROM orders WHERE orderid ='{}'".format(oid)
    deposit1 =my.select_data(sql)
    sql = "UPDATE orders SET deposit=0 WHERE orderid ='{}'".format(oid)
    my.update_data(sql)
    my.close()
    deposit2 = deposit1[0]
    deposit = deposit2[0]

    if deposit:
        msg = "success return {} yuan to you".format(deposit)
        '''
        updata database
        '''
    else:
        msg = "you have not ever deposit"
    res = {
        "status": 0,
        "msg": msg
    }
    return json.dumps(res)

# query is_deposit 交押金
@app.route('/query/deposit')
def query_deposit():
    oid = request.args.get("oid")
    deposit = request.args.get("deposit")
    print(oid)
    print(deposit)
    '''
    query database
    '''
    if deposit:
        my = PYSQL('127.0.0.1', 'sa', 'lin123456.', 'pickme')
        sql ="UPDATE orders SET deposit={} WHERE orderid ='{}'".format(deposit, oid)
        my.update_data(sql)
        my.close()
        status = 0
        msg = 'success'
    else:
        status = -1
        msg = 'fail'
    res = {
        "status": status,
        "msg":msg,
        "data": {"is_deposit": deposit}
    }
    return json.dumps(res)


# is deposit 判断是否已交押金
@app.route('/deposit')
def deposit():

    oid = request.args.get("oid") #订单号
    print(oid)
    '''
    add into database
    '''
    my = PYSQL('127.0.0.1', 'sa', 'lin123456.', 'pickme')
    sql = "SELECT deposit FROM orders WHERE orderid ='{}'".format(oid)
    data1 = my.select_data(sql)
    my.close()
    if data1:
        msg = 'success'
        status = 0
    else:
        msg = 'fail'
        status = -1
    res = {
        "status": status,
        "msg": msg
    }
    return json.dumps(res)


# valid 认证
@app.route('/driver/valid', methods=['POST'])
def dri_valid():
    username = request.form.get("user")
    name = request.form.get("name")
    sex = request.form.get("sex")
    idnum = request.form.get("idnum")
    # carnum = request.form.get("carnum")
    con = pymssql.connect('127.0.0.1', 'test', '123', 'pickme')
    cursor = con.cursor()
    sql = "SELECT dusername FROM driver where dusername='{}'".format(username)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        msg = 'you have already register'
    else:

        sql = "SELECT userid FROM driver where userid='{}'".format(idnum)
        cursor.execute(sql)
        idout = cursor.fetchone()
        if idout == None:
            sql = "insert into driver(dusername,dname,dsex,userid) values('{}','{}','{}','{}')".format(username, name, sex, idnum)
            con.commit()
    cursor.close()
    res = {
        "status": 0,
        "msg": "success"
    }
    return json.dumps(res)


# get info 获取用户信息
@app.route('/info')
def get_info():
    username = request.args.get("user")
    print(username)
    '''
    query database
    '''
    my = PYSQL('127.0.0.1', 'DESKTOP-Q15FB3G\SQLEXPRESS', '55007', 'sa', 'lin123456.', 'pickme')
    # print(cursor)
    sql = "SELECT username FROM users where username='{}'".format(username)
    res = my.select_data(sql)

    if res == None:
        msg = 'can not find the user'
    else:
        sql = "SELECT dusername FROM driver where dusername='{}'".format(username)
        res = my.select_data(sql)
        if res ==None:
            sql = "SELECT stel,userid,sname,ssex,sbirth FROM student where susername='{}'".format(username)
            suer1 = my.select_data(sql)
            suer = suer1[0]
            res = {
                "status": 0,
                "data": {
                    "msg": "seccess",
                    "username": username,
                    "tel": suer[0],
                    "userid": suer[1],
                    "name": suer[2],
                    "sex": suer[3],
                    "birth": suer[4]
                }
            }
        else:
            sql = "SELECT dtel,userid,dname,dsex,dbirth FROM driver where dusername='{}'".format(username)
            suer1 = my.select_data(sql)
            suer = suer1[0]
            res = {
                "status": 0,
                "data": {
                     "msg": "seccess",
                     "username": username,
                     "tel": suer[0],
                     "userid": suer[1],
                     "name": suer[2],
                     "sex": suer[3],
                     "birth": suer[4]
                }
            }

        '''
        return result
        '''
        msg = 'success'
        my.close()

    return json.dumps(res, ensure_ascii=False)


# register 注测
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('user')
    password = request.form.get('pwd')
    # identify = request.form.get('identify')
    '''
    add new user into database
    '''
    con = pymssql.connect('127.0.0.1', 'test', '123', 'pickme')
    cursor = con.cursor()
    # print(cursor)
    sql = "SELECT username FROM users where username='{}'".format(username)
    cursor.execute(sql)
    res = cursor.fetchone()
    if res == None:
        sql = "insert into users values('{}','{}')".format(username, password)
        cursor.execute(sql)
        con.commit()
        msg = 'success'
    else:
           msg = 'username has been registered'
    # res = cursor.fetchone()
    # print(res)
    cursor.close()
    res = {
        "status": 0,
        "msg": msg
    }
    return json.dumps(res)


# login 登录
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('user')
    password = request.form.get('pwd')
    # identify = request.form.get('identify')
    if username == None or password == None:
        res = {
            "status": 1000,
            "msg": "a bad way to request"
        }
        return json.dumps(res)
    '''
    query database
    '''

    con = pymssql.connect('127.0.0.1', 'test', '123', 'pickme')
    cursor = con.cursor()
    # print(cursor)
    cursor.execute("SELECT username,userpwd FROM users")
    res = cursor.fetchone()
    # print(res)
    user = res[0].strip()
    pwd = res[1].strip()

    cursor.close()
    if username == user and password == pwd:
        res = {
            "status": 0,
            "msg": "success"
        }
        return json.dumps(res)
    else:
        res = {
            "status": 0,
            "msg": "username or password is not match"
        }
        return json.dumps(res)

@app.route('/requery') # type=0:p?driver
def isoddone():
    username = request.args.get('user')
    type = request.args.get('type')
    my = PYSQL('127.0.0.1', 'DESKTOP-Q15FB3G\SQLEXPRESS', '55007', 'sa', 'lin123456.', 'pickme')

    if int(type) == 0:
        sql = "select * from orders where finish is NULL and susername='{}'".format(username)
        result = my.select_data(sql)
        # print(result)
        if result:
            status = 1
            data = []
            if result[0][2]:

                msg = '你有未完成订单'
                dd = result[0]
                sql1 = "select dname,dtel,cycleinfo from driver where dusername='{}'".format(dd[2])
                dn = my.select_data(sql1)
                print(dn)
                if dn:
                    data = {"oid":dd[0],"dname":dn[0][0], "st": dd[7], "isfast": dd[3], "isfree": dd[4], "end": dd[8], "dtel":dn[0][1], "cycleinfo":dn[0][2]}
            else:
                msg = '你的订单待匹配'

            res = {
                "status": status,
                "msg": msg,
                "data": data
            }
        else:
            status = -1
            msg = "没有进行中订单"
            res = {
                "status": status,
                "msg": msg,
            }
    else:
        sql = "select * from orders where finish is NULL and dusername='{}'".format(username)
        result = my.select_data(sql)
        print(result)
        if result:
            status = 1
            msg = '你有未完成订单'
            dd = result[0]
            sql1 = "select sname,stel from student where susername='{}'".format(dd[1])
            dn = my.select_data(sql1)
            print(dn)
            data = {"oid": dd[0], "sname": dn[0][0], "st": dd[7], "isfast": dd[3], "isfree": dd[4], "end": dd[8], "stel":dn[0][1]}
            res = {
                "status": status,
                "msg": msg,
                "data": data
            }
        else:
            status = -1
            msg = "没有进行中订单"
            res = {
                "status": status,
                "msg": msg,
            }
    my.close()
    return json.dumps(res, ensure_ascii=False)

@app.route('/',methods=['GET', 'POST'])
def hello_world():
    print('\nconnect in {}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    #print(request.form.get('user'))
    # req = request.get_data()

    #print(type(j))
    # print(json.loads(s))
    return 'Hello World!\nwelcome to PICKME'


if __name__ == '__main__':
    # app.run(host="www.pickmi.club", port=8090)
    app.run(host='0.0.0.0', port=80)
    # 6bf6c9ddca23383f