Web app for displaying video game store sql database

Usage:
1. Set up sql database and edit .env to relect database parameters
2. run from terminal:
        mysql -u root -p < app/schema.sql
        mysql -u root -p cerulean_capybara < app/procedures.sql
        mysql -u root -p cerulean_capybara < populate_tables.sql
        if you run into foreign key constraint errors when populating, do all 3 of these:
                mysql -u root -p cerulean_capybara -e "SET FOREIGN_KEY_CHECKS=0;"
                mysql -u root -p cerulean_capybara < populate_tables.sql
                mysql -u root -p cerulean_capybara -e "SET FOREIGN_KEY_CHECKS=1;"
3. 'flask run' to run web server
