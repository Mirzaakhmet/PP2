#Function 2

# Dictionary of movies

movies = [
{
"name": "Usual Suspects", 
"imdb": 7.0,
"category": "Thriller"
},
{
"name": "Hitman",
"imdb": 6.3,
"category": "Action"
},
{
"name": "Dark Knight",
"imdb": 9.0,
"category": "Adventure"
},
{
"name": "The Help",
"imdb": 8.0,
"category": "Drama"
},
{
"name": "The Choice",
"imdb": 6.2,
"category": "Romance"
},
{
"name": "Colonia",
"imdb": 7.4,
"category": "Romance"
},
{
"name": "Love",
"imdb": 6.0,
"category": "Romance"
},
{
"name": "Bride Wars",
"imdb": 5.4,
"category": "Romance"
},
{
"name": "AlphaJet",
"imdb": 3.2,
"category": "War"
},
{
"name": "Ringing Crime",
"imdb": 4.0,
"category": "Crime"
},
{
"name": "Joking muck",
"imdb": 7.2,
"category": "Comedy"
},
{
"name": "What is the name",
"imdb": 9.2,
"category": "Suspense"
},
{
"name": "Detective",
"imdb": 7.0,
"category": "Suspense"
},
{
"name": "Exam",
"imdb": 4.2,
"category": "Thriller"
},
{
"name": "We Two",
"imdb": 7.2,
"category": "Romance"
}
]

#Task 1
def movie_rate_is_high():
    print('Choose a movie:')
    i = 0
    for description in movies:
        i += 1
        ij = str(i)+'>'
        print(f'{ij:<4}{description['name']}')

    
    choose = int(input('Enter movie number: '))

    if movies[choose-1]['imdb'] > 5.5:
        print(True)
    else:
        print(False)

#Task 2
def movies_55():
    movies_collection = []
    for description in movies:
        if description['imdb'] > 5.5:
            movies_collection.append(description['name'])

    j = 0
    print('Movies rated above 5.5:')
    for i in movies_collection:
        j += 1
        jj = str(j)+'.'
        print(f'{jj:<4}{i}')
        
#Task 3

def movies_category():
    categories = set()
    for descriptions in movies:
        categories.add(descriptions['category'])
    
    print('Movie categories:')
    j = 0
    for i in categories:
        j += 1
        ij = str(j)+'.'
        print(f'{ij:<3}{i}')
    
    choose = input('Select category: ')
    
    print(f'\nMovies in the category {choose}:')
    i = 0
    for descriptions in movies:
        if descriptions['category'] == choose:
            i += 1
            ij = str(i)+'.'
            print(f'{ij:<3}{descriptions['name']}')

#Task 4

def avg_imdb():
    arr = []
    for descriptions in movies:
        arr.append(descriptions['imdb'])
    print(f'Average IMDB score = {sum(arr)/len(arr):.2f}')

#Task 5

def avg_imdb_of_category():
    categories = set()
    for descriptions in movies:
        categories.add(descriptions['category'])

    j = 0
    for i in categories:
        j += 1
        ij = str(j)+'.'
        print(f'{ij:<3}{i}')

    choose = input('\nSelect movie category: ')
    arr = []
    for descriptions in movies:
        if descriptions['category'] == choose:
            arr.append(descriptions['imdb'])

    print(f'Average IMDB score = {sum(arr)/len(arr):.2f}')