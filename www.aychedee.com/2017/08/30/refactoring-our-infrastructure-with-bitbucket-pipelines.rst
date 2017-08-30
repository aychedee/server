public: yes
tags: [infrastructure, development]
summary: |
  Creating a safe environment for engineers to write code is the most important
  part of my job. We recently refactored our infrastructure to use bitbuckets
  new pipelines feature and it's been a great success.

Refactoring Touch Surgery’s infrastructure using Bitbucket Pipelines
====================================================================

I’m a strong believer that having great processes makes great engineering
possible. Fear really is the mind killer when it comes to improving on an
existing product or creating something new. If an engineer is scared to make a
change, then chances are they’re not going to do it. Especially without seeking
permission from someone else.

Touch Surgery’s existing infrastructure had some characteristics that made it
scary for our engineering team:

* Servers had been modified by hand and existed forever
* The deploy process had to be run from specific environments and involved downtime for the API
* There was no easy way to replace it if a disaster occurred
* Upgrading packages or the entire OS was pretty much infeasible and would have caused downtime

With that in mind, we recently rebuilt our primary engineering work flow to be
automatic, easy to use, and safe.

We built this infrastructure using `BitBucket Pipelines <https://bitbucket.org/product/features/pipelines>`_,
a new offering from Atlassian. At the moment it’s a minimal product with exactly
the features we need to build what we want.

The new workflow incorporates continuous integration and continuous deployment.
Our fleet of special snowflakes were entirely replaced by immutable servers.
These are destroyed and replaced with every deploy. Deploying the latest
version of our platform now involves no downtime. Which is great because we’re
doing it many times a day.

Continuous integration
----------------------

Each commit made to our code base triggers the the automated quality assurance
process. The steps, in order of increasing time taken, and complexity are:

* Does the code still meet our linting standards?
* Should these changes be accompanied by a database migration?
* Do the supplied database migrations work?
* Do our tests pass?
* Do our build scripts complete successfully?

If a commit can pass these hurdles. Then we’re confident it can be deployed and
used by our customers.

Building configured Amazon Machine Images (AMIs)
------------------------------------------------

Once the quality process has been completed successfully and the commit is on
an actively deployed branch we use packer to build a universal AMI that
contains the current code and the necessary environment to run our application.
The same image can be used to launch any one of our server types. Which are
currently: Application, celery, content or scheduler.

Automated deployment
--------------------

The entire AWS environment is created through Ansible roles. We have roles that create:

* Our per environment virtual private cloud
* The database, working from a particular snapshot (in practice this is only regularly done in testing and staging environments - Where they are created from an anonymised snapshot of the production DB)
* The elastic loadbalancer
* The Redis cluster - used for caching and celery task management
* The autoscaled app servers
* The celery scheduler
* And the autoscaled celery workers

Each environment (testing, staging, production) has a playbook that combines
these roles and deploys the latest built image into them.

The great thing about this approach is that our entire infrastructure lives in
code, in a disaster, or if the security of our environment was compromised, we
could delete it entirely and be back up and running within an hour.

The deployment process for our three environments uses these same
playbooks. They deploy each new platform release with zero downtime.

Custom tools
------------

We also created three custom pipeline jobs

* Rollback to commit
* Deploy to staging
* Create test environment

These three commands give our engineers the simple tools to manage the
environment in emergencies, test their code in the deploy process or to show
the product team work, to get signoff, prior to it being released.

*Rollback* is only there as an emergency measure. It lets an engineer quickly
deploy the pre-built image for a particular commit. Unlike the normal deploy
process there is an additional sanity check performed. Which is: “Has this
commit been successfully deployed to production before?” If that’s not the case
we just fail. Even though `"you can’t have a rollback button" <https://blog.skyliner.io/you-cant-have-a-rollback-button-83e914f420d9>`_ this can still be
useful.

Deploying a commit to the *staging environment* is a way for engineers to test
the entire deployment process, including database migrations, before their code
is merged into master and the automated process kicks in.

Creating a *custom test environment* is the primary way for an engineer to show their
work to other members of Touch Surgery. The output of running this command is a
scaled down, isolated environment with a url unique to this commit. This gives
ultimate flexibility. Nobody is blocked because the staging environment is
broken or busy. If you want to show your work to someone else you can. We
destroy these environments every night so that they don’t accumulate. But since
each one is only a load balancer and a micro instances they only cost a $0.30 a
day. In fact our entire development infrastructure costs us ~ $100 /
month on AWS.

Together these three custom tools give individual developers most of the
control over our environment that they need on a day to day basis without
requiring special access to anything sensitive.

~~~

We’ve had this new infrastructure running live now for two months. We’ve done
hundreds of deploys and created almost a thousand on demand test environments
without any downtime or outages that affected our users and customers. Most
importantly the confidence that our engineers now have when making changes is
night and day.

