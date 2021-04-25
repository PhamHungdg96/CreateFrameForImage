import logging
from api.restplus import api
from flask_restplus import Resource
log = logging.getLogger(__name__)

ns = api.namespace('frame_print', description='create print with frame')

@ns.route('/')
class Hello(Resource):
    def get(self):
        """
        Returns list of blog posts.
        """
        return "HUNG"