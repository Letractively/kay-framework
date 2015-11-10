# Introduction #

This document is modeled after Django's release policy document found at the following url.

http://docs.djangoproject.com/en/dev/internals/release-process/

# Official releases #

Kay’s release numbering works as follows:

  * Versions are numbered in the form A.B or A.B.C.
  * A is the major version number, which is only incremented for major changes to Kay, and these changes are not necessarily backwards-compatible. That is, code you wrote for Kay 6.0 may break when we release Kay 7.0.
  * B is the minor version number, which is incremented for large yet backwards compatible changes. Code written for Kay 6.4 will continue to work under Kay 6.5.
  * C is the micro version number which, is incremented for bug and security fixes. A new micro-release will always be 100% backwards-compatible with the previous micro-release.

In some cases, we’ll make alpha, beta, or release candidate releases. These are of the form A.B alpha/beta/rc N, which means the Nth alpha/beta/release candidate of version A.B.
An exception to this version numbering scheme is the pre-1.0 code. There’s no guarantee of backwards-compatibility until the 1.0 release.

In mercurial, each Kay release will be tagged under **Tags**.

# Major releases #

Major releases (1.0, 2.0, etc.) will happen every year on Kay's birthday which is July 7th. These releases will frequently represent major, sweeping changes to Kay as he progresses.

# Minor releases #

Because of the relative speed of new releases of the appengine SDK, minor releases (1.1, 1.2, etc.) will happen roughly every two months – see release process, below for details.

These releases will contain new features, improvements to existing features, and such. A minor release may deprecate certain features from previous releases. If a feature in version A.B is deprecated, it will continue to work in version A.B+2. In version A.B and A.B+1 deprecation messages will be logged with a level of info if DEBUG is turned on in the settings.py. A.B+2 will log deprecation warnings with a level of warning regardless of the DEBUG setting. **Version A.B+3 will remove the feature entirely**. This will give you, roughly, 3 release versions `*` 2 month release cycle = **6 months** to update your code.

So, for example, if we decided to remove a function that existed in Kay 1.0:

  * Kay 1.1 will contain a backwards-compatible replica of the function which will log an info level deprecation message in DEBUG mode.
  * Kay 1.2 will also log an info level deprecation message in DEBUG mode.
  * Kay 1.3 will contain the backwards-compatible replica, but the warning will be promoted to a full-fledged warning. This warning is loud by default, and will likely be quite annoying.
  * Kay 1.4 will remove the feature outright.

# Micro releases #

Micro releases (1.0.1, 1.0.2, 1.1.1, etc.) will be issued to fix serious bugs and security issues. Micro releases may or may not be released in between minor releases.

These releases will always be 100% compatible with the associated minor release – the answer to “should I upgrade to the latest micro release?” will always be “yes.”

# Branching #

Releases are released from the default branch of mercurial. Releases branches will  be maintained however development will not occur in this branch directly. Branches for individual issues named off of the issue number will be created and merged into the release branch before a release. The issues that make it into a release will be determined to some extent before the release is made but an issue is not guaranteed to be added to a release until it is merged into the default branch.

# Supported versions #

At any moment in time, Kay’s developer team will support a set of releases to varying levels:

The mercurial repository will get new features and bug fixes requiring major refactoring. All bug fixes applied to the default will also be applied to the last minor release, to be released as the next micro release.
Security fixes will be applied to the current trunk and the previous two minor releases.
As a concrete example, consider a moment in time halfway between the release of Kay 1.3 and 1.4. At this point in time:

Features will be added to the default branch, to be released as Kay 1.4.
Bug fixes will be applied to a 1.3.X branch, and released as 1.3.1, 1.3.2, etc.
Security releases will be applied to the default branch, a 1.3.X branch and a 1.2.X branch. Security fixes will trigger the release of 1.3.1, 1.2.1, etc.

**Note: Will will not be supporting versions prior to 1.0**

# Release process #

Kay uses a time-based release schedule, with minor (i.e. 1.1, 1.2, etc.) releases roughly every two months, depending on features.

After each previous release (and after a suitable cooling-off period of a week or two), the core development team will examine the landscape and announce a timeline for the next release. Most releases will be scheduled in the 2 month range, but if we have bigger features to develop we might schedule a longer period to allow for more ambitious work.

# Release cycle #

Each release cycle will be split into three periods, each lasting roughly one-third of the cycle:

## PHASE ONE: FEATURE PROPOSAL ##

The first phase of the release process will be devoted to figuring out what features to include in the next version. This should include a good deal of preliminary work on those features – working code trumps grand design.

At the end of part one, the core developers will propose a feature list for the upcoming release. This will be broken into:

  * "Must-have”: critical features that will delay the release if not finished
  * "Maybe” features: that will be pushed to the next release if not finished
  * "Not going to happen”: features explicitly deferred to a later release.

"Must-have" and "Maybe" features will be marked with a Milestone-ReleaseX.X, where X.X is the release version. However, this does not guarantee their inclusion in the release.

## PHASE TWO: DEVELOPMENT ##

The second third of the release schedule is the “heads-down” working period. Using the roadmap produced at the end of phase one, we’ll all work very hard to get everything on it done.

At the end of phase two, any unfinished features will be postponed until the next release. Though it shouldn’t happen, any “must-have” features will extend phase two, and thus postpone the final release.

Phase two will culminate with an alpha release.

## PHASE THREE: BUGFIXES ##

The last third of a release is spent fixing bugs – no new features will be accepted during this time. We’ll release a beta release about halfway through, and an rc complete with string freeze two weeks before the end of the schedule.

### Bug-fix releases ###

After a minor release (i.e 1.1), the previous release will go into bug-fix mode.