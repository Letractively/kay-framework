# Introduction #

This is a document on how to work on Kay's core.

# Code Style #

Kay's code style follows Python's [PEP-8](http://www.python.org/dev/peps/pep-0008/) style guide with one difference. The indentation for Kay's core code is 2 space characters.


# Running Kay's Tests #

The automated tests for Kay's core can be run locally or on the Appengine service using [gaeunit](http://code.google.com/p/gaeunit/).

## Running Tests Locally ##

From Kay's root directory you can run the following command to run Kay's tests. This assumes that Kay can find the Appengine SDK. You can also run Kay's tests in the same way from your own project directory.

```
$ python manage.py test kay
```

## Running Tests on Appengine ##

1. Create a test project to upload to appengine.

```
$ python manage.py startproject kaytest
```

2. Set the appid and version in your app.yaml

3. After creating the project you will need to set the GAEUNIT\_INCLUDES\_KAY setting to True in your settings.py

```
GAEUNIT_INCLUDES_KAY = True
```

4. Upload the project to appengine.

```
$ python manage.py appcfg update
```

5. Access the url http:// `<appid>` .appspot.com/_ah/test to run the tests on the live appengine._

# Starting a Review #

Code reviews are conducted using the rietveld code review tool at http://codereview.appspot.com/

Reviews can be uploaded by using the upload.py tool that can be downloaded from http://codereview.appspot.com/use_uploadpy

After committing to your local mercurial repository, create a review with the following command.

```
upload.py -e <google account email> -m <review title> -d <review description> --send_mail -r <reviewer email>,<reviewer email> --rev=<start revision>:<end revision>
```

TODO: Updating reviews.

# Backporting Changesets #

Changes are backported from newer releases to previous release branches based on Kay's [Release Policy](ReleasePolicy.md).

1. Create a branch for the older minor release. The branch name should be something like v\_1.0.x or v\_1.1.x to denote minor version branches.

```
$ hg update v_1.0.x
$ hg branch v_1.0.x
```

2. Use the [mercurial transplant extension](http://mercurial.selenic.com/wiki/TransplantExtension) to backport the changeset. This will copy the changeset from the newer release branch to the older minor release branch.

```
$ hg transplant <changeset id>
```

# Creating A Kay Release #

Use the mercurial archive command to create a release.

```
$ hg archive -t tgz -r v_<major_version>.<minor_version>.<bugfix_version> kay-<major_version>.<minor_version>.<bugfix_version>.tar.gz
$ hg archive -t zip -r v_<major_version>.<minor_version>.<bugfix_version> kay-<major_version>.<minor_version>.<bugfix_version>.zip
```