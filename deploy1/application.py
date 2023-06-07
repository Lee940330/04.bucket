from flask import Flask, render_template, request, jsonify
application = app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.eouggot.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']

    bucket_list = list(db.bucket.find({}, {'_id': False}))
    count = len(bucket_list) + 1
    doc = {
        'num':count,  #버킷 등록 시, db에서 특정 버킷을 찾기 위해 'num' 이라는 고유 값 부여
        'bucket' :bucket_receive,
        'done' : 0   #'done' key값을 추가 해 각 버킷의 완료 상태 구분(0 = 미완료, 1 = 완료)
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})

@app.route("/bucket/reset", methods=["POST"])
def reset_done():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 0}})



@app.route("/bucket", methods=["GET"])
def bucket_get():
    all_buckets = list(db.bucket.find({},{'_id':False}))
    return jsonify({'result':all_buckets})

if __name__ == '__main__':
    app.run()



# //////////////////////////////////////////////////////



# from flask import Flask, render_template, request, jsonify
# app = Flask(__name__)

# from pymongo import MongoClient
# client = MongoClient('mongodb+srv://test:sparta@cluster0.rpcfu.mongodb.net/Cluster0?retryWrites=true&w=majority')
# db = client.dbsparta


# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route("/bucket", methods=["POST"])
# def bucket_post():
#     bucket_receive = request.form['bucket_give']

#     bucket_list = list(db.bucket.find({}, {'_id': False}))
#     count = len(bucket_list) + 1

#     doc = {
#         'num': count,
#         'bucket': bucket_receive,
#         'done': 0
#     }
#     db.bucket.insert_one(doc)



#     return jsonify({'msg': '버킷 기록 완료!!!'})




# @app.route("/bucket/done", methods=["POST"])
# def bucket_done():
#     num_receive = request.form['num_give']
#     db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})


#     return jsonify({'msg': '버킷을 달성하셨군요 축하드려요!!'})



# @app.route("/bucket/reset", methods=["POST"])
# def reset_done():
#     num_receive = request.form['num_give']

#     db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 0}})


#     return jsonify({'msg': '버킷달성을 취소하였습니다. 다음번에는 꼭 이루시길!'})




# @app.route("/bucket", methods=["GET"])
# def bucket_get():
#     bucket_list = list(db.bucket.find({}, {'_id': False}))

#     return jsonify({'buckets': bucket_list})




# if __name__ == '__main__':
#     app.run('0.0.0.0', port=5000, debug=True)