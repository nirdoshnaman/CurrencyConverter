from curr_converter import create_app
import os


config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == "__main___":
    app.run(debug=True)