from flask import Flask, render_template


app = Flask(__name__, template_folder='templates')


@app.route('/')
def hello_world():

    img = './static/entity.svg'
    return render_template('base.html', img=img)


if __name__ == '__main__':
    app.run()
