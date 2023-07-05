import re
from http import HTTPStatus

from flask import jsonify, request

from yacut import app, db
from yacut.constants import REG_EXPRESSION
from yacut.error_handlers import APIErrors
from yacut.models import URLMap
from yacut.views import check_short_id, get_db_object, get_unique_short_id


@app.route("/api/id/", methods=["POST"])
def create_short_link():
    data = request.get_json()
    if not data:
        raise APIErrors("Отсутствует тело запроса", HTTPStatus.BAD_REQUEST)
    if "url" not in data:
        raise APIErrors('"url" является обязательным полем!',
                        HTTPStatus.BAD_REQUEST)
    if "custom_id" in data:
        custom_id = data.get("custom_id")
        if not check_short_id(custom_id):
            raise APIErrors(f'Имя "{custom_id}" уже занято.',
                            HTTPStatus.BAD_REQUEST)
        if custom_id == "" or custom_id is None:
            data["custom_id"] = get_unique_short_id()
        elif not re.match(REG_EXPRESSION, custom_id):
            raise APIErrors(
                "Указано недопустимое имя для короткой ссылки",
                HTTPStatus.BAD_REQUEST
            )
    else:
        data["custom_id"] = get_unique_short_id()
    new_url = URLMap()
    new_url.from_dict(data)
    db.session.add(new_url)
    db.session.commit()
    return jsonify(new_url.to_dict()), HTTPStatus.CREATED


@app.route("/api/id/<short_id>/", methods=["GET"])
def get_original_url(short_id):
    try:
        db_object = get_db_object(URLMap.short, short_id).first()
        if db_object is None:
            return jsonify(
                {"message": "Указанный id не найден"}
            ),HTTPStatus.NOT_FOUND
        return jsonify({"url": db_object.original}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
