import mysql.connector
from mysql.connector import Error

DB_Host = "localhost"
DB_User = "root"
DB_PASS = "2004"
DB_NAME = "movie_recommendation"

def create_tables():
    try:
        connection = mysql.connector.connect(host=DB_Host, user=DB_User, password=DB_PASS, database=DB_NAME)
        cursor = connection.cursor()

        # Create 'movies' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                genre VARCHAR(255) NOT NULL
            )
        """)

        # Create 'ratings' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                movie_id INT NOT NULL,
                rating INT NOT NULL,
                FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
            )
        """)

        print("Tables created successfully.")

    except Error as e:
        print(f"Error creating tables: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

class Movie():
    def __init__(self, movie_id, name, genre,):
        self.name = name
        self.genre = genre
        self.movie_id = movie_id
    
    def __repr__(self):
        return f"Movie('{self.name}', '{self.genre}')"


    def set_movie_id(self, movie_id):
        self.movie_id = movie_id

    def set_name(self, name):
        self.name = name
    
    def set_genre(self, genre):
        self.genre = genre
    
    def get_name(self):
        return self.name
    
    def get_genre(self):
        return self.genre
    
    def get_movie_id(self):
        return self.movie_id
    

class MovieCollection():
    def addMovie(self, name, genre):
        try:
            connection = mysql.connector.connect(host = DB_Host,  user = DB_User, password = DB_PASS, database = DB_NAME)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO movies (name, genre) VALUES (%s, %s)", (name, genre))
            connection.commit()
        except Error as e:
            print(f"Error adding movie: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_movies_by_name(self, name):
        result = []
        try:
            connection = mysql.connector.connect(host = DB_Host,  user = DB_User, password = DB_PASS, database = DB_NAME)
            cursor = connection.cursor()
            cursor.execute('Select id, name, genre from movies WHERE name = %s', (name,))
            rows  = cursor.fetchall()
                
            for row in rows:
                result.append(Movie(row[0], row[1], row[2]))

        except Error as e:
            print(f"Error fetching by name: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        
        return result
    
    def get_movie_by_genre(self, genre):
        result = []
        try:
            connection = mysql.connector.connect(host = DB_Host,  user = DB_User, password = DB_PASS, database = DB_NAME)
            cursor = connection.cursor()
            cursor.execute('Select id, name, genre from movies WHERE genre = %s', (genre,))
            rows = cursor.fetchall()
                
            for row in rows:
                result.append(Movie(row[0], row[1], row[2]))

        except Error as e:
            print(f"Error fetching by genre: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        
        return result
     
    def get_all_movies(self):
        result = []
        try:
            connection = mysql.connector.connect(host = DB_Host,  user = DB_User, password = DB_PASS, database = DB_NAME)
            cursor = connection.cursor()
            cursor.execute('Select id, name, genre from movies')
            rows = cursor.fetchall()
                
            for row in rows:
                result.append(Movie(row[0], row[1], row[2]))

        except Error as e:
            print(f"Error fetching all movies: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        
        return result
    
    def get_movies_by_id(self, movie_id):
        result = []
        try:
            connection = mysql.connector.connect(host = DB_Host,  user = DB_User, password = DB_PASS, database = DB_NAME)
            cursor = connection.cursor()
            cursor.execute('Select name, genre from movies where id = %s', (movie_id,))
            rows = cursor.fetchall()
                
            for row in rows:
                result.append(Movie(row[0], row[1]))

        except Error as e:
            print(f"Error fetching all movies by id: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        
        return result
    
    def is_Genre_Available(self, genre):
        result = False
        try:
            connection = mysql.connector.connect(host = DB_Host,  user = DB_User, password = DB_PASS, database = DB_NAME)
            cursor = connection.cursor()
            cursor.execute('Select count(*) from movies WHERE genre = %s', (genre,))
            count = cursor.fetchone()[0]
            result = count>0
                
        except Error as e:
            print(f"Error checking Genre Availabilty: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        
        return result


class Ratings(MovieCollection):
    def __init__(self):
        super().__init__()
        self.rating = 0
        
    def rate_movie(self, movie_id):
        try:
            rating = int(input('How much would you rate the movie out of 10: '))
            while rating > 10 or rating < 0:
                rating = int(input('Invalid Rating, please try again'))
            
            self.add_rating(movie_id, rating)
            print('Rating Updated')

        except ValueError:
            print('Invalid input please try enter an integer.') 

    def add_rating(self, movie_id, rating):
        if not self.collection.get_movie_by_id(movie_id):  # Check if the movie exists
            raise ValueError("Movie not found. Please enter a valid movie ID.")
        try:
            connection = mysql.connector.connect(host = DB_Host,  user = DB_User, password = DB_PASS, database = DB_NAME)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO ratings (movie_id, rating) VALUES (%s, %s)", (movie_id, rating))
            connection.commit()
        except Error as e:
            print(f"Error adding ratings: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def get_all_ratings(self, movie_id):
        result = []
        try:
            connection = mysql.connector.connect(host = DB_Host,  user = DB_User, password = DB_PASS, database = DB_NAME)
            cursor = connection.cursor()
            cursor.execute('Select id, name, rating from ratings where movie_id = %s', (movie_id,))
            rows = cursor.fetchall()
                
            for row in rows:
                if len(row) >= 3:
                  result.append(Movie(row[0], row[1], row[2]))
                else:
                  print(f"Warning: Row has fewer than 3 elements: {row}")
        
        except Error as e:
            print(f"Error fetching ratings: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        
        return result

class Main():
    def __init__(self):
        self.collection = MovieCollection()
        self.ratings = Ratings()
        
    def intail_create_Setup(self):
        movies = [
            ("Inception", "Sci-Fi"),
            ("The Dark Knight", "Action"),
            ("Pulp Fiction", "Crime"),
            ("Forrest Gump", "Drama"),
            ("The Shawshank Redemption", "Drama"),
            ("Fight Club", "Drama"),
            ("The Godfather", "Crime"),
            ("Schindler's List", "Biography"),
            ("Goodfellas", "Crime"),
            ("The Matrix", "Sci-Fi"),
            ("Saving Private Ryan", "War"),
            ("Gladiator", "Action"),
            ("The Silence of the Lambs", "Thriller"),
            ("Braveheart", "Biography"),
            ("The Departed", "Crime"),
            ("Titanic", "Romance"),
            ("The Lord of the Rings", "Adventure"),
            ("The Lion King", "Animation"),
            ("Jurassic Park", "Adventure"),
            ("The Shining", "Horror"),
            ("Toy Story", "Animation"),
            ("The Terminator", "Sci-Fi"),
            ("E.T. the Extra-Terrestrial", "Family"),
            ("The Green Mile", "Crime"),
            ("The Sixth Sense", "Mystery"),
            ("Avatar", "Adventure"),
            ("The Avengers", "Action"),
            ("Inglourious Basterds", "War"),
            ("The Social Network", "Biography"),
            ("Interstellar", "Sci-Fi"),
            ("Charli and the Choclate Factory", "Action"),
        ]

        for name, genre in movies:
            self.collection.addMovie(name, genre)

        movie_ids = self.get_movie_ids()
        
        dummy_ratings = [
             (movie_ids[0], 8),
             (movie_ids[1], 8),
             (movie_ids[2], 9),
             (movie_ids[3], 7),
             (movie_ids[4], 9),
             (movie_ids[5], 10),
             (movie_ids[6], 8),
             (movie_ids[7], 9),
             (movie_ids[8], 7),
             (movie_ids[9], 8),
             (movie_ids[10], 9),
             (movie_ids[11], 8),
             (movie_ids[12], 7),
             (movie_ids[13], 8),
             (movie_ids[14], 9),
             (movie_ids[15], 7),
             (movie_ids[16], 8),
             (movie_ids[17], 9),
             (movie_ids[18], 8),
             (movie_ids[19], 7),
             (movie_ids[20], 8),
             (movie_ids[21], 9),
             (movie_ids[22], 7),
             (movie_ids[23], 8),
             (movie_ids[24], 9),
             (movie_ids[25], 8),
             (movie_ids[26], 7),
             (movie_ids[27], 8),
             (movie_ids[28], 9),
             (movie_ids[29], 7),
             (movie_ids[30], 6),
        ]

        for movie_id, rating in dummy_ratings:
            self.ratings.add_rating(movie_id, rating)
    
    def get_movie_ids(self):
        movies = self.collection.get_all_movies()
        movie_ids = []
        for i, movie in enumerate(movies):
            movie_ids[i] = movie.get_name()
        
        return movie_ids
    
    def get_movies_id_by_name(self, name):
        movie_id = None

        try:
            connection = mysql.connector.connect(host = DB_Host, user = DB_User, password = DB_PASS, database = DB_NAME)
            cursor = connection.cursor()
            cursor.execute('Select id from movies where name = %s', (name,))
            row = cursor.fetchone()

            if row:
                movie_id = row[0]
        
        except Error as e:
            print(f'Error fetching movie ID by name: {e}')

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        
        return movie_id
    
    
    def displaymovie(self):
        all_movies = self.collection.get_all_movies()
        for movie in all_movies:
            print(f"Name: {movie.get_name()}, Genre: {movie.get_genre()}")

        
    def display_ratings(self, movie_id):
        ratings = self.ratings.get_all_ratings(movie_id)
        if ratings:
            average_rating = sum(ratings)/len(ratings)
            print(f"Average Rating: {average_rating}")
        else:
            print('No ratings available.')

    def displaymenu(self):
        print("************************************************************************")
        print("-----------------------MOVIE RECOMMENDATION SYSTEM-----------------------")
        print("************************************************************************")
        print("1 Display All Movies.")
        print("2 Receive Recommendations")
        print("3 Rate a Movie")
        print("4 Search for movies by genre")
        print("5 Search for movies by name")
        print("6 Exit")
    

    
    def recommendmovies(self):
        
        import random 
        movies = self.collection.get_all_movies()
    
        if not movies:
           print("No movies available for recommendations.")
           return
      
    # Check if movies is a list
           print(type(movies))

    # Check if movies list is not empty
           print(len(movies))

    # Print each movie in the movies list
        for movie in movies:
            print(movie)

    # Select a random movie (for demonstration purposes)
        selected_movie = random.choice(movies)

        print(type(selected_movie))

        print(f"Recommended movie: {selected_movie.get_name()}")

    def display_by_genre(self, genre: str) -> None:
        """
    Displays a list of movies that match the specified genre.

    Args:
        genre (str): The genre to search for.

    Returns:
        None
    """
        if self.collection.is_Genre_Available(genre):
            movies = self.collection.get_movie_by_genre(genre)

            print(f"{'ID':5} {'Name':35} {'Genre':15} Ratings")
            print("-"*60)

            for movie in movies:
                print(dir(movie))
                print(f"{movie.movie_id:5} {movie.name:35} {movie.genre:15}")
                ratings = self.ratings.get_all_ratings(movie.movie_id)

                if ratings:
                    print(",".join(map(str, ratings)))
                
                else:
                    print('No ratings yet')

        else:
            print(f"Error: Genre '{genre}' not found in database.")

    def display_by_name(self):
        name = input("Enter movie name: ")
        movies = self. collection.get_movies_by_name(name) 

        if not movies:
            print('No movie found')
            return 

        print(f"{'ID':5} {'Name':35} {'Genre':15} Ratings")
        print("-" * 60) 

        for movie in movies:
            movie_id = movie.movie_id
            print(f"{movie.movie_id:5} {movie.name:35} {movie.genre:15}")

            ratings = self.ratings.get_all_ratings(movie_id)
            if ratings:
                print(", ".join(map(str, ratings)))
            else:
                print("No ratings yet")  

    def run(self):
        while True:
            self.displaymenu()
            option = input("Enter your choice: ")

            if option == '1':
                print("***************************************************************************")
                print("-------------------------------WELCOME USER--------------------------------")
                print("***************************************************************************")
                print("-------------------------------LIST OF MOVIES------------------------------")
                print("***************************************************************************")
                self.displaymovie()  

            elif option == '2':
                self.recommendmovies()

            elif option == '3':
                movie_id = int(input('Enter movie ID to rate: '))
                if self.collection.get_movie_by_id(movie_id):
                   rating = float(input('Enter rating out of 10: '))
                   self.ratings.add_rating(movie_id, rating)
                   self.display_ratings(movie_id)
                else:
                    print('Movie not found please enter a valid movie id.')

            elif option == '4':
                genre = input('Enter genre to display movies: ')
                self.display_by_genre(genre)
            
            elif option == '5':
                self.display_by_name()

            elif option == '6':
                print('Thankyou for using this program. Exiting.......')
                break
            
            else:
                print('Inavlid choice, please try again.')


if __name__ == "__main__":
    create_tables() 

    try:
        main = Main()
        main.run()

    except Error as e:
        print(f'SQL Error: {e}')
    
                      


                




            



