"""Flask app factory"""
from flask import Flask, make_response, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

from src.uni.data_loader import fill_tables
from database import Database

from googletrans import Translator
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

# requests module will be used to CREATE client requests and send them to ANOTHER server
# from crypt import methods
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from src.news.data_loader import update

# Globally accessible libraries
# db = SQLAlchemy()
db = Database()
migrate = Migrate()
ma = Marshmallow()
QAmodel = AutoModelForQuestionAnswering.from_pretrained(
    "moska/deepset_bert-base-uncased-squad2_trained",
    use_auth_token="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",
)
sentence_model = SentenceTransformer("sentence-transformers/LaBSE")
tokenizer = AutoTokenizer.from_pretrained(
    "moska/deepset_bert-base-uncased-squad2_trained",
    use_auth_token="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",
)

jwt = JWTManager()


def create_app(config_class="config.DevConfig"):
    "initiate core application"
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)
    print(app.config["DEBUG"])

    CORS(app)
    api = Api(app)

    """initialize plugins"""
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    with app.app_context():
        # include routes
        from src.uni.routes.voivodeship_routes import (
            VoivodeshipIdApi,
            VoivodeshipsApi,
        )

        from src.uni.routes.course_routes import (
            CourseIdApi,
            CourseNameApi,
            CoursesApi,
        )

        from src.uni.routes.uni_routes import (
            UniIdApi,
            UniUidApi,
            # UniNameApi,
            UnisApi,
            CitiesApi,
        )

        from src.uni.routes.discipline_routes import (
            DisciplineIdApi,
            DisciplineNameApi,
            DisciplinesApi,
        )

        from src.uni.routes.level_routes import (
            CourseLevelIdApi,
            CourseLevelNameApi,
            CourseLevelsApi,
        )

        from src.uni.routes.search_routes import SearchUniApi, SearchCourseApi

        from src.forum.routes.topic_routes import (
            TopicIdApi,
            TopicNameApi,
            TopicsApi,
            TopicsInfoApi,
        )

        from src.forum.routes.thread_routes import (
            ThreadIdApi,
            ThreadsApi,
            ThreadsByTopicApi,
            ThreadIdInfoApi,
        )

        from src.forum.routes.post_routes import (
            PostIdApi,
            PostsApi,
            PostsByThreadApi,
        )

        from src.user.routes.user_routes import UserIdApi, UsersApi, UserAuthApi

        api.add_resource(VoivodeshipIdApi, "/voivodeships/<id>")
        api.add_resource(VoivodeshipsApi, "/voivodeships")

        api.add_resource(DisciplineIdApi, "/disciplines/<discipline_id>")
        api.add_resource(DisciplineNameApi, "/disciplines/name/<disciline_name>")
        api.add_resource(DisciplinesApi, "/disciplines")

        api.add_resource(CourseIdApi, "/courses/<course_id>")
        api.add_resource(CourseNameApi, "/courses/name/<course_name>")
        api.add_resource(CoursesApi, "/courses")

        api.add_resource(UniIdApi, "/unis/<uni_id>")
        api.add_resource(UniUidApi, "/unis/uid/<uni_uid>")
        # api.add_resource(UniNameApi, "/unis/name/<uni_name>")
        api.add_resource(UnisApi, "/unis")
        api.add_resource(CitiesApi, "/unis/cities")

        api.add_resource(CourseLevelIdApi, "/courses/levels/<level_id>")
        api.add_resource(CourseLevelNameApi, "/courses/levels/name/<level_name>")
        api.add_resource(CourseLevelsApi, "/courses/levels")

        api.add_resource(SearchUniApi, "/search/unis")
        api.add_resource(SearchCourseApi, "/search/courses")

        api.add_resource(TopicIdApi, "/forum/topics/<topic_id>")
        api.add_resource(TopicNameApi, "/forum/topics/name/<topic_name>")
        api.add_resource(TopicsApi, "/forum/topics")
        api.add_resource(TopicsInfoApi, "/forum/topics/info")

        api.add_resource(ThreadIdApi, "/forum/threads/<thread_id>")
        api.add_resource(ThreadsApi, "/forum/threads")
        api.add_resource(ThreadsByTopicApi, "/forum/topics/<topic_id>/threads")
        api.add_resource(ThreadIdInfoApi, "/forum/threads/<thread_id>/info")

        api.add_resource(PostIdApi, "/forum/posts/<post_id>")
        api.add_resource(PostsApi, "/forum/posts")
        api.add_resource(PostsByThreadApi, "/forum/threads/<thread_id>/posts")

        api.add_resource(UsersApi, "/users", endpoint="users")
        api.add_resource(UserIdApi, "/users/<user_id>", endpoint="user")
        api.add_resource(UserAuthApi, "/users/login")

        from src.currency.currency_routes import currency_routes
        from src.docs.docs_routes import docs_routes

        app.register_blueprint(currency_routes)
        app.register_blueprint(docs_routes)

        # db.create_all()
        print("db=====================================================")
        print(db.engine.url.database)

        # @app.before_first_request
        # @with_appcontext
        # def create_tables():
        #    db.Base.metadata.create_all(bind=db.engine)
        # fill_tables(db.engine.url.database)
    # delete everything from database, then run once, then comment it out

    # fill_forum_tables(db.engine.url.database)

    @app.after_request
    def after_request(response: Response) -> Response:
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, PATCH, DELETE"
        )
        response.headers.add("Access-Control-Allow-Headers", "x-csrf-token")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Headers", "Authorization")
        # response.headers.add("Access-Control-Allow-Headers", "Origin")
        # response.access_control_allow_headers = "Origin, Content-Type"
        # "Origin, X-Requested-With, Content-Type, Accept, Authorization"
        return response

    from src.currency.currency_routes import currency_routes
    from src.docs.docs_routes import docs_routes
    from src.map.map_routes import map_routes
    from src.qa.qa_routes import qa_routes

    app.register_blueprint(currency_routes)
    app.register_blueprint(map_routes, url_prefix="/map")
    app.register_blueprint(docs_routes)
    app.register_blueprint(qa_routes)
    from src.news.news_routes import news_routes

    app.register_blueprint(news_routes)
    return app
