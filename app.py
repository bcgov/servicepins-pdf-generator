from flask import Flask, render_template, request, make_response
from flask_cors import CORS

from pdf import form

app = Flask(__name__)
CORS(app)

@app.get("/")
def home():
    return render_template("conversion.html")

# converts the form information into new pdf from template
@app.post("/convert")
def convert():

    #pull out data from request form
    supervisor = request.form['supervisorName']
    prefix = request.form['prefix']
    streetAddress = request.form['streetAddress']
    cityTown = request.form['cityTown']
    postal = request.form['postal']
    ministry = request.form['ministry']
    province = request.form['province']
    staff = []

    #create staffing array
    for x in range(1,7):
        if(request.form[f'employee{x}']):
            employee = [request.form[f'employee{x}']]
            years = request.form.getlist(f'employee{x}years')
            yearList = ""
            for each in years:
                    yearList += f"{each} years, "
            yearList = yearList[0:-2]
            employee.append(yearList)
            staff.append(employee)

    supervisor = {
                'superName': supervisor, 'address': f'{prefix} {streetAddress}, <br/> {cityTown} {postal}', 'prefix': prefix, 'street_address': streetAddress, 'postal': postal, 'city_town': cityTown, 'ministry': ministry, 'staff': staff, 'province': province}
    response = make_response(form(supervisor))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = \
            'attachment; filename=%s.pdf' % supervisor['superName']
    try:
        return response
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=False)