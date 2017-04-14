# Ranker
A web-based application for organizing and ranking collections of ideas across topics, like "best casual restaurants" or "most iconic Bruce Willis movies".

## Where it lives
The Ranker app is still in development, so there isn't a live instance of it available. Sorry!

## How it works
The basic idea is to use an ELO-based ranking algorithm to sort lists of options, such as local restaurants or 90s pop songs. Options can be associated with topics like "Best Casual Dining" and compared with other options within the same topic in randomly selected contests - one option will win, raising its score and ranking in the topic.

## Contributing
Want to help out? Awesome! At the moment this is just a personal project to get to play with end-to-end full stack concepts like using Vagrant and Ansible to configure nginx and Gunicorn to host Django for the backend, Angular and SCSS for the user interface, and eventually AWS hosting with EC2 and S3. Over time I plan on expanding the concepts into more and more areas, so if you'd like to help out here's how:

### Getting started
The goal is to have the entire application live inside of a Vagrant image that's configured via Ansible, so all you'll need to do to get started is:
* Install Vagrant
* Check out the git repository
* Run `vagrant up`
* Start the server with `vagrant ssh "/vagrant/Ranker/manage.py runserver 0.0.0.0:8000"`

We're not quite there yet, but getting Django to run within Vagrant is a high priority once basic functionality is ready.
