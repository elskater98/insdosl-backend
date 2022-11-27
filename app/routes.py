import json
import tempfile
import base64
from flask import jsonify, request
from geoalchemy2.functions import ST_FlipCoordinates, ST_AsGeoJSON
from app.models import Canalization, Rd008
from app import app, db, telegram_bot

from config import Config


@app.route('/')
def index():
    return 'It works'


@app.route('/canalization', methods=['GET'])
def canalization():
    return jsonify([
            {
                'description': c.description,
                'geom': json.loads(c.geom),
            } for c in db.session.query(ST_AsGeoJSON(ST_FlipCoordinates(
                        Canalization.geom)).label('geom'),
                Canalization.description).limit(500)])


@app.route('/rd008', methods=['GET', 'POST', 'DELETE'])
def canal():
    if request.method == 'POST':
        if ('latitude' not in request.json or
                'longitude' not in request.json):
            return jsonify({'error': 'Missing photo or geo field'}), 400
        db.session.add(Rd008(
                id=Rd008.query.with_entities(Rd008.id).order_by(
                    Rd008.id.desc()).first()[0] + 1,
                photo=request.json.get('photo'),
                type=request.json.get('type'),
                description=request.json.get('description'),
                geom=(
                "SRID=4326;POINT(%s %s)" % (request.json['longitude'],
                        request.json['latitude'])),
        ))
        db.session.commit()
        telegram_bot.send_message(Config.TELEGRAM_NOTIFICATION_USERS,
            """<b>Nova imatge - %s</b>
            S'ha pujat nova informació.
            """ % request.json.get('description') or ' ',
            parse_mode='html')
        if 'photo' in request.json and request.json['photo']:
            with tempfile.NamedTemporaryFile() as tmp:
                if len(request.json['photo'].split('base64,')) <= 1:
                    tmp.write(base64.decodebytes(request.json['photo'].encode()
                            ))
                else:
                    tmp.write(base64.decodebytes(request.json['photo'].split(
                                    'base64,')[1].encode()))
                tmp.seek(0)
                telegram_bot.send_photo(Config.TELEGRAM_NOTIFICATION_USERS,
                    photo=tmp)
        return jsonify({'success': 1})
    elif request.method == 'DELETE':
        if 'id' in request.json:
            db.session.delete(Rd008.query.filter_by(
                    id=request.json.get('id')))
            db.session.commit()
            return jsonify({'success': 1})
    return jsonify([
            {
                'id': c.id,
                'photo': c.photo,
                'geom': json.loads(c.geom),
                'description': c.description,
                'type': c.type,
            } for c in db.session.query(Rd008.photo, Rd008.description,
                Rd008.type, Rd008.Id,
                ST_AsGeoJSON(ST_FlipCoordinates(Rd008.geom)).label('geom'))])
