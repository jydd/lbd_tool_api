from flask import jsonify


def register_errors(bp):
    @bp.errorhandler(422)
    def handle_validation_error(e):
        exc = e.exc
        return jsonify(errors=exc.messages), 422

    @bp.errorhandler(404)
    def _handle_404_error(e):
        return jsonify(success=False, message=e.description)

    @bp.errorhandler(403)
    def handle_validation2_error(e):
        return jsonify(success=False, message=e.description)
