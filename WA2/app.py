from flask import Flask, render_template, request, url_for, redirect, session, flash
import os
import csv
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

art_folder = 'static/art_uploads'
app.config['art_folder'] = art_folder
music_folder = 'static/music_uploads'
app.config['music_folder'] = music_folder
sports_folder = 'static/sports_uploads'
app.config['sports_folder'] = sports_folder
writing_folder = 'static/writing_uploads'
app.config['writing_folder'] = writing_folder



@app.route('/')
def index():
    if 'username' in session:
        return render_template("index.html")
    return render_template('login.html')

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('register'))
        #file closes after with block
        with open("users_info.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if username == row[0]:
                    flash("Username has been taken!")
                    return redirect(url_for('register'))

        user_info = [username, password]
        
        #file closes after with block
        with open("users_info.csv", "a",  newline='') as file:
            writer = csv.writer(file)
            writer.writerow(user_info)
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        #file closes after with block
        with open('users_info.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row == [username,password]:
                    session['username'] = username
                    return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout', methods=["POST"])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
            

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    username = session['username']
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'Please insert a file'
            
        if file:
            html_page = request.form['folder']
            if html_page == 'arts':
                path = app.config['art_folder']
            elif html_page == 'music':
                path = app.config['music_folder']
            elif html_page == 'sports':
                path = app.config['sports_folder']
            elif html_page == 'writing':
                path = app.config['writing_folder']
            else:
                return 'Invalid folder'
                
            filename = file.filename
            filepath = os.path.join(path, filename)
            file.save(filepath)
    
            description = request.form['description']
            likes = 0
            #file closes after with block
            with open('uploads.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([filename, description, html_page, likes,username])
        

            return redirect(url_for(html_page))

@app.route('/arts')
def arts():
    posts = {}
    #file closes after with block
    with open('uploads.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            filename, description, folder, likes, username = row
            if folder == 'arts':
                posts[filename] = [description, folder, likes, username]
    return render_template('arts.html', posts=posts)
    
@app.route('/sports')
def sports():
    posts = {}
    #file closes after with block
    with open('uploads.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            filename, description, folder, likes, username = row
            if folder == 'sports':
                posts[filename] = [description, folder, likes, username]
    return render_template('sports.html', posts=posts)

@app.route('/music')
def music():
    posts = {}
    #file closes after with block
    with open('uploads.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            filename, description, folder, likes, username = row
            if folder == 'music':
                posts[filename] = [description, folder, likes, username]
    return render_template('music.html', posts=posts)

@app.route('/writing')
def writing():
    posts = {}
    #file closes after with block
    with open('uploads.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            filename, description, folder, likes, username = row
            if folder == 'writing':
                posts[filename] = [description, folder, likes, username]
    return render_template('writing.html', posts=posts)

@app.route('/like', methods=['POST'])
def like():
    html_page = request.form['folder'].strip('/')
    filename = request.form['filename']
    updated_info = []
    #file closes after with block
    with open('uploads.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == filename:
                likes = int(row[3])
                likes += 1
                row[3] = str(likes)
            updated_info.append(row)
    #file closes after with block
    with open('uploads.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_info)
    return redirect(url_for(html_page))
    
    
    

@app.route('/feedback', methods=["POST","GET"])
def feedback():
    if request.method == "POST":
        comment = request.form.get('feedback')
        #file closes after with block
        with open('feedback.txt', 'a') as file:
            file.write(str(comment) + '\n')
    return render_template('feedback.html')

if __name__ == '__main__':
  app.run(debug=True, port=5000)
