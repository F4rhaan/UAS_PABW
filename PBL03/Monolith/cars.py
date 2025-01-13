from peewee import *
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

global appType 
appType = 'Monolith'

database = SqliteDatabase('carsweb.db')

class BaseModel(Model):
     class Meta:
        database = database

class TBCars(BaseModel):
    id = TextField()
    carname = TextField()
    carbrand = TextField()
    carmodel = TextField()
    carprice = TextField()

def create_tables():
    with database:
        database.create_tables([TBCars])

@app.route('/')
def indeks():
    return render_template('index.html', appType=appType)

@app.route('/createcar')
def createcar():
    return render_template('createcar.html', appType=appType)

@app.route('/createcarsave',methods=['GET','POST'])
def createcarsave():
    fName = request.form['carName']
    fBrand = request.form['carBrand']
    fModel = request.form['carModel']
    fPrice = request.form['carPrice']

    viewData = {
        "name" : fName,
        "brand" : fBrand,
        "model" : fModel,
        "price" : fPrice 
    }

    #simpan di DB
    car_simpan = TBCars.create(
        carname = fName,
        carbrand = fBrand,
        carmodel = fModel,
        carprice = fPrice
        )
    return redirect(url_for('readcar'))

@app.route('/readcar')
def readcar():
    rows = TBCars.select()
    return render_template('readcar.html', rows=rows, appType=appType)

@app.route('/updatecar')
def updatecar():
    return render_template('updatecar.html', appType=appType)

@app.route('/updatecarsave', methods=['GET','POST'])
def updatecarsave():
    fId = request.form['id']
    fName = request.form['carName']
    fBrand = request.form['carBrand']
    fModel = request.form['carModel']
    fPrice = request.form['carPrice']

    car_update = TBCars.update(
        carname=fName,
        carbrand=fBrand,
        carmodel=fModel,
        carprice=fPrice
    ).where(TBCars.id == fId)
    
    car_update.execute()
    return redirect(url_for('readcar'))
    # return render_template('updatecar.html', appType=appType)

@app.route('/deletecar')
def deletecar():
    return render_template('deletecar.html', appType=appType)

@app.route('/deletecarsave', methods=['GET','POST'])
def deletecarsave():
    fId = request.form['id']
    car_delete = TBCars.delete().where(TBCars.id==fId)
    car_delete.execute()
    return redirect(url_for('readcar'))

@app.route('/searchcar')
def searchcar():
    return render_template('searchcar.html', appType=appType)

@app.route('/searchcarinput', methods=['GET', 'POST'])
def searchcarinput():
    if request.method == 'POST':
        search_term = request.form.get('searchTerm')
        results = TBCars.select().where(TBCars.carname.contains(search_term))
        
        return render_template('searchcar.html', results=results)
    return render_template('searchcar.html')

@app.route('/help')  # Definisikan endpoint 'help'
def help():
    return render_template('help.html')

if __name__ == '__main__':
    create_tables()
    app.run(
        port =5010,
        host='0.0.0.0',
        debug = True
        )


