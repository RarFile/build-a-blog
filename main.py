from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:hamham11!@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# creating a persistent class for the database

class Blog(db.Model):

    # specify the data fields that should go into columns

    id = db.Column(db.Integer, primary_key=True)     # start with primary ID
    
    # these are both set as Text instead of String so there is not a character limit
    
    title = db.Column(db.Text)  # blog title
    post = db.Column(db.Text)   # blog post text

    def __init__(self, title, post):
        self.title = title
        self.post = post 

# DISPLAYS ALL BLOG POSTS
#@app.route('/blog')
#def index():
    # queries database for all existing blog entries
    # all_blog_posts = Blog.query.all()
    # first of the pair matches to {{}} in for loop in the .html template, second of the pair matches to variable declared above
    # return render_template('blog.html', posts=all_blog_posts)

# DISPLAYS IND BLOG POSTS
@app.route('/blog')
def show_blog():
    post_id = request.args.get('id')
    if (post_id):
        ind_post = Blog.query.get(post_id)
        return render_template('ind_post.html', ind_post=ind_post)
    else:
        # queries database for all existing blog entries
        # post_id = request.args.get('id')
        all_blog_posts = Blog.query.all()
        # first of the pair matches to {{}} in for loop in the .html template, second of the pair matches to variable declared above
        return render_template('blog.html', posts=all_blog_posts)


# VALIDATION FOR EMPTY FORM
def empty_val(x):
    if x:
        return True
    else:
        return False

# THIS HANDLES THE REDIRECT (SUCCESS) AND ERROR MESSAGES (FAILURE)

@app.route('/newpost', methods=['POST', 'GET'])
def add_entry():

    if request.method == 'POST':

        # THIS CREATES EMPTY STRINGS FOR THE ERROR MESSAGES

        title_error = ""
        blog_entry_error = ""

        # assigning variable to blog title from entry form

        post_title = request.form['blog_title']

        # assigning variable to blog post from entry form
        
        post_entry = request.form['blog_post']
        
        # creating a new blog post variable from title and entry
        
        post_new = Blog(post_title, post_entry)

        # if the title and post entry are not empty, the object will be added
        
        if empty_val(post_title) and empty_val(post_entry):
        
            # adding the new post (this matches variable created above) as object 
        
            db.session.add(post_new)
        
            # commits new objects to the database
        
            db.session.commit()
            post_link = "/blog?id=" + str(post_new.id)
            return redirect(post_link)
        else:
            if not empty_val(post_title) and not empty_val(post_entry):
                title_error = "Please enter text for blog title"
                blog_entry_error = "Please enter text for blog entry"
                return render_template('new_post.html', blog_entry_error=blog_entry_error, title_error=title_error)
            elif not empty_val(post_title):
                title_error = "Please enter text for blog title"
                return render_template('new_post.html', title_error=title_error, post_entry=post_entry)
            elif not empty_val(post_entry):
                blog_entry_error = "Please enter text for blog entry"
                return render_template('new_post.html', blog_entry_error=blog_entry_error, post_title=post_title)

    # DISPLAYS NEW BLOG ENTRY FORM

    else:
        return render_template('new_post.html')
        

# only runs when the main.py file run directly

if __name__ == '__main__':
    app.run()