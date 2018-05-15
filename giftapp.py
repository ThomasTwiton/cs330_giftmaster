from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from forms import AddPerson, AddDate, AddGift, QueryGift, Login
import records
import sqlite3

#default database tables#
class Tables():
    roster = "roster_test"
    gift = "gift_test"
    date = "date_test"

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'giftmaster'
tables = Tables()

#Routes#
@app.route('/add_roster', methods=['GET', 'POST'])
def addpeople():
    addform = AddPerson()

    if addform.validate_on_submit():
        #print(addform.first_name.data)
        db = records.Database('sqlite:///giftmaster.db')
        db.query('insert into ' + tables.roster + ' values ("'
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
    res=db.query('select first_name, last_name, id from '+tables.roster)

    dateform = AddDate()
    dateform.person.choices = []

    for name in res:
        pid = name.id
        display = name.first_name + " " + name.last_name
        dateform.person.choices += [(pid, display)]

    if dateform.validate_on_submit():
        db.query('insert into ' + tables.date +' values ("'
            +dateform.person.data + '", "'
            +str(dateform.date.data) + '", "'
            +dateform.description.data + '")'
        )
        return render_template("add_forms.html", form1 = dateform, msg1='Date recorded')

    return render_template("add_forms.html", form1 = dateform, msg1='')

@app.route('/add_gift', methods=['GET', 'POST'])
def addgift():
    db = records.Database('sqlite:///giftmaster.db')
    res=db.query('select first_name, last_name, id from ' + tables.roster)

    giftform = AddGift()
    giftform.person.choices = []

    for name in res:
        pid = name.id
        display = name.first_name + " " + name.last_name
        giftform.person.choices += [(pid, display)]

    if giftform.validate_on_submit():
        db.query('insert into ' + tables.gift +' values ("'
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
    cur.execute('select first_name, last_name, relationship, nickname, middle_name from '+ tables.roster)
    res = cur.fetchall()
    return render_template("roster.html", data = res, theader = cur)

@app.route('/upcoming_dates')
def getdates():
    conn = sqlite3.connect('giftmaster.db')
    cur = conn.cursor()
    cur.execute('select '+tables.roster+'.first_name, '+tables.roster+'.last_name, '+tables.date+'.eventdescription, '+tables.date+'.eventdate from '+tables.date+' join '+tables.roster+' on '+tables.roster+'.id='+tables.date+'.id where '+tables.date+'.eventdate >= date("now") order by '+tables.date+'.eventdate')
    res = cur.fetchall()
    return render_template("dates.html", data = res, theader = cur)

@app.route('/gift_ideas', methods=['GET', 'POST'])
def getgifts():
    db = records.Database('sqlite:///giftmaster.db')
    res=db.query('select first_name, last_name, id from '+tables.roster)

    selectperson = QueryGift()
    selectperson.person.choices = []

    for name in res:
        pid = name.id
        display = name.first_name + " " + name.last_name
        selectperson.person.choices += [(pid, display)]
    
    if selectperson.validate_on_submit():
        conn = sqlite3.connect('giftmaster.db')
        cur = conn.cursor()
        cur.execute(('select '+tables.gift+'.giftidea, '+tables.gift+'.url from '+tables.gift+' join '+tables.roster+' on '+tables.roster+'.id='+tables.gift+'.id where '+tables.roster+'.id=="'+selectperson.person.data+'"'))
        res = cur.fetchall()

        return render_template('ideas.html', form1=selectperson, ideasfor = selectperson.person.data, data=res)
    return render_template('ideas.html', form1=selectperson, ideasfor='', data=[])

@app.route('/login', methods=['GET', 'POST'])
def login():
    logger=Login()
    if logger.validate_on_submit():
        tables.roster = ("roster_" + logger.username.data)
        tables.gift = ("gift_" + logger.username.data)
        tables.date = ("date_" + logger.username.data)
        #print([roster, gift, date])
        db = records.Database('sqlite:///giftmaster.db')
        db.query('create table if not exists '+ tables.roster + '(first_name text, last_name text, middle_name text, nickname text, relationship text, id text)')
        db.query('create table if not exists ' + tables.gift + '(id text, giftidea text, url text)')
        db.query('create table if not exists ' + tables.date + '(id text, eventdate date, eventdescription)')

        return render_template('login.html', form1=logger, msg= ('Logged in as '+ logger.username.data))
    return render_template('login.html', form1=logger, msg='')


if __name__=='__main__':
    app.run(debug=True)