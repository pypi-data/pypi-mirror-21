=======
History
=======

Pending Release
---------------

* (Insert new release notes below this line)

1.1.0 (2017-04-27)
------------------

* Added Python 3 compatibility

1.0.0 (2017-03-22)
------------------

* Forked from RyanSB to Time Out.
* Allow rescheduling - by raising the new built-in ``NoResponse`` exception, a
  resource can avoid sending any messing to CloudFormation. This is to support
  Lambda functions that take >300 seconds to execute and thus reschedule
  themselves.

0.2.2 (2016-01-29)
------------------

* Last version `by RyanSB <https://github.com/ryansb/cfn-wrapper-python>`_.
