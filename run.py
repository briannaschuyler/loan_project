#!/usr/bin/env python
from recommender import app

# Port has been changed from 5000 to 80 so the domain name (kivaloans4.me) doesn't need a :5000 on
# the end.  However, root is required to run any port below 1024 so I have to use the command:
# >> sudo /home/ubuntu/anaconda3/bin/python run.py
# Since sudo automatically wants to call its own version of python, so I have to be direct and
# specify it.
#app.run(debug=True, host='0.0.0.0', port=5000)
app.run(debug=True, host='0.0.0.0', port=80)

#app.run(debug=True)
