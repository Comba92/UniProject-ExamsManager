
# https://docs.sqlalchemy.org/en/14/core/ddl.html

# last_seen is updated when user logs in
# Then when user logs in, after the update, we check whether it is still premium
# if not we remove all the premium content from likes, playlists...
# We set premium to false

# TODO: same artist cannot publish songs with same names