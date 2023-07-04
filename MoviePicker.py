import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import *
from tkinter import messagebox

available_genres = [
    'Action', 'Adventure', 'Animation', 'Biography',
    'Comedy', 'Crime', 'Documentary', 'Drama',
    'Family', 'Fantasy', 'Film-Noir', 'Game-Show',
    'History', 'Horror', 'Music', 'Musical',
    'Mystery', 'News', 'Reality-TV', 'Romance',
    'Sci-Fi', 'Sport', 'Talk-Show', 'Thriller',
    'War', 'Western'
]

# Web scraping function to collect movie data
def scrape_movies(genre):
    if genre not in available_genres:
        raise ValueError("Invalid genre. Please choose from the available genres.")

    url = 'https://www.imdb.com/search/title?genres=' + genre
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    movies = soup.find_all('div', class_='lister-item-content')

    movie_data = []
    for movie in movies:
        title = movie.find('h3')
        if title is not None and title.find('a') is not None:
            title = title.find('a').text
        else:
            title = 'N/A'

        year = movie.find('span', class_='lister-item-year')
        if year is not None:
            year = year.text.strip('()')
        else:
            year = 'N/A'

        rating = movie.find('div', class_='ratings-imdb-rating')
        if rating is not None:
            rating = rating.text.strip()
        else:
            rating = 'N/A'

        genre = movie.find('span', class_='genre')
        if genre is not None:
            genre = genre.text.strip()
        else:
            genre = 'N/A'

        movie_data.append({'Title': title, 'Year': year, 'Rating': rating, 'Genre': genre})

    return movie_data

# Read the scraped data and filter based on user's selected genre
def get_movie_suggestions(genre):
    if genre not in available_genres:
        raise ValueError("Invalid genre. Please choose from the available genres.")

    df = pd.read_csv('movies.csv')  
    suggestions = df[df['Genre'].str.contains(genre)]  # Filter the dataset based on the user's selected genre
    return suggestions

# Genre selection
def genre_selected():
    selected_genre = genre_dropdown.get()
    try:
        movie_data = scrape_movies(selected_genre)
        df = pd.DataFrame(movie_data)
        df.to_csv('movies.csv', index=False)  # Saving the scraped movie data to a CSV file

        suggestions = get_movie_suggestions(selected_genre)
        if not suggestions.empty:
            suggestions = suggestions.sort_values(by='Rating', ascending=False)  # Sort by ratings in descending order
            suggestions_str = "Movie Suggestions:\n\n"
            for _, movie in suggestions.iterrows():
                suggestions_str += f"Title: {movie['Title']}\n"
                suggestions_str += f"Year: {movie['Year']}\n"
                suggestions_str += f"Rating: {movie['Rating']}\n"
                suggestions_str += "-" * 20 + "\n"

            # Show a message box with the movie suggestions
            messagebox.showinfo("Movie Suggestions", suggestions_str)
        else:
            messagebox.showinfo("Movie Suggestions", "No movies found for the selected genre.")
    except Exception as e:
        messagebox.showerror("Error", "An error occurred: " + str(e))


# GUI window
window = Tk()
window.title("Movie Suggestion App")

# Genre selection dropdown
genre_label = Label(window, text="Select a genre:")
genre_label.pack()

genre_dropdown = StringVar(window)
genre_dropdown.set(available_genres[0])  # Set the default genre
dropdown_menu = OptionMenu(window, genre_dropdown, *available_genres)
dropdown_menu.pack()

select_button = Button(window, text="Select", command=genre_selected)
select_button.pack()
window.mainloop()