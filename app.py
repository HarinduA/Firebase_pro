from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize Flask app
app = Flask(__name__)

# Path to your service account key JSON file
cred = credentials.Certificate('/Users/harinduadhikari/Documents/itemmy-firebase-adminsdk-lkzr9-9b824cfecd.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/')
def index():
    # Fetch items from Firestore
    items_ref = db.collection('items')
    docs = items_ref.stream()

    items = []
    for doc in docs:
        items.append(doc.to_dict())

    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item_code = request.form['itemCode']
        description = request.form['description']
        qty = int(request.form['qty'])
        price = float(request.form['price'])
        amount = qty * price
        
        item = {
            "itemCode": item_code,
            "description": description,
            "qty": qty,
            "price": price,
            "amount": amount
        }
        
        db.collection('items').add(item)
        return redirect(url_for('index'))
    
    return render_template('add_item.html')

if __name__ == '__main__':
    app.run(debug=True)
