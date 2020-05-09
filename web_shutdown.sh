ps auxww | grep 'runserver' | awk '{print $2}' | xargs kill -9
