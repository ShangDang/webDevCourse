#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, cgi,re
form = """
<form method = "post">
    <b>Input your string:</br>
    <br>
    <textarea name = "text">%s</textarea>
    <input type = "submit"> </input>
    <h2>%s</h2>
</form>
"""
formSignup ="""
<h2>Signup</h2>
<br>
<form method = "post">
    <label>
        Username
        <input type="text" name = "username" value = "%(username)s"> 
        %(ue)s
    </label>
    <br>
    <label>
        Password
        <input type="text" name = "password" value = "%(password)s">
        %(pe)s
    </label>
    <br>
    <label>
        Verify Password
        <input type="text" name = "verify" value = "%(verify)s">
        %(ve)s
    </label>
    <br>
    <label>
        Email(optional)
        <input type="text" name = "email" value = "%(email)s">
        %(ee)s
    </label>
    <br>
    <input type = "submit">
</form>
"""

welcome_form = """
    <h2>Welcome, %s!</h2>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$" )
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASS_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)

def output(out_form,username,ue,password,pe,verify,ve,email,ee):
        return (out_form %{"username":username, "ue":ue,"password":password, "pe":pe, "verify":verify, "ve":ve,"email":email,"ee":ee})


class Rot13Handler(webapp2.RequestHandler):
    def rot(self, input):
        return input.encode('rot13')
             
    def get(self):
        self.response.write(form % ("",""))
    def post(self):
        input = self.request.get("text")
        input = self.rot(input)
        input = cgi.escape(input,  True)
        self.response.write(form % (input, "muamuamua~~~~"))

class SignupHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write(output(formSignup,"","","","","","","",""))

    def post(self):
        ue = ""
        pe = ""
        ve = ""
        ee = ""
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        user_va = valid_username(username)
        pass_va = valid_password(password)
        veri_va = verify == password
        
        if not email:
            email_va = True
        else:
            email_va = valid_email(email)

        if user_va and pass_va and veri_va and email_va:
            self.redirect("/welcome?username=" + username)
        else:
            if not user_va:
                ue = "That's not a valid username."

            if not pass_va:
                pe = "That wasn't a valid password."
            else:
                if not veri_va:
                    ve = "Your passwords didn't match."

            if not email_va:
                ee = "That's not a valid email."
            username = cgi.escape(username,True)
            email = cgi.escape(email, True)

            self.response.write(output(formSignup,username,ue,"",pe,"",ve,email,ee)) 

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        if valid_username(username):
            self.response.write(welcome_form % username)
        else:
            self.redirect('/signon')

app = webapp2.WSGIApplication([
    ('/rot13', Rot13Handler),
    ('/signup', SignupHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
