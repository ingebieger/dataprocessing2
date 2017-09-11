#!/usr/bin/env python
# Name: Inge Bieger
# Student number: 10697500
'''
This script scrapes IMDB and outputs a CSV file with highest rated tv series.
'''
import csv

from pattern.web import URL, DOM

TARGET_URL = "http://www.imdb.com/search/title?num_votes=5000,&sort=user_rating,desc&start=1&title_type=tv_series"
BACKUP_HTML = 'tvseries.html'
OUTPUT_CSV = 'tvseries.csv'


def extract_tvseries(dom):
    '''
    Extract a list of highest rated TV series from DOM (of IMDB page).

    Each TV series entry should contain the following fields:
    - TV Title
    - Rating
    - Genres (comma separated if more than one)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    '''
    tv_series = []
    
    # iterate over every tv serie
    for i in dom.body.by_class("lister-item-content"):

        # extract title, rating genres, runtime
        title = i.by_tag("a")[0].content.encode('utf-8')
        rating = i.by_tag("strong")[0].content.encode('utf-8')
        genres = i.by_class("genre")[0].content.encode('utf-8').strip("\n").strip(12*" ")
        runtime = i.by_class("runtime")[0].content.strip(" min").encode('utf-8')
        
        # extract every actor seperately and concatenate them together with commas
        actorlist = []
        for j in range(4):
            actor =  i.by_tag("p")[2].by_tag("a")[j].content.encode('utf-8')
            actorlist.append(actor)
        actors= ",".join(actorlist)
        # save serie as list
        serie = [title, rating, genres, actors, runtime]

        # add serie list to tvseries list
        tv_series.append(serie)

    
    # ADD YOUR CODE HERE TO EXTRACT THE ABOVE INFORMATION ABOUT THE
    # HIGHEST RATED TV-SERIES
    # NOTE: FOR THIS EXERCISE YOU ARE ALLOWED (BUT NOT REQUIRED) TO IGNORE
    # UNICODE CHARACTERS AND SIMPLY LEAVE THEM OUT OF THE OUTPUT.
    print tv_series
    return tv_series


def save_csv(f, tvseries):
    '''
    Output a CSV file containing highest rated TV-series.
    '''
    writer = csv.writer(f)
    writer.writerow(['Title', 'Rating', 'Genre', 'Actors', 'Runtime'])
    
    # write for every item in tvseries, every list in seperately on a row
    for item in tvseries:
        writer.writerow([item[i] for i in range(5)])
    # ADD SOME CODE OF YOURSELF HERE TO WRITE THE TV-SERIES TO DISK

if __name__ == '__main__':
    # Download the HTML file
    url = URL(TARGET_URL)
    html = url.download()

    # Save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # Parse the HTML file into a DOM representation
    dom = DOM(html)

    # Extract the tv series (using the function you implemented)
    tvseries = extract_tvseries(dom)

    # Write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'wb') as output_file:
        save_csv(output_file, tvseries)