### 🗄️ Database Setup: 

Create Database  from Postgres console. 

Refer [this](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04) article for more information on how to create database.

### 💾 Redis Setup:

Refer to [this](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-20-04) article for more information on how to install Redis. Just follow through to step 3.

### 👨‍💻 Project Setup: 

- Enter the shell by typing `$ pipenv shell`
- Install dependencies by typing `$ pipenv install`
- Complete the steps mentioned in **Environment variables** section
- Run migrations `$ python manage.py migrate`
- Run local server `$ python manage.py runserver`
- Create superuser `$ python manage.py createsuperuser`
- Run Tests `$ pytest`

### 🔐 Environment variables: 

- Create file `.env` inside `cinevault` directory
- Copy contents from `.env.example` file and paste it in the `.env` file you just created.
- In `DATABASE_URL`,  replace `your_database_user` and `your_database_password` and `your_database_name` with your respective Database User and Password.
