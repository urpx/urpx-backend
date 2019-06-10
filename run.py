from urpx.app import create_app
from urpx.config import DevelopConfig

app = create_app(DevelopConfig)

if __name__ == '__main__':
    app.run('0.0.0.0', '8080')
