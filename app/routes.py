import json
from flask import jsonify, request
from app.models import Canalization, Rd008
from app import app, db


@app.route('/')
def index():
    return 'It works'


@app.route('/canalization', methods=['GET'])
def canalization():
    return jsonify([
            {
                'description': c.description,
                'geom': json.loads(c.geom),
            } for c in db.session.query(Canalization.geom.ST_AsGeoJSON(
                    ).label('geom'),
                Canalization.description)])


@app.route('/rd008', methods=['GET', 'POST'])
def canal():
    if request.method == 'POST':
        if ('photo' not in request.json or 'latitude' not in request.json or
                'longitude' not in request.json):
            return jsonify({'error': 'Missing photo or geo field'}), 400
        db.session.add(Rd008(
                id=Rd008.query.with_entities(Rd008.id).order_by(
                    Rd008.id.desc()).first()[0] + 1,
                photo=request.json['photo'],
                description=request.json.get('description'),
                geom=(
                "SRID=4326;POINT(%s %s)" % (request.json['longitude'],
                        request.json['latitude'])),
        ))
        db.session.commit()
        return jsonify({'success': 1})
    return jsonify([
            {
                'photo': c.photo,
                'geom': json.loads(c.geom),
                'description': c.description,
            } for c in db.session.query(Rd008.photo, Rd008.description,
                Rd008.geom.ST_AsGeoJSON().label('geom'))])
