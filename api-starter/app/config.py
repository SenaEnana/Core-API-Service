# ```text
# Remember the following everytime especially whenever you delete your codespace

# 1. Remember that env file will be deleted everytime you delete the codespace so create:
# .env file in the root directory
# with the ff code ==> ADMIN_SECRET_KEY=your_secrete_admin_code_including_numbers
# 2. Remember your database will also be deleted with codespace so keep the copy somewhere safe as a backup
# 3. Remember to install dependencies before starting any work like the following:
#  * Frontend
#    * npm install
#    * npm install lucide-react
#  * Backend
#    * pip install fastapi[standard]
#    * pip install dotenv
#    * pip install psycopg2-binary--installed in the backend folder for postgresql db
# 4. Remember to replace the endpoint in the frontend/services/api with the correct backend api endpoint when deployed
# 5. Remember to use the following command to commit to the previous date
#   * git add .
#   * $env:GIT_AUTHOR_DATE="2026-08-15T04:00:00"
#   * $env:GIT_COMMITTER_DATE="2026-08-15T04:00:00"
#   * git add .
#   * git commit -m "message here"
#   * git commit -m "message here" or use the ff in one line
#   * GIT_AUTHOR_DATE="2026-09-09T10:00:00" GIT_COMMITTER_DATE="2026-09-09T10:00:00" git commit --date="2026-09-09T10:00:00" -m "commit message"
# 6. Remember to view your work use the following command
#   * python -m uvicorn app.main:app --reload "or" in my case use the following
#   * python -m uvicorn backend.app.main:app --reload   

# -the .env.development and .env.production are in the frontend
# ```
