# Ranker
A web-based application for organizing and ranking collections of ideas across topics, like "best casual restaurants" or "most iconic Bruce Willis movies".

## Where it lives
The Ranker app is still in development, so there isn't a live instance of it available. Sorry!

## How it works
At its core, there are three main concepts:
* Options are a "thing" that can be categorized... a favorite movie, restaurant you want to check out, or cocktail recipe for an upcoming party. They can represent anything you want!
* Topics are contexts that options can be ranked against each other within. The best summer picnic spot by the beach might not be much good if you're trying to find a snowy hike in the woods, so you can use topics to give your options meaning when picking which is your favorite.
* Categories hold it all together, grouping topics and options into a single bucket so you don't get your Mad Max mixed in with your Lemon Meringue Pie

## Contributing
Want to help out? Awesome! At the moment this is just a personal project to get to play with end-to-end full stack concepts like using Vagrant and Ansible to configure nginx and Gunicorn to host Django for the backend, Angular and SCSS for the user interface, and eventually AWS hosting with EC2 and S3. Over time I plan on expanding the concepts into more and more areas, so if you'd like to help out here's how:

### Getting started
The goal is to have the entire application live inside of a Vagrant image that's configured via Ansible, so all you'll need to do to get started is:
* Install Vagrant
* Check out the git repository
* Run `vagrant up`
* Start the server with `vagrant ssh "/vagrant/Ranker/manage.py runserver 0.0.0.0:8000"`

We're not quite there yet, but getting Django to run within Vagrant is a high priority once basic functionality is ready.
