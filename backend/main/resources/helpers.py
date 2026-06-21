from flask import request, jsonify


def paginated_response(service, dto_class, items_key, **filter_fields):
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    filters = {"page": page, "per_page": per_page}
    for key, param in filter_fields.items():
        value = request.args.get(param)
        if value is not None:
            filters[key] = value
    result = service.get_all(filters)
    return jsonify({
        items_key: [dto_class.full(x) for x in result.items],
        'total': result.total,
        'pages': result.pages,
        'page': page
    })
