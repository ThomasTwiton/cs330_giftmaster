from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from forms import AddPerson
import sqlite3

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'giftmaster'

#Routes#
@app.route('/add', methods=['GET', 'POST'])
def addform():
    addform = AddPerson()
    if addform.validate_on_submit():
        print(addform.first_name.data)
        print(addform.last_name.data)
        return render_template("add_forms.html", form1 = addform, msg1 ='Person added to roster')
    return render_template("add_forms.html", form1 = addform, msg1='')

if __name__=='__main__':
    app.run(debug=True)