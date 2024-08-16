from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Example in-memory storage (for demonstration purposes)
inventory_data = []
delivery_logs = []
out_of_stock_items = set()
order_requests = []  # Added for Order Request
form_management = []  # Placeholder for Form Management
inventory_tracking = []  # Placeholder for Inventory Tracking
order_reports = []  # Added for Order Report


@app.route('/')
def index():
    return render_template('layout.html')


@app.route('/analytics')
def analytics():
    return render_template('analytics.html')


@app.route('/inventory')
def inventory():
    return render_template('inventory.html')


@app.route('/orders')
def orders():
    return render_template('orders.html')


@app.route('/add_inventory', methods=['GET', 'POST'])
def add_inventory():
    if request.method == 'POST':
        item = request.form.get('item')
        uoi = request.form.get('uoi')
        beginning = float(request.form.get('beginning'))
        receive = float(request.form.get('receive'))
        sales = float(request.form.get('sales'))
        waste = float(request.form.get('waste'))
        ending = float(request.form.get('ending'))

        # Save the inventory data (for demonstration, just appending to a list)
        inventory_data.append({
            'item': item,
            'uoi': uoi,
            'beginning': beginning,
            'receive': receive,
            'sales': sales,
            'waste': waste,
            'ending': ending
        })

        return redirect(url_for('add_inventory'))  # Redirect to the same page to see updated data

    # Handle GET request to display the form and saved inventory data
    return render_template('add_inventory.html', inventory_records=inventory_data)


@app.route('/edit_inventory/<int:index>', methods=['GET', 'POST'])
def edit_inventory(index):
    if index < 0 or index >= len(inventory_data):
        return "Inventory record not found", 404

    if request.method == 'POST':
        item = request.form.get('item')
        uoi = request.form.get('uoi')
        beginning = float(request.form.get('beginning'))
        receive = float(request.form.get('receive'))
        sales = float(request.form.get('sales'))
        waste = float(request.form.get('waste'))
        ending = float(request.form.get('ending'))

        # Update the inventory data
        inventory_data[index] = {
            'item': item,
            'uoi': uoi,
            'beginning': beginning,
            'receive': receive,
            'sales': sales,
            'waste': waste,
            'ending': ending
        }

        return redirect(url_for('review_inventory'))  # Redirect to the inventory list

    # Handle GET request to display the edit form
    record = inventory_data[index]
    return render_template('edit_inventory.html', record=record, index=index)


@app.route('/monitor_inventory')
def review_inventory():
    return render_template('monitor_inventory.html', inventory_records=inventory_data)


@app.route('/supplier_report', methods=['GET', 'POST'])
def supplier_report():
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        delivery_id = request.form.get('delivery_id')
        quality_rating = int(request.form.get('quality_rating'))
        timeliness_rating = int(request.form.get('timeliness_rating'))
        issues = request.form.get('issues')

        # Save multiple deliveries for the same item
        delivery_logs.append({
            'item_id': item_id,
            'delivery_id': delivery_id,
            'quality_rating': quality_rating,
            'timeliness_rating': timeliness_rating,
            'issues': issues
        })

        return redirect(url_for('supplier_report'))  # Redirect to the same page to see updated data

    # Handle GET request to display the supplier report and delivery logs
    return render_template('supplier_report.html', delivery_logs=delivery_logs, out_of_stock_items=out_of_stock_items)


@app.route('/mark_out_of_stock', methods=['POST'])
def mark_out_of_stock():
    item_id = request.form.get('item_id')
    out_of_stock_items.add(item_id)
    return redirect(url_for('supplier_report'))  # Redirect to the supplier report page


@app.route('/waste_logs')
def waste_logs():
    return render_template('waste_logs.html')


@app.route('/generate_reports')
def generate_reports():
    return render_template('generate_reports.html')


@app.route('/export_data')
def export_data():
    return render_template('export_data.html')


@app.route('/logout')
def logout():
    # Clear the session data to log the user out
    session.clear()
    return redirect(url_for('index'))  # Redirect to the home page or login page


# New routes for Order Management
@app.route('/order_request', methods=['GET', 'POST'])
def order_request():
    if request.method == 'POST':
        order = request.form.get('order')
        # Add more fields as necessary
        order_requests.append({'order': order})
        return redirect(url_for('order_request'))  # Redirect to see updated data

    return render_template('order_request.html', orders=order_requests)


@app.route('/form_management', methods=['GET', 'POST'])
def form_management_page():
    if request.method == 'POST':
        form_name = request.form.get('form_name')
        form_description = request.form.get('form_description')

        # Append new form with 'Pending' status
        form_management.append({
            'id': len(form_management) + 1,
            'name': form_name,
            'description': form_description,
            'status': 'Pending'
        })

        return redirect(url_for('form_management_page'))

    return render_template('form_management.html', forms=form_management)


@app.route('/edit_form/<int:form_id>', methods=['GET', 'POST'])
def edit_form(form_id):
    form = next((f for f in form_management if f['id'] == form_id), None)
    if form is None:
        return "Form not found", 404

    if request.method == 'POST':
        form_name = request.form.get('form_name')
        form_description = request.form.get('form_description')

        form['name'] = form_name
        form['description'] = form_description

        return redirect(url_for('form_management_page'))

    return render_template('edit_form.html', form=form)


@app.route('/review_form/<int:form_id>', methods=['GET'])
def review_form(form_id):
    # Implement review logic here
    for form in form_management:
        if form['id'] == form_id:
            form['status'] = 'Reviewed'
            break
    return redirect(url_for('form_management_page'))


@app.route('/flag_form/<int:form_id>', methods=['GET'])
def flag_form(form_id):
    # Implement flag logic here
    for form in form_management:
        if form['id'] == form_id:
            form['status'] = 'Flagged'
            break
    return redirect(url_for('form_management_page'))


@app.route('/return_form/<int:form_id>', methods=['GET'])
def return_form(form_id):
    # Implement return logic here
    for form in form_management:
        if form['id'] == form_id:
            form['status'] = 'Returned'
            break
    return redirect(url_for('form_management_page'))


@app.route('/approve_form/<int:form_id>', methods=['GET'])
def approve_form(form_id):
    # Implement approval logic here
    for form in form_management:
        if form['id'] == form_id:
            form['status'] = 'Approved'
            break
    return redirect(url_for('form_management_page'))


@app.route('/inventory_tracking', methods=['GET', 'POST'])
def inventory_tracking_page():
    if request.method == 'POST':
        item_name = request.form['item']
        quantity = request.form['quantity']
        date = request.form['date']
        destination = request.form['destination']
        status = request.form['status']

        # Add the new inventory data to your storage (for demonstration, appending to the list)
        inventory_tracking.append({
            'item': item_name,
            'quantity': quantity,
            'date': date,
            'destination': destination,
            'status': status
        })

        # Optionally, redirect to avoid form resubmission on refresh
        return redirect(url_for('inventory_tracking_page'))

    # Render the template with inventory_items data
    return render_template('inventory_tracking.html', inventory_items=inventory_tracking)


@app.route('/order_report', methods=['GET'])
def order_report_page():
    # Retrieve the report data from the in-memory storage (for demonstration purposes)
    reports = order_reports  # Replace with your actual data retrieval logic

    # Render the template with the reports data
    return render_template('order_report.html', reports=reports)


if __name__ == '__main__':
    app.run(debug=True)
