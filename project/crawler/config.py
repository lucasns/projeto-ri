import os

DOMAINS = {
            'rottentomatoes':   {'seed': 'https://www.rottentomatoes.com/',
                                 'robots_txt': ['license/export/', 'search', 'user', 'click',
                                                'logout', 'trailer', 'login', 'ajax'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'https://www.rottentomatoes.com/m/[^/\?]*$'
                                },

            'imdb':             {'seed': 'http://www.imdb.com/',
                                 'robots_txt': ['tvschedule', 'ActorSearch', 'ActressSearch', 'AddRecommendation',
                                                'ads/', 'AlternateVersions', 'AName', 'Awards', 'BAgent', 'Ballot/',
                                                'BornInYear', 'BornWhere', 'BPublicity', 'BQuotes', 'BTrivia',
                                                'BusinessThisDay', 'BWorks', 'careers', 'help/show_leaf?careeratimdb',
                                                'CommentsAuthor', 'CommentsEnter', 'CommentsIndex', 'Companies',
                                                'CrazyCredits', 'Credits', 'DiedInYear', 'DiedWhere', 'DVD', 'ExciteTitle',
                                                'Find', 'FName', 'GName', 'Guests', 'harvest_me', 'HelpPage', 'Icons/',
                                                'JointVentures', 'Laserdisc', 'List', 'Literature', 'Locations',
                                                'LocationTree', 'Lookup', 'M/', 'Maltin', 'MarriedInYear', 'MetaSearch',
                                                'Mlinks', 'More', 'Movies', 'Movies/', 'MyMovies', 'mymovies/',
                                                'name_pick_n_mix', 'Nsearch', 'NUrls', 'OnThisDay', 'Ontv', 'OnTV',
                                                'Overlap', 'Pawards', 'pick_n_mix', 'PName', 'Posters', 'prepare_data',
                                                'Psales', 'Quiz', 'r/', 'ra/', 'Ratings', 'rd/', 'Recommendations',
                                                'register', 'ReleaseDates', 'ReleasedInYear', 'Reviews', 'rg/', 'ri/',
                                                'RName', 'Sales', 'SearchAwards', 'SearchBios', 'SearchBusiness',
                                                'SearchCrazy', 'SearchDVD', 'SearchGoofs', 'SearchLaserdisc',
                                                'SearchLiterature', 'SearchPlots', 'SearchPlotWriters', 'SearchQuotes',
                                                'SearchRatios', 'SearchSongs', 'SearchTaglines', 'SearchTechnical',
                                                'SearchTrivia', 'SearchVersions', 'ShowAll', 'Showing', 'SName',
                                                'Soundtracks', 'Taglines', 'Tawards', 'Technical', 'tiger_redirect',
                                                'Title/ASIN', 'TitleBrowse', 'Trailers', 'Tsearch', 'TUrls', 'VName',
                                                'Vote', 'WorkedWith', 'updates', 'board', 'boards'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.imdb.com/title/.*/'
                                },

            'metacritic':       {'seed': 'http://www.metacritic.com/',
                                 'robots_txt': ['search', 'signup', 'login', 'user', 'jl/'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.metacritic.com/movie/[^/\?]*$'
                                },

            'movies':           {'seed': 'http://www.movies.com/',
                                 'robots_txt': ['undefined', 'Bin/', 'backlot/', 'controls/', 'reviews/controls/',
                                                'exclusives/controls/','search', 'narrow-your-search-results',
                                                'search-results', 'search-result', 'page-not-found'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.movies.com/[^/\?]*/m[0-9]*$'
                                },

            'allmovie':         {'seed': 'http://www.allmovie.com/',
                                 'robots_txt': ['admin', 'user/'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.allmovie.com/movie/[^/\?]*$'
                                },

            'flixster':         {'seed': 'http://www.flixster.com/',
                                 'robots_txt': ['actor/random', 'admin', 'address-book', 'api', 'bebo', 'captcha',
                                                 'converse.do', 'DoNotSend.jsp', 'facebook', 'friendsAction.do',
                                                 'friends.do', 'global-scripts', 'hi5', 'igoogle', 'invite',
                                                 'inviteDisplay.do', 'mctResults.do', 'metrics', 'mmessage',
                                                 'movie-facts', 'myspace', 'news/saved-stories',
                                                 'news/submitted-stories', 'page-scripts', 'people',
                                                 'people.do', 'rate-movies', 'recommendations', 'static/scripts',
                                                 'support', 'userAuth.do', 'ad.do', 'sponsors', 'misc',
                                                 'email-content', 'static/ads', 'user/'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.flixster.com/movie[s]?/[^/\?]*$'
                                },

            'tribute':          {'seed': 'http://www.tribute.ca/',
                                 'robots_txt': ['demo/', 'tvlistings/', 'ads/', 'doubleclick/', 'flash/', 'feeds/',
                                                'controls/', 'aspnet_client/', 'pages/', 'app_data/', 'css/',
                                                'lib/', 'config/', 'aspnet_client/', 'rma/'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.tribute.ca/movies/[^/\?]*/[0-9]*/$'
                                },

            'boxofficemojo':    {'seed': 'http://www.boxofficemojo.com/',
                                 'robots_txt': ['movies/default.movies.htm', 'showtimes/buy.php', 'forums/',
                                 'derbygame/', 'grades/', 'moviehangman/', 'users/'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://www.boxofficemojo.com/movies/\?id=.*'
                                },

            'mubi':             {'seed': 'https://mubi.com/',
                                 'robots_txt': ['login'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'https://mubi.com/films/*[^/\?]*$'
                                },

            'yify':             {'seed': 'http://yify.info/',
                                 'robots_txt': ['engine/go.php', 'engine/download.php', 'user/', 'newposts/',
                                                'statistics.html'],
                                 'sleep_time': 1,
                                 'movies_pattern': r'http://yify.info/[^(?!tv$)].*/[0-9]*[-].*.html$'
                                }
        }


USER_AGENT = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
FILES_PATH = os.path.join(DIR_PATH, "files")

if not os.path.exists(FILES_PATH):
    os.makedirs(FILES_PATH)
