import pandas as pd
import numpy as np

titles_by_age = {}

def getMoviesByAge(age, max_num):
    best_movies = []
    best_age = getBestAge(age)
    
    for rating in range(5,2,-1):
        try:
            movies = titles_by_age[best_age][rating]
            for movie in movies:
                if len(best_movies) >= max_num:
                    break
                best_movies.append(movie)
        except:
            pass
        if len(best_movies) >= max_num:
            break
    return ','.join(best_movies)

def getBestAge(age):
    min_age = min(titles_by_age.keys(), key=lambda a: abs(a - age))
    return min_age

def main():
    # Read input files
    df = pd.read_csv("RatingsInput.csv")
    df2 = pd.read_csv("NewUsers.csv")

    # Task 1 - Separate Movie IDs and Movie names.
    df['MovieID'], df['MovieName'] = df['MovieName'].str.split(',').str
    
    # Task 2 - String Capitalization - Capitalizing the first letter of every word in the movie names.
    df['MovieName'] = df['MovieName'].str.title()

    # Task 3 - Read in from your new CSV file from Task 2 and parse data into lists and dictionaries.
    grouped = df.groupby('UserAge')
    
    for g in grouped:
        ratings = g[1].groupby('Rating')['MovieName'].apply(list)
        titles_by_age[g[0]] = {}
        for k,v in ratings.sort_index(ascending=False).items():
            titles_by_age[g[0]][k] = v
    
    # Task 4 - Find the recommended movies for a given age from best to worst ratings.
    # Please refer the getMoviesByAge() function above
    df2["Movies"] = df2.apply(lambda x: getMoviesByAge(x['UserAge'], x['NoOfMoviesToRecommend']), axis=1)
    # Task 5 - Recommend movies to users in the second input file.
    df2.to_csv('output.csv', index=False)

if __name__=="__main__":
    main()
