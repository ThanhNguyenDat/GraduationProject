from flask import Flask

server = Flask(__name__,
            static_url_path='',
            static_folder='src/static',
            template_folder='src/templates', )
