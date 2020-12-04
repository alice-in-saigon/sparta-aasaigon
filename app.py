from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb://ID:PWa@13.209.35.193',27017)
db = client.dbsparta

# from openpyxl import load_workbook
# load_wb = load_workbook("C:/Users/Alice/Desktop/sparta/projects/saigon/test.xlsx")
# load_ws = load_wb['places']
#
# #엑셀파일 데이터 읽기
# for i in range(2, 42):
#     get_name = load_ws.cell(row = i, column = 1)
#     get_desc = load_ws.cell(row = i, column = 2)
#     get_tags = load_ws.cell(row = i, column = 3)
#     get_address = load_ws.cell(row = i, column = 4)
#     get_mapurl = load_ws.cell(row = i, column=5)
#     get_instaurl = load_ws.cell(row = i, column=6)
#     get_lat = load_ws.cell(row = i, column=7)
#     get_lng = load_ws.cell(row = i, column=8)
#
#
#
#     #place DB에 데이터 생성
#
#     place = {
#         'name': get_name.value,
#         'desc': get_desc.value,
#         'address': get_address.value,
#         'mapurl': get_mapurl.value,
#         'instaurl': get_instaurl.value,
#         'lat': get_lat.value,
#         'lng': get_lng.value,
#
#     }
#
#     db.places.insert_one(place)
#
#     # #tags DB에 데이터 생성
#     tags = get_tags.value.split(',')
#     for t in tags:  # t라는 변수안에 태그 이름이 하나씩 들어가게됨
#         t = t.strip()
#         tag_before = db.tags.find_one({'tag': t})
#         if tag_before is None:
#             db.tags.insert_one({'tag': t})

        # place = db.places.find_one({'name': get_name})
        # tag = db.tags.find_one({'tag': t})
        #
        # data = {
        #     'place_id': place['_id'],
        #     'tag_id': tag['_id']
        # }
        #
        # db.places_tags.insert_one(data)


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET'])
def registerPage():
    return render_template('register.html')

@app.route('/list', methods=['GET'])
def listPage():
    return render_template('list.html')






## API 역할을 하는 부분
@app.route('/places', methods=['POST'])
def makePlace():
    name_receive = request.form['name_give']
    desc_receive = request.form['desc_give']
    address_receive = request.form['address_give']
    mapurl_receive = request.form['mapurl_give']
    instaurl_receive = request.form['instaurl_give']
    tag_receive = request.form['tag_give']
    lat_receive = request.form['lat_give']
    lng_receive = request.form['lng_give']

    place = {
            'name': name_receive,
            'desc': desc_receive,
            'address': address_receive,
            'mapurl': mapurl_receive,
            'instaurl': instaurl_receive,
            'lat': lat_receive,
            'lng': lng_receive
    }

    db.places.insert_one(place)

    tags = tag_receive.split(',')
    for t in tags: #t라는 변수안에 태그 이름이 하나씩 들어가게됨
        t = t.strip()
        tag_before = db.tags.find_one({'tag':t})
        if tag_before is None:
            db.tags.insert_one({'tag':t})

        place = db.places.find_one({'name': name_receive})
        tag = db.tags.find_one({'tag': t})

        data = {
            'place_id':place['_id'],
            'tag_id': tag['_id']
        }

        db.places_tags.insert_one(data)

    return jsonify({'result': 'success', 'msg': '장소가 저장되었습니다'})



@app.route('/places', methods=['GET'])
def readPlace():
    # 태그 관련 장소 전부 검색
    places = db.places.find({})
    places_list = []
    for place in places:
        place_id = place['_id']
        # 장소와 관련있는 태그만 검색
        ts = db.places_tags.find({'place_id': place_id})
        # "카페, 한식, 사이공" 이런 식으로 태그가 연결될 최종 리스트
        # 아직 완성되지 않았으므로 빈 리스트로 시작
        tags = []
        # 검색한 태그들을 차례대로 꺼내서 tag 변수 안에 집어넣는다.
        for t in ts:
            tag_id = t['tag_id'] #tagid꺼냄
            obj_tag = db.tags.find_one({'_id': tag_id}) #tagid 검색 -> obj_tag 넣음
            tags.append(obj_tag['tag']) #tag 이름 가져옴
        # ObjectId 형태는 jsonify 가 안되기 때문에, str() 함수 이용하여 문자열 타입으로 변경
        place['_id'] = str(place['_id'])
        # tags 리스트에 담긴 녀석들을 ", "를 사이에 넣어서 문자열로 합친다.
        tag_names = ", ".join(tags)
        place['tags'] = tag_names
        places_list.append(place)

    return jsonify({'result': 'success', 'places': places_list, 'tags': list(db.tags.find({}, {'_id': False}))})




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
