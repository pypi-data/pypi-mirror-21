##################
Contribution Guide
##################

We welcome and encourage community contributions to this work.

Please familiarise yourself with these contribution guidelines before
contributing.


Ways to Contribute
==================

There are many ways to help improve this work:

* Find and `report bugs <Pagure issues_>`_ with detailed information
  to troubleshoot.

* The set of `issues open for newcomer contributions <Pagure newcomer
  label_>`_ makes it easy to find a bug you might be able to fix.

* Correct and `improve the documentation <Pagure project page>`_,
  especially while still learning how to use the project.

..  _Pagure issues: https://pagure.io/python-configdeck/issues
..  _Pagure project page: https://pagure.io/python-configdeck/
..  _Pagure newcomer label:
    https://pagure.io/python-configdeck/issues?tags=newcomer


Contributing Code
=================

All code contributions are made via `merge request <Pagure merge
requests_>`_ (also called “pull request”). *All code changes from all
contributors are reviewed* in a merge request, before deciding whether
to accept the changes. Once the merge request is created, other
contributors will offer feedback, and if the changes pass review a
maintainer will accept the request by merging it with a comment.

When the merge request do not have a clean report from automated tests
and merge preview, authors are expected to update their merge requests
to address the test failures and conflicts, until all tests pass and
the pull request merges successfully.

At least one review from a maintainer is required for all changes
(even changes from maintainers).

Reviewers should leave a “LGTM” comment once they are satisfied with
the change. If the change was submitted by a maintainer with write
access, the pull request should be merged by the submitter after
review.

..  _Pagure merge requests:
    https://pagure.io/python-configdeck/pull-requests/


Code Style
==========

Ensure your text editor complies with the `EditorConfig`_ settings in
the code base.

All Python code must conform to :PEP:`8`.

..  _EditorConfig: http://editorconfig.org/


Developer Certificate of Origin
===============================

All contributions must include acceptance of the Developer Certificate
of Origin (DCO, originally `from the Linux Foundation <Linux
Foundation Developer Certificate of Origin_>`_):

    ..  include:: developer-certificate-of-origin

..  _Linux Foundation Developer Certificate of Origin:
    https://developercertificate.org/

To accept this DCO, simply add this line to each Git commit message
(using ``git commit -s`` will do this for you) with your real name and
email address::

    Signed-off-by: Jane Example <jane@example.com>

To correctly track the provenance of changes, no anonymous or
pseudonymous contributions are accepted.


Merge request procedure
=======================

To make a merge request (also terms a “pull request”), you will need a
Pagure account. A merge request should have the `master` branch as its
destination.

Before creating a merge request, use this checklist:

* Check the :doc:`current and future road map <roadmap>` to see how
  your contribution fits the broader plan.

* If you do not have write access in the central repository, make a
  personal fork of the repository.

* Create a feature branch, starting from `master`, in which to make
  your changes.

* Use ``git rebase …`` to make your changes apply cleanly against the
  current `master` branch.

* Run the full test suite; correct any failures until all tests pass.

* Accept the `Developer Certificate of Origin`_ on all your commits.

* Create the merge request in Pagure, from your feature branch,
  targeting the `master` branch in the central repository.

The new merge request will be treated as a “code review” forum.
Maintainers will give feedback on the style and substance of the
changes.

Test coverage for changes
-------------------------

Normally, all changes must include tests that exercise your change,
pass with your change in place, and fail in the absence of the change.
Occasionally, a change will be very difficult to test for. In those
cases, please include a note in your commit message explaining why.


Contributor Covenant
====================

Whether you are a regular contributor or a newcomer, we care about
making this community a safe place for you and we’ve got your back.
This project is governed by the :doc:`Contributor Covenant Code of
Conduct <code-of-conduct>`.


..
    This document is written using `reStructuredText`_ markup, and can
    be rendered with `Docutils`_ to other formats.

    ..  _Docutils: http://docutils.sourceforge.net/
    ..  _reStructuredText: http://docutils.sourceforge.net/rst.html

..
    Local variables:
    coding: utf-8
    mode: text
    mode: rst
    End:
    vim: fileencoding=utf-8 filetype=rst :
