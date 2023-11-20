
from project_app import app
from flask import Flask, render_template

@app.route('/admin1')
def admin_dashboard():
    return render_template('admin/dashboard.html')

@app.route('/form')
def form():
    return render_template('admin/form.html')