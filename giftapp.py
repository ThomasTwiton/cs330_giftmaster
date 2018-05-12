from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from forms import AddPerson, AddDate, AddGift, QueryGift
import records
import sqlite3

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
            +str(dateform.date.data) + '", "'
            +dateform.description.data + '")'
        )
        return render_template("add_forms.html", form1 = dateform, msg1='Date recorded')

    return render_template("add_forms.html", form1 = dateform, msg1='')

@app.route('/add_gift', methods=['GET', 'POST'])
def addgift():
    db = records.Database('sqlite:///giftmaster.db')
    res=db.query('select first_name, last_name, id from roster_test')

    giftform = AddGift()
    giftform.person.choices = []

    for name in res:
        pid = name.id
        display = name.first_name + " " + name.last_name
        giftform.person.choices += [(pid, display)]

    if giftform.validate_on_submit():
        db.query('insert into gift_test values ("'
            +giftform.person.data + '", "'
            +giftform.gift.data + '", "'
            +giftform.link.data + '")'
        )
        return render_template("add_forms.html", form1 = giftform, msg1='Gift idea recorded')

    return render_template("add_forms.html", form1 = giftform, msg1='')

@app.route('/roster')
def getroster():
    conn = sqlite3.connect('giftmaster.db')
    cur = conn.cursor()
    cur.execute('select first_name, last_name, relationship, nickname, middle_name from roster_test')
    res = cur.fetchall()
    return render_template("roster.html", data = res, theader = cur)

@app.route('/upcoming_dates')
def getdates():
    conn = sqlite3.connect('giftmaster.db')
    cur = conn.cursor()
    cur.execute('select roster_test.first_name, roster_test.last_name, date_test.eventdescription, date_test.eventdate from date_test join roster_test on roster_test.id=date_test.id where date_test.eventdate >= date("now") order by date_test.eventdate')
    res = cur.fetchall()
    return render_template("dates.html", data = res, theader = cur)

@app.route('/gift_ideas', methods=['GET', 'POST'])
def getgifts():
    db = records.Database('sqlite:///giftmaster.db')
    res=db.query('select first_name, last_name, id from roster_test')

    selectperson = QueryGift()
    selectperson.person.choices = []

    for name in res:
        pid = name.id
        display = name.first_name + " " + name.last_name
        selectperson.person.choices += [(pid, display)]
    
    if selectperson.validate_on_submit():
        conn = sqlite3.connect('giftmaster.db')
        cur = conn.cursor()
        cur.execute(('select gift_test.giftidea, gift_test.url from gift_test join roster_test on roster_test.id=gift_test.id where roster_test.id=="'+selectperson.person.data+'"'))
        res = cur.fetchall()

        return render_template('ideas.html', form1=selectperson, ideasfor = selectperson.person.data, data=res)
    return render_template('ideas.html', form1=selectperson, ideasfor='', data=[])



if __name__=='__main__':
    app.run(debug=True)