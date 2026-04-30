Web app for displaying video game store sql database

Usage:
0. Install python dependencies 'pip install -r requirements.txt'
1. Set up sql database and edit .env to relect database parameters
2. run from terminal (on windows use backslash instead of /):
        mysql -u root -p < app/schema.sql
        mysql -u root -p cerulean_capybara < app/procedures.sql
        mysql -u root -p cerulean_capybara < app/seed.sql
3. 'flask run' to run web server

To reset:
mysql -u root -p -e "DROP DATABASE IF EXISTS cerulean_capybara; CREATE DATABASE cerulean_capybara;"
mysql -u root -p cerulean_capybara < app/schema.sql
mysql -u root -p cerulean_capybara < app/procedures.sql
mysql -u root -p cerulean_capybara < app/seed.sql

