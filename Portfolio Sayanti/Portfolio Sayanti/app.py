from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

app.secret_key = os.getenv('FLASK_SECRET_KEY')

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]
        sender_email = request.form.get("email", "no-reply@example.com")

        try:
            msg = Message(
                subject=f"New Message from {name}",
                sender=sender_email,
                recipients=["your_email@gmail.com"],
                body=f"Name: {name}\nEmail: {sender_email}\n\nMessage:\n{message}"
            )
            mail.send(msg)
            flash("✅ Your message has been sent successfully!")
        except Exception as e:
            print(e)
            flash("❌ Failed to send message. Please try again later.")
        return redirect(url_for("contact"))
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)
