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
import webapp2
import re



form="""<!DOCTYPE HTML>
<html>
    <head>
    <h1>User Sign up</h1>
    <style type = "text/css">
        .error {color:red}
    </style>
    </head>
    <body>
<form method = post>
    <table>
        <tr><td><label>Username</td>
            <td><input type ="text" name ="Username" value = %(username)s >
        </label></td><td class = "error">%(error_username)s</td></tr>

        <tr><td><label>Password</td>
            <td><input type ="password" name ="Password" value = "">
        </label></td><td class = "error">%(error_password)s</td></tr>

        <tr><td><label>Verify Password</td>
            <td><input type ="password" name ="Verify" value="">
        </label></td><td class = "error">%(error_verify)s</td></tr>

        <tr><td><label>Email (Optional)</td>
        <td><input type ="text" name ="Email" value = %(email)s>
        </label></td><td class = "error">%(error_email)s</td></tr>
        </br>
    </table>
    <input type="submit">
</form>
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)
PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)
EMAIL_RE = re.compile(r'^[\S]+@[\S]+.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):



    def get(self):
        self.write_form()

    def write_form( self, username = "", password="", verify = "", email="", error_username="",error_password="",error_verify="",error_email=""):
        self.response.out.write(form % {"username":username,"email":email, "error_username":error_username,"error_password" :error_password,"error_verify" :error_verify,"error_email":error_email})


    def post(self):
        have_Error = False
        username = self.request.get("Username")
        password =  self.request.get("Password")
        verify = self.request.get("Verify")
        email = self.request.get("Email")

        error_username=""
        error_password=""
        error_verify=""
        error_email=""

        if not valid_username(username):
            error_username = "Username is not valid"
            have_Error = True
        if not valid_password(password):
            error_password = "Password not valid"
            have_Error = True
        if verify != password:
            error_verify = "Passwords do not match!"
            have_Error = True
        if not valid_email(email):
            error_email ="Not a valid email address"
            have_Error = True
        if have_Error:

            self.write_form(username, password, verify, email, error_username , error_password, error_verify, error_email)
        else:
            self.redirect("/welcome?username="+username)


class Welcome(webapp2.RequestHandler):
    def get(self):
        username=self.request.get("username")
        if valid_username(username):
            self.response.out.write("Welcome, " + username)
        else:
            self.redirect("/")





app = webapp2.WSGIApplication([
    ('/', MainHandler),('/welcome',Welcome)
], debug=True)
