Web app for displaying video game store sql database

Usage:
1. Set up sql database and edit .env to relect database parameters.
2. run:
    mysql -u root -p cerulean_capybara < app/schema.sql
    mysql -u root -p cerulean_capybara < app/procedures.sql
3. 'flask run' to run web server
