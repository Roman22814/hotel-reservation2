from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory "database"
reservations = {}
reservation_id = 1

@app.route('/', methods=['GET', 'POST'])
def reservation():
    global reservation_id
    if request.method == 'POST':
        data = {
            'id': reservation_id,
            'name': request.form['name'],
            'email': request.form['email'],
            'checkin': request.form['checkin'],
            'checkout': request.form['checkout'],
            'room': request.form['room'],
            'payment': False
        }
        reservations[reservation_id] = data
        rid = reservation_id
        reservation_id += 1
        return redirect(url_for('payment', rid=rid))
    return render_template('reservation.html')

@app.route('/payment/<int:rid>', methods=['GET', 'POST'])
def payment(rid):
    if request.method == 'POST':
        reservations[rid]['payment'] = True
        return redirect(url_for('confirmation', rid=rid))
    return render_template('payment.html', rid=rid)

@app.route('/confirmation/<int:rid>')
def confirmation(rid):
    data = reservations.get(rid)
    return render_template('confirmation.html', data=data)

@app.route('/cancel/<int:rid>')
def cancel(rid):
    reservations.pop(rid, None)
    return "Reservation Cancelled"

if __name__ == '__main__':
    app.run(debug=True)