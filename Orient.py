import click
from colorama import Fore,Style
#top_movies,ratings,user_accuracy,female_users,age_user, tech_job_users,zip_code_users = recs.get_recommendations('F',25,'programmer','94123',1.0,1.0,1.0,1.0)
#del recs

def colored(string,color):
    return color + string+Fore.RESET

@click.command()
def dialogue():
    click.echo('Welcome to Orient! Let\'s get you some recommendations.')
    name = click.prompt(colored('Enter your name',Fore.MAGENTA))
    #click.echo(name)
    age = click.prompt(colored('Enter your age',Fore.YELLOW), type=int)
    #click.echo(age,type(age))
    gender = click.prompt(colored('Enter gender(M/F)',Fore.GREEN), type= click.Choice(['M','F']))
    #click.echo(gender,type(gender))
    location = click.prompt(colored('Enter your ZIPcode',Fore.CYAN))
    #click.echo(location,type(location))
    click.clear()
    occupation = click.echo(colored('Enter the number corresponding to your occupation from the list above',Fore.MAGENTA))


    job = ['administrator',
    'artist',
    'doctor',
    'educator',
    'engineer',
    'entertainment',
    'executive',
    'healthcare',
    'homemaker',
    'lawyer',
    'librarian',
    'marketing',
    'none',
    'other',
    'programmer',
    'retired',
    'salesman',
    'scientist',
    'student',
    'technician',
    'writer']

    for i,j in enumerate(job):
        click.echo(j+'|'+str(i))

    occupation = click.prompt('')
    #click.echo(occupation,type(occupation))

    click.clear()
    genres = click.echo(colored('Enter the numbers corresponding to your favorite genres (separate with commas)',Fore.YELLOW))

    genre = ['unknown',
    'Action',
    'Adventure',
    'Animation',
    'Children\'s',
    'Comedy',
    'Crime',
    'Documentary',
    'Drama',
    'Fantasy',
    'Film-Noir',
    'Horror',
    'Musical',
    'Mystery',
    'Romance',
    'Sci-Fi',
    'Thriller',
    'War',
    'Western']

    for i,g in enumerate(genre):
        click.echo(g+'|'+str(i))

    g_choices = click.prompt('')

    click.clear()
    click.echo(Fore.GREEN + '__' * 20)
    click.echo(f'Thank you {name} here are your recommendations:')
    click.echo(Style.RESET_ALL)

    W_gen=0.25
    W_age=0.25
    W_job=0.75
    W_zip=0.25

    import Recommendations as recs
    top_movies,ratings,user_accuracy,female_users,age_user, tech_job_users,zip_code_users = recs.get_recommendations(gender,age,'programmer',location,W_gen,W_age,W_job,W_zip)
    #del recs
    click.echo(f'Movies (year) Average Rating):\n {top_movies}')

    while True:
        choice = ['gender','age','occupation']
        selection = click.prompt('Which weights do you want to change?')

    sim_u_profiles = click.prompt(colored('How many similar user profiles would you like to be compared with? (Default = 10): ',Fore.CYAN), type=int)
    n_movies = click.prompt(colored('How many movies would you like recommended to you? (Default = 3): ',Fore.MAGENTA), type=int)

    rating_cut = click.prompt(colored('At least how many stars would you like your movie to have? (Default = 3): ',Fore.GREEN), type=int)

if __name__ == '__main__':
    dialogue()
