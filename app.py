import os
from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-for-session')

def get_github_user(username):
    """Fetch GitHub user data"""
    response = requests.get(f'https://api.github.com/users/{username}', 
                            headers={'Accept': 'application/vnd.github.v3+json'})
    if response.status_code == 200:
        return response.json()
    return None

def get_user_repos(username):
    """Fetch repositories for a GitHub user"""
    response = requests.get(f'https://api.github.com/users/{username}/repos?sort=updated&per_page=100', 
                           headers={'Accept': 'application/vnd.github.v3+json'})
    if response.status_code == 200:
        return response.json()
    return []

def get_repo_languages(username, repo_name):
    """Fetch languages used in a repository"""
    response = requests.get(f'https://api.github.com/repos/{username}/{repo_name}/languages', 
                           headers={'Accept': 'application/vnd.github.v3+json'})
    if response.status_code == 200:
        return response.json()
    return {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        github_username = request.form.get('github_username')
        if not github_username:
            flash('Please enter a GitHub username')
            return redirect(url_for('index'))
            
        return redirect(url_for('user_profile', username=github_username))
    
    # If GET request or no username provided
    return redirect(url_for('index'))

@app.route('/profile/<username>')
def user_profile(username):
    user_data = get_github_user(username)
    
    if not user_data:
        flash(f'User {username} not found or GitHub API rate limit exceeded')
        return redirect(url_for('index'))
        
    repos_data = get_user_repos(username)
    
    # Enhance repo data with language information
    for repo in repos_data:
        repo['languages'] = get_repo_languages(username, repo['name'])
    
    return render_template('profile.html', user=user_data, repos=repos_data)

@app.errorhandler(HTTPException)
def handle_exception(e):
    return render_template('error.html', error=e), e.code

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error="Server error occurred"), 500

if __name__ == '__main__':
    app.run(debug=True)