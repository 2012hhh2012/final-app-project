from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6 import uic
import sys
import json
import os

class SigninWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("signin.ui", self)
        self.btnSignUp.clicked.connect(lambda: opensignup(self))
        self.btnSignIn.clicked.connect(self.Signin)
        self.btnGoogle.clicked.connect(self.showUnavailable)
        self.btnGithub.clicked.connect(self.showUnavailable)

    def Signin(self):
        if self.linePassword.text() and self.lineEmail.text():
            status, message = UserManager().verify_user(self.lineEmail.text(), self.linePassword.text())
            if status:
                self.clearInputs()
                opendashboard(self)
            else:
                self.clearInputs()
                QMessageBox.warning(self, "Warning", message)
        else:
            self.clearInputs()
            QMessageBox.warning(self, "Warning", "Please enter your email and password.")

    def clearInputs(self):
        self.linePassword.clear()
        self.lineEmail.clear()

    def showUnavailable(self):
        QMessageBox.information(self, "Sorry", "This Signin method is unavailable.")

class SignupWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("signup.ui", self)
        self.btnSignIn.clicked.connect(lambda: opensignin(self))
        self.btnSignUp.clicked.connect(self.Signup)
        self.btnGoogle.clicked.connect(self.showUnavailable)
        self.btnGithub.clicked.connect(self.showUnavailable)

    def Signup(self):
        if self.linePassword.text() and self.lineUsername.text() and self.lineEmail.text():
            status, message = UserManager().add_user(self.lineUsername.text(), self.linePassword.text(), self.lineEmail.text())
            if status:
                self.clearInputs()
                opendashboard(self)
            else:
                self.clearInputs()
                QMessageBox.warning(self, "Warning", message)
        else:
            self.clearInputs()
            QMessageBox.warning(self, "Warning", "Please enter your username, password and email.")

    def clearInputs(self):
        self.linePassword.clear()
        self.lineEmail.clear()
        self.lineUsername.clear()

    def showUnavailable(self):
        QMessageBox.information(self, "Sorry", "This Signup method is unavailable.")

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("dashboard.ui", self)
        self.btnProfiles.clicked.connect(lambda: openprofiles(self))
        self.btnSettings.clicked.connect(lambda: opensettings(self))
        self.btnSignOut.clicked.connect(lambda: signout(self))

class ProfilesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("profiles.ui", self)
        self.btnDashboard.clicked.connect(lambda: opendashboard(self))
        self.btnSettings.clicked.connect(lambda: opensettings(self))
        self.btnSignOut.clicked.connect(lambda: signout(self))

class EditProfileWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("editprofile.ui", self)
        self.btnDashboard.clicked.connect(lambda: opendashboard(self))
        self.btnSettings.clicked.connect(lambda: opensettings(self))
        self.btnProfiles.clicked.connect(lambda: openprofiles(self))
        self.btnSignOut.clicked.connect(lambda: signout(self))

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("settings.ui", self)
        self.btnDashboard.clicked.connect(lambda: opendashboard(self))
        self.btnProfiles.clicked.connect(lambda: openprofiles(self))
        self.btnSideSignOut.clicked.connect(lambda: signout(self))

class UserManager:
    def __init__(self, filename="users-data.json"):
        self.filename = filename
        self.users = []  # Array to store multiple users
        self.current_user = None
        self.load_users()

    def get_current_user(self):
        return self.current_user
    
    def load_users(self):
        """Load users array from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    self.users = json.load(file)
            except:
                self.users = []
        else:
            self.users = []
    
    def save_users(self):
        """Save users array to JSON file"""
        with open(self.filename, "w") as file:
            json.dump(self.users, file, indent=4)
    
    def add_user(self, username, password, email):
        """Add a new user to the array"""
        # Check if username already exists
        if self.find_user_by_username(username):
            return False, "Username already exists!"
        
        # Check if email already exists
        if self.find_user_by_email(email):
            return False, "Email already exists!"
        
        # Create new user object
        new_user = {
            "username": username,
            "password": password,
            "email": email,
            "settings": {
                "launchOnStartup": False,
                "MinimizeToTray": False
            },
            "profiles": {}
        }
        
        # Add to array
        self.users.append(new_user)
        self.save_users()
        return True, "User created successfully!"
    
    def find_user_by_email(self, email):
        """Find user by email in the array"""
        for user in self.users:
            if user["email"].lower() == email.lower():
                return user
        return None
    
    def find_user_by_username(self, username):
        """Find user by username in the array"""
        for user in self.users:
            if user["username"] == username:
                return user
        return None
    
    def verify_user(self, email, password):
        """Verify user credentials using email and password"""
        # Find user by email
        user = self.find_user_by_email(email)
        
        if not user:
            return False, "Email not found! Please sign up first."
        
        # Check password
        if user["password"] != password:
            return False, "Incorrect password!"
        
        # Set current user
        self.current_user = user
        return True, f"Welcome {user['username']}!"
    
    def Signout(self):
        self.current_user = None
    
    def get_user_profiles(self, email):
        """Get all profiles for a user"""
        user = self.find_user_by_email(email)
        if user:
            return user.get("profiles", {})
        return None
    
    def get_current_user_profiles(self):
        """Get profiles for currently logged in user"""
        if self.current_user:
            return self.current_user.get("profiles", {})
        return None
    
    def get_profile_resources(self, email, profile_name):
        """Get all resources in a specific profile"""
        user = self.find_user_by_email(email)
        if not user:
            return None
        
        profiles = user.get("profiles", {})
        return profiles.get(profile_name, [])
    
    def add_resource_to_profile(self, email, profile_name, resource_name):
        """Add a resource to a profile's array"""
        user = self.find_user_by_email(email)
        if not user:
            return False, "User not found!"
        
        if profile_name not in user.get("profiles", {}):
            return False, f"Profile '{profile_name}' not found!"
        
        # Check if resource already exists
        if resource_name in user["profiles"][profile_name]:
            return False, f"Resource '{resource_name}' already exists in profile!"
        
        user["profiles"][profile_name].append(resource_name)
        self.save_users()
        return True, f"Resource '{resource_name}' added to '{profile_name}'!"
    
    def remove_resource_from_profile(self, email, profile_name, resource_name):
        """Remove a resource from a profile's array"""
        user = self.find_user_by_email(email)
        if not user:
            return False, "User not found!"
        
        if profile_name not in user.get("profiles", {}):
            return False, f"Profile '{profile_name}' not found!"
        
        if resource_name not in user["profiles"][profile_name]:
            return False, f"Resource '{resource_name}' not found in profile!"
        
        user["profiles"][profile_name].remove(resource_name)
        self.save_users()
        return True, f"Resource '{resource_name}' removed from '{profile_name}'!"
    
    def get_all_users(self):
        """Return the entire users array"""
        return self.users
    
    def update_user(self, username, updated_data):
        """Update user information"""
        for i, user in enumerate(self.users):
            if user["username"] == username:
                self.users[i].update(updated_data)
                self.save_users()
                return True
        return False
    
    def delete_user(self, username):
        """Remove user from array"""
        for i, user in enumerate(self.users):
            if user["username"] == username:
                del self.users[i]
                self.save_users()
                return True
        return False
    
    def get_user_count(self):
        """Get total number of users"""
        return len(self.users)

# Switch ui functions
def opendashboard(current_window):
    global dashboardwindow
    dashboardwindow.show()
    current_window.close()

def opensignin(current_window):
    global signinwindow
    signinwindow.show()
    current_window.close()

def opensignup(current_window):
    global signupwindow
    signupwindow.show()
    current_window.close()

def openprofiles(current_window):
    global profileswindow
    profileswindow.show()
    current_window.close()

def opensettings(current_window):
    global settingswindow
    settingswindow.show()
    current_window.close()

def openeditprofile(current_window):
    global editprofilewindow
    editprofilewindow.show()
    current_window.close()

def signout(current_window):
    UserManager().Signout()
    opensignin(current_window)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    signupwindow = SignupWindow()
    signinwindow = SigninWindow()
    dashboardwindow = DashboardWindow()
    profileswindow = ProfilesWindow()
    editprofilewindow = EditProfileWindow()
    settingswindow = SettingsWindow()
    signinwindow.show()
    app.exec()