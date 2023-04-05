from flask import Flask, render_template, request, redirect, url_for, session,redirect

from datetime import datetime
import os

import pyrebase


app = Flask(__name__)
app.secret_key = os.urandom(24)


config = {
    "apiKey": "AIzaSyDAesz3zK6oVrspQg0t8VPymG34v_0LIkQ",
    "authDomain": "dusocietyhub.firebaseapp.com",
    "databaseURL": "https://dusocietyhub.firebaseio.com",
    "projectId": "dusocietyhub",
    "storageBucket": "dusocietyhub.appspot.com",
    "messagingSenderId": "111278657030"

}

firebase = pyrebase.initialize_app(config)


db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()



@app.route("/")
def index():

    #db.child("Clubs").push("Nowrin Hossain")


    #return redirect(url_for("create_class"))
    return render_template("index.html")




@app.route("/signIn_signUp")
def userReg():

    #db.child("Clubs").push("Nowrin Hossain")


    #return redirect(url_for("create_class"))
    return render_template("signIn_signUp.html")


@app.route("/signUp", methods=['GET','POST'])
def signUp():

    if request.method=='POST':
        username = str(request.form["newuser"])
        department = str(request.form["new_user_dept"])
        regNo = str(request.form["reg_no"])
        email = str(request.form["new_user_email"])
        password = str(request.form["new_user_pass"])

        if len(password)>=6:
            auth.create_user_with_email_and_password(email, password)
            db.child("Users").push({
                "Username":username,
                "Department":department,
                "Registration_No":regNo,
                "Email":email
            })
    return render_template("signIn_signUp.html")



@app.route("/signIn", methods=['GET','POST'])
def signIn():
    if request.method=='POST':
        email                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 = str(request.form["userMail"])
        password = request.form["pass"]

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for("all_clubs"))


        except:
            render_template("signIn_signUp.html",err='Unsucessfull')
            #return redirect(url_for(signIn,err='Unsucessfull'))



    return render_template("signIn_signUp.html")







@app.route("/all_clubs.html", methods=['GET'])
def all_clubs():

    club_list_db = db.child("Clubs").get()
    club_list = club_list_db.val().values()
    print(club_list_db.val().values())


    return render_template("all_clubs.html",club_list = club_list)


@app.route("/profile", methods=['POST','GET'])
def profile():

    try:
        club_code = session['club_signed_in']
        club_name = session['club_name']
    except:
        print()

    clubs = db.child("Clubs").get()
    all_clubs_info = clubs.val()

    infos = []
    for club in all_clubs_info:
        infos.append(all_clubs_info[club])

    club_info = []
    for u in infos:
        if u["name"] == club_name:
            club_info = u
            break


    if request.method=='POST':


        postType = request.form['post_type']
        text_post = request.form['club_post']
        try:
            img_file = request.files['image_post']
        except:
            print()
        now = str(datetime.now())

        #storage.child('post_image').put(img_file)

        db.child("Post").push({
            "name":club_name,
            "postType":postType,
            "post":text_post,
            "Image_link":None,
            "time":now
            })

        print(postType+text_post)
        return render_template("user_profile.html", club_name=club_name,club_info=club_info)

    return render_template("user_profile.html",club_name=club_name,club_info=club_info)



@app.route("/create_class")
def create_class():

    #db.child("Clubs").push("Nowrin Hossain")

    return render_template("create_class.html")

@app.route("/club_reg", methods=['GET','POST'])
def club_reg():

    if request.method == 'POST':
        club_name= str(request.form["club_name"])
        club_code= request.form["club_code"]
        club_info = str(request.form["club_info"])
        club_location = str(request.form["location"])
        cpassword = str(request.form["password"])


        db.child("Clubs").push({"name":club_name,
                                "code":club_code,
                                "description":club_info,
                                "location":club_location,
                                "pass":cpassword
                                })
        #db.child("Clubs").push("Nowrin Hossain")

        return redirect(url_for("all_clubs"))

    #return render_template("create_class.html")




@app.route("/view_post", methods=['POST','GET'])
def view_post():

    club_name= request.args.get('club')

    clubs = db.child("Clubs").get()
    all_clubs_info = clubs.val()

    infos = []
    for club in all_clubs_info:
        infos.append(all_clubs_info[club])

    club_info=[]
    for u in infos:
        if u["name"]==club_name:
            club_info = u
            break

    posts = db.child("Post").get().val()

    post_list=[]
    for i in posts:
        post_list.append(posts[i])

    this_club_posts=[]
    for i in post_list:
        if i["name"]==club_name:
            this_club_posts.append(i)

    print(this_club_posts)


    return render_template("view_club_page.html", club_info=club_info,all_posts=this_club_posts)



@app.route("/member_request_form",methods=['GET','POST'])
def member_request_form():
    club_name = request.args.get('club')

    #print("uporer Club Name: ")print(club_name)

    session['request_club'] = club_name

    if request.method=='POST':

        name = request.form['user']
        reg = request.form['reg']
        contact = request.form['contact']
        dept = request.form['dept']
        year = request.form['year']
        sess = request.form['session']

        hall = request.form['hall_name']

        print("Eitai ")
        try:
            this_club = session['request_club']
            print(this_club)
        except:
            print("Hoy nai")

        db.child('StudentInfo').push({
            "name": name,
            "department": dept,
            "hall": hall,
            "session":sess,
            "contact":contact,
            "registration":reg,
            "club":"Dhaka University IT Society"
        })
        return redirect(url_for("all_clubs"))
    return render_template("member_request_form.html")





@app.route("/club_signIn", methods=['GET','POST'])
def club_signIn():

    if request.method=='POST':
        code = request.form['club_code']
        passc = str(request.form['pass'])

        clubs = db.child("Clubs").get()
        #print(users_by_score)
        all_clubs_info = clubs.val()

        infos = []
        for club in all_clubs_info:
            infos.append(all_clubs_info[club])

        club_info = []


        for u in infos:
            if u["code"] == code:
                get_pass = u["pass"]
                club_name = u["name"]
                break
            else:
                get_pass = "neetu"
                club_name = "neetur club"

        print(get_pass+" "+club_name)
        print(passc)

        if get_pass==passc:
            session['club_signed_in'] = code
            session['club_name'] = club_name
            return redirect(url_for("profile"))

        else:
            return render_template("club_sign_in.html", err="Incorrect Password")

    return render_template("club_sign_in.html")




@app.route("/dashboard", methods=['GET','POST'])
def dashboard():

    requests = db.child("StudentInfo").get().val()
    try:
        club_name = session['club_name']
    except:
        return redirect(url_for("/"))

    notification= []
    for i in requests:
        notification.append(requests[i])

    print(notification)
    nlist = []
    print(club_name)
    for i in notification:
        if i['club']==club_name:
            nlist.append(i)

    print("YYYYYYYYYAAAAAAAAAAHHHHHHHHHHOOOOOOOOOOOOOOO")
    print(nlist)


    return render_template("dashboard.html",notifications = nlist)





if __name__ == "__main__":
    app.run(debug=True)