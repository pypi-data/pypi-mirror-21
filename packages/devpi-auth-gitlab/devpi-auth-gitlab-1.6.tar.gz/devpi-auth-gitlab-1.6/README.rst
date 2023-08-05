=================
devpi-auth-gitlab
=================

An authentication plugin for use with gitlab-ci, utilising the built in registry token authentication scheme.

Installation
------------
Simply install the module onto the same server/python as your ``devpi-server`` installation
``pip install devpi-auth-gitlab``

You will need to specify your gitlab registry server.
This url can be found in the 'Registry' page of your gitlab project on a line like ``docker login registry.gitlab.com``

Add this server address to the devpi-server arguments when you run it.
``devpi-server --host 0.0.0.0 --port 3141 --gitlab-registry-url registry.gitlab.com``

Make sure any gitlab user you want as well as the "gitlab-ci-token" user is added to your devpi index's authentication list
``devpi index -c corona/prod volatile=False acl_upload="corona,gitlab-ci-token" bases="root/pypi" mirror_whitelist="*"``

Usage
-----

Usage from a Gitlab CI script is as simple as::

    deploy:
      script:
        - pip install devpi-client
        - devpi use https://devpi.localnet
        - devpi login "gitlab-ci-token" --password "$CI_BUILD_TOKEN"
        - devpi use "corona/prod"
        - devpi upload --formats sdist,bdist_wheel


Extra
-----
This hasn't been tested, but really this plugin is a docker registry authenticator.... as such you should be able to authenticate against any docker registry supporting v2 api