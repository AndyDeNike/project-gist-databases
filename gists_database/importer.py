import requests

#How does the schema.sql tie into this py file?  Is it connected via the test_importer.py?
#This disconnect can be confusing for someone just learning the process

#At this point we havent really been introduced to dynamic query sqlite assignment 

INSERT_GIST_QUERY = """INSERT INTO gists (
    "github_id", "html_url", "git_pull_url",
    "git_push_url", "commits_url", "forks_url",
    "public", "created_at", "updated_at",
    "comments", "comments_url"
) VALUES (
    :github_id, :html_url, :git_pull_url,
    :git_push_url, :commits_url, :forks_url,
    :public, :created_at, :updated_at, 
    :comments, :comments_url
);"""

#unclear why would access them from this url
#is this from the actual website or is this a local file in the project? 

URL_TEMPLATE = 'https://api.github.com/users/{username}/gists'

def import_gists_to_database(db, username, commit=True):
    
    #resp captures all the database from the url based on the inputed username within the test 
    resp = requests.get(URL_TEMPLATE.format(username=username))
    resp.raise_for_status()
    
    gists_data = resp.json()
    for gist in gists_data:
        params = {
            "github_id": gist['id'],
            "html_url": gist['html_url'],
            "git_pull_url": gist['git_pull_url'],
            "git_push_url": gist['git_push_url'],
            "commits_url": gist['commits_url'],
            "forks_url": gist['forks_url'],
            "public": gist['public'],
            "created_at": gist['created_at'],
            "updated_at": gist['updated_at'],
            "comments": gist['comments'],
            "comments_url": gist['comments_url']
        }
        db.execute(INSERT_GIST_QUERY, params)
        if commit: 
            db.commit()
    
    