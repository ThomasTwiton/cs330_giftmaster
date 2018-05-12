from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from forms import AddPerson, AddDate
import records

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'giftmaster'

#Routes#
@app.route('/add_roster', methods=['GET', 'POST'])
def addpeople():
    addform = AddPerson()

    if addform.validate_on_submit():
        #print(addform.first_name.data)
        db = records.Database('sqlite:///giftmaster.db')
        db.query('insert into roster_test values ("'
            +addform.first_name.data+'", "'
            +addform.last_name.data+'", "'
            +addform.middle_name.data+'", "'
            +addform.nickname.data+'", "'
            +addform.relationship.data+'", "'
            +(addform.first_name.data + addform.last_name.data+ addform.middle_name.data + addform.nickname.data + addform.relationship.data)
            + '")'
        )
        return render_template("add_forms.html", form1 = addform, msg1 ='Person added to roster')
    return render_template("add_forms.html", form1 = addform, msg1='')

@app.route('/add_date', methods=['GET', 'POST'])
def adddate():
    db = records.Database('sqlite:///giftmaster.db')
    res=db.query('select first_name, last_name, id from roster_test')

    dateform = AddDate()
    dateform.person.choices = []

    for name in res:
        pid = name.id
        display = name.first_name + " " + name.last_name
        dateform.person.choices += [(pid, display)]

    if dateform.validate_on_submit():
        db.query('insert into date_test values ("'
            +dateform.person.data + '", "'
            +dateform.date.data + '", "'
            +dateform.description.data + '")'
        )
        return render_template("add_forms.html", form1 = dateform, msg1='Date added to person')

    return render_template("add_forms.html", form1 = dateform, msg1='')

    

if __name__=='__main__':
    app.run(debug=True)