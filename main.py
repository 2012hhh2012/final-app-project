from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
from PyQt6 import uic
import sys
import json
import os
import webbrowser
import platform
import subprocess

class SigninWindow(QMainWindow):
    def __init__(self, user_manager):
        super().__init__()
        uic.loadUi("signin.ui", self)
        self.setWindowTitle("VibeDock - Signin")
        self.user_manager = user_manager
        self.btnSignUp.clicked.connect(lambda: opensignup(self))
        self.btnSignIn.clicked.connect(self.Signin)
        self.btnGoogle.clicked.connect(self.showUnavailable)
        self.btnGithub.clicked.connect(self.showUnavailable)

    def Signin(self):
        if self.linePassword.text() and self.lineEmail.text():
            status, message = self.user_manager.verify_user(self.lineEmail.text(), self.linePassword.text())
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
    def __init__(self, user_manager):
        super().__init__()
        uic.loadUi("signup.ui", self)
        self.setWindowTitle("VibeDock - Signup")
        self.user_manager = user_manager
        self.btnSignIn.clicked.connect(lambda: opensignin(self))
        self.btnSignUp.clicked.connect(self.Signup)
        self.btnGoogle.clicked.connect(self.showUnavailable)
        self.btnGithub.clicked.connect(self.showUnavailable)

    def Signup(self):
        if self.linePassword.text() and self.lineUsername.text() and self.lineEmail.text():
            status, message = self.user_manager.add_user(self.lineUsername.text(), self.linePassword.text(), self.lineEmail.text())
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
    def __init__(self, user_manager):
        super().__init__()
        uic.loadUi("dashboard.ui", self)
        self.setWindowTitle("VibeDock - Dashboard")
        self.user_manager = user_manager
        self.loadQuickAccess()
        self.lblUsername.setText(f"Username: {self.user_manager.get_current_username()}")
        self.btnProfiles.clicked.connect(lambda: openprofiles(self))
        self.btnSettings.clicked.connect(lambda: opensettings(self))
        self.btnSignOut.clicked.connect(lambda: signout(self))
        self.btnLaunch.clicked.connect(self.launchProfile)
        self.btnEdit.clicked.connect(self.editProfile)

    def loadQuickAccess(self):
        if self.user_manager.get_current_user():
            self.listQuickAccess.clear()
            if self.user_manager.get_current_user().get("quickaccess"):
                for profile in user_manager.get_current_user().get("quickaccess"):
                    self.listQuickAccess.addItem(profile)

    def launchProfile(self):
        if self.listQuickAccess.currentItem():
            self.user_manager.push_quick_access_profile_of_current_user(self.listQuickAccess.currentItem().text())
            launch_resources(self.user_manager.get_current_user_profile_resources(self.listQuickAccess.currentItem().text()))
        else:
            QMessageBox.warning(self, "Warning", "Please select a profile to launch.")

    def editProfile(self):
        if self.listQuickAccess.currentItem():
            self.user_manager.push_quick_access_profile_of_current_user(self.listQuickAccess.currentItem().text())
            openeditprofile(self, self.listQuickAccess.currentItem().text())
        else:
            QMessageBox.warning(self, "Warning", "Please select a profile to edit.")

class ProfilesWindow(QMainWindow):
    def __init__(self, user_manager):
        super().__init__()
        uic.loadUi("profiles.ui", self)
        self.setWindowTitle("VibeDock - Profiles")
        self.user_manager = user_manager
        self.loadProfiles()
        self.lblUsername.setText(f"Username: {self.user_manager.get_current_username()}")
        self.btnDashboard.clicked.connect(lambda: opendashboard(self))
        self.btnSettings.clicked.connect(lambda: opensettings(self))
        self.btnSignOut.clicked.connect(lambda: signout(self))
        self.btnAddProfile.clicked.connect(self.addProfile)
        self.btnLaunch.clicked.connect(self.launchProfile)
        self.btnEdit.clicked.connect(self.editProfile)
        self.btnDelete.clicked.connect(self.deleteProfile)
    
    def loadProfiles(self):
        if self.user_manager.get_current_user():
            self.listProfiles.clear()
            for profile in user_manager.get_current_user_profiles():
                self.listProfiles.addItem(profile)

    def addProfile(self):
        profile_name, ok = QInputDialog.getText(self, "Add Profile", "Enter profile name:")
        if ok and profile_name:
            status, message = self.user_manager.add_profile_to_current_user(profile_name)
            if status:
                openeditprofile(self, profile_name)
            else:
                QMessageBox.warning(self, "Warning", message)

    def launchProfile(self):
        if self.listProfiles.currentItem():
            self.user_manager.push_quick_access_profile_of_current_user(self.listProfiles.currentItem().text())
            launch_resources(self.user_manager.get_current_user_profile_resources(self.listProfiles.currentItem().text()))
        else:
            QMessageBox.warning(self, "Warning", "Please select a profile to launch.")

    def editProfile(self):
        if self.listProfiles.currentItem():
            openeditprofile(self, self.listProfiles.currentItem().text())
        else:
            QMessageBox.warning(self, "Warning", "Please select a profile to edit.")

    def deleteProfile(self):
        if self.listProfiles.currentItem():
            status, message = self.user_manager.delete_current_user_profile(self.listProfiles.currentItem().text())
            if status:
                self.user_manager.get_current_user()["quickaccess"].remove(self.listProfiles.currentItem().text())
                self.loadProfiles()
            else:
                QMessageBox.warning(self, "Warning", message)
        else:
            QMessageBox.warning(self, "Warning", "Please select a profile to delete.")

class EditProfileWindow(QMainWindow):
    def __init__(self, user_manager, profile_name):
        super().__init__()
        uic.loadUi("editprofile.ui", self)
        self.setWindowTitle(f"VibeDock - Editing profile: {profile_name}")
        self.resources = []
        self.settings = {}
        self.user_manager = user_manager
        self.profile_name = profile_name
        self.loadProfile()
        self.lblUsername.setText(f"Username: {self.user_manager.get_current_username()}")
        self.btnDashboard.clicked.connect(lambda: opendashboard(self))
        self.btnSettings.clicked.connect(lambda: opensettings(self))
        self.btnProfiles.clicked.connect(lambda: openprofiles(self))
        self.btnSignOut.clicked.connect(lambda: signout(self))
        self.btnDeleteProfile.clicked.connect(self.deleteProfile)
        self.btnSave.clicked.connect(self.saveProfile)
        self.btnAddResource.clicked.connect(self.addResource)
        self.btnDeleteResource.clicked.connect(self.deleteResource)

    def addResource(self):
        resource, ok = QInputDialog.getText(self, "Add Resource", "Enter resource (file path, url):")
        if ok and resource:
            self.resources.append(resource)
            self.listResources.addItem(resource)

    def deleteResource(self):
        if self.listResources.currentItem():
            self.resources.remove(self.listResources.currentItem().text())
            self.listResources.takeItem(self.listResources.currentRow())
        else:
            QMessageBox.warning(self, "Warning", "Please select a resource to delete.")

    def loadProfile(self):
        if self.user_manager.get_current_user():
            self.user_manager.push_quick_access_profile_of_current_user(self.profile_name)
            self.lblProfileName.setText(self.profile_name)
            self.lblHeadingProfileName.setText(self.profile_name)
            self.listResources.clear()
            self.settings = self.user_manager.get_current_user_profile(self.profile_name).get("settings", {})
            self.chkFocusTimer.setChecked(self.settings.get("focus_timer", False))
            self.lineDuration.setText(str(self.settings.get("duration", 0)))
            self.resources = self.user_manager.get_current_user_profile_resources(self.profile_name)
            for resource in self.resources:
                self.listResources.addItem(resource)

    def deleteProfile(self):
        status, message = self.user_manager.delete_current_user_profile(self.profile_name)
        if status:
            self.user_manager.get_current_user()["quickaccess"].remove(self.profile_name)
            openprofiles(self)
        else:
            QMessageBox.warning(self, "Warning", message)

    def saveProfile(self):
        self.settings = {"focus_timer": self.chkFocusTimer.isChecked(), "duration": int(self.lineDuration.text())}
        status, message = self.user_manager.update_current_user_profile(self.profile_name, self.resources, self.settings)
        if status:
            openprofiles(self)
        else:
            QMessageBox.warning(self, "Warning", message)

class SettingsWindow(QMainWindow):
    def __init__(self, user_manager):
        super().__init__()
        uic.loadUi("settings.ui", self)
        self.setWindowTitle("VibeDock - Settings")
        self.user_manager = user_manager
        self.loadAppSettings()
        self.lblUsername.setText(f"Username: {self.user_manager.get_current_username()}")
        self.btnDashboard.clicked.connect(lambda: opendashboard(self))
        self.btnProfiles.clicked.connect(lambda: openprofiles(self))
        self.btnSideSignOut.clicked.connect(lambda: signout(self))
        self.btnDeleteAccount.clicked.connect(self.deleteAccount)
        self.btnAppSave.clicked.connect(self.saveAppSettings)
        self.btnAccountSave.clicked.connect(self.saveAccountCredentials)

    def loadAppSettings(self):
        if self.user_manager.get_current_user():
            self.chkLaunchOnStartup.setChecked(self.user_manager.get_current_user()["settings"]["launchOnStartup"])
            self.chkMinimizeToTray.setChecked(self.user_manager.get_current_user()["settings"]["MinimizeToTray"])

    def deleteAccount(self):
        status, message = self.user_manager.delete_user(self.user_manager.get_current_user()["email"])
        if status:
            opensignup(self)
        else:
            QMessageBox.warning(self, "Warning", message)

    def saveAppSettings(self):
        self.user_manager.get_current_user()["settings"]["launchOnStartup"] = self.chkLaunchOnStartup.isChecked()
        self.user_manager.get_current_user()["settings"]["MinimizeToTray"] = self.chkMinimizeToTray.isChecked()
        self.user_manager.save_users()
        QMessageBox.information(self, "Success", "App settings saved successfully!")

    def saveAccountCredentials(self):
        if self.linePassword.text():
            self.user_manager.get_current_user()["password"] = self.linePassword.text()
            self.linePassword.clear()
        if self.lineEmail.text():
            self.user_manager.get_current_user()["email"] = self.lineEmail.text()
            self.user_manager.current_user["email"] = self.lineEmail.text()
            self.lineEmail.clear()
        self.user_manager.save_users()
        QMessageBox.information(self, "Success", "Account credentials saved successfully!")

class UserManager:
    def __init__(self, filename="users-data.json"):
        self.filename = filename
        self.users = []  # Array to store multiple users
        self.current_user = None
        self.load_users()

    def get_current_user(self):
        return self.current_user
    
    def get_current_username(self):
        if self.current_user:
            return self.current_user.get("username")
        return None
    
    def load_users(self):
        """Load users array from JSON file, create if doesn't exist"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    self.users = json.load(file)
                print(f"Loaded {len(self.users)} users from {self.filename}")
            except json.JSONDecodeError:
                print(f"Error reading {self.filename}, creating new file")
                self.users = []
                self.save_users()
            except Exception as e:
                print(f"Error loading users: {e}")
                self.users = []
                self.save_users()
        else:
            # File doesn't exist, create it with empty array
            print(f"{self.filename} not found, creating new file")
            self.users = []
            self.save_users()
    
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
            "profiles": {},
            "quickaccess": []
        }
        
        # Add to array
        self.users.append(new_user)
        self.save_users()
        self.current_user = new_user
        return True, "User created successfully!"

    def push_quick_access_profile_of_current_user(self, profile_name):
        if self.current_user.get("quickaccess"):
            if profile_name in self.current_user["quickaccess"]:
                self.current_user["quickaccess"].remove(profile_name)
        else:
            self.current_user["quickaccess"] = []
        self.current_user["quickaccess"].insert(0, profile_name)
        self.save_users()
    
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
        print(self.current_user)
        return True, f"Welcome {user['username']}!"
    
    def signout(self):
        self.current_user = None
    
    def get_current_user_profiles(self):
        """Get profiles for currently logged in user"""
        if self.current_user:
            return self.current_user.get("profiles", {})
        return None
    
    def add_profile_to_current_user(self, profile_name):
        """Add a new profile to the currently logged in user"""
        # Check if user is logged in
        user = self.current_user
        if not user:
            return False, "No user is currently logged in!"
        
        # Initialize profiles dict if it doesn't exist
        if "profiles" not in user:
            user["profiles"] = {}
        
        # Check if profile already exists
        if profile_name in user["profiles"]:
            return False, f"Profile '{profile_name}' already exists!"
        
        # Add the new profile with empty resources array
        user["profiles"][profile_name] = {
            "resources": [],
            "settings": {
                "focus_timer": False,
                "duration": 0
            }
        }
        
        # Update current_user reference
        self.current_user = user
        
        # Save to file
        self.save_users()
        
        return True, f"Profile '{profile_name}' created successfully!"

    def delete_current_user_profile(self, profile_name):
        """Delete a profile from the currently logged in user"""
        user = self.current_user
        if not user:
            return False, "No user is currently logged in!"
        
        if profile_name not in user.get("profiles", {}):
            return False, f"Profile '{profile_name}' not found!"
        
        del user["profiles"][profile_name]
        self.save_users()
        return True, f"Profile '{profile_name}' deleted successfully!"

    def get_current_user_profile_resources(self, profile_name):
        """Get all resources in a specific profile"""
        user = self.current_user
        if not user:
            return None
        
        profile = user.get("profiles", {}).get(profile_name, {})
        return profile.get("resources", [])
    
    def update_current_user_profile(self, profile_name, resource_list, settings):
        user = self.current_user
        if not user:
            return False, "No user is currently logged in!"
        
        if profile_name not in user.get("profiles", {}):
            return False, f"Profile '{profile_name}' not found!"
        
        user["profiles"][profile_name]["resources"] = resource_list
        user["profiles"][profile_name]["settings"] = settings
        self.save_users()
        return True, f"Profile '{profile_name}' updated successfully!"
    
    def get_current_user_profile(self, profile_name):
        user = self.current_user
        if not user:
            return None
        
        profiles = user.get("profiles", {})
        return profiles.get(profile_name, {})
    
    def delete_user(self, email):
        """Remove user from array. Returns (success, message)"""
        # Find the user
        for i, user in enumerate(self.users):
            if user["email"].lower() == email.lower():
                # If the deleted user is the current user, log them out
                if self.current_user and self.current_user["email"].lower() == email.lower():
                    self.current_user = None
                del self.users[i]
                self.save_users()
                return True, "Account deleted successfully!"
        return False, "User not found!"

# Switch ui functions
def opendashboard(current_window):
    global dashboardwindow
    dashboardwindow = DashboardWindow(current_window.user_manager)
    dashboardwindow.show()
    current_window.close()

def opensignin(current_window):
    global signinwindow
    signinwindow = SigninWindow(current_window.user_manager)
    signinwindow.show()
    current_window.close()

def opensignup(current_window):
    global signupwindow
    signupwindow = SignupWindow(current_window.user_manager)
    signupwindow.show()
    current_window.close()

def openprofiles(current_window):
    global profileswindow
    profileswindow = ProfilesWindow(current_window.user_manager)
    profileswindow.show()
    current_window.close()

def opensettings(current_window):
    global settingswindow
    settingswindow = SettingsWindow(current_window.user_manager)
    settingswindow.show()
    current_window.close()

def openeditprofile(current_window, profile_name):
    global editprofilewindow
    editprofilewindow = EditProfileWindow(current_window.user_manager, profile_name)
    editprofilewindow.show()
    current_window.close()

def signout(current_window):
    UserManager().signout()
    opensignin(current_window)

# Helper
def smart_open(target):
    # 1. URL
    if target.startswith(("http://", "https://")):
        webbrowser.open(target)
    
    # 2. File or Folder
    else:
        if platform.system() == "Windows":
            os.startfile(target)
        # elif platform.system() == "Darwin": # macOS
        #     subprocess.Popen(["open", target])
        # else: # Linux
        #     subprocess.Popen(["xdg-open", target])

def launch_resources(resources):
    for resource in resources:
        smart_open(resource)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    user_manager = UserManager("users-data.json")
    signupwindow = SignupWindow(user_manager)
    signinwindow = SigninWindow(user_manager)
    dashboardwindow = DashboardWindow(user_manager)
    profileswindow = ProfilesWindow(user_manager)
    editprofilewindow = EditProfileWindow(user_manager, None)
    settingswindow = SettingsWindow(user_manager)
    signinwindow.show()
    app.exec()