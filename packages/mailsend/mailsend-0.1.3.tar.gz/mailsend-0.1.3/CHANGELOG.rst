0.1.3 (released 2017-04-19)
---------------------------

- Added ability to send stdlib email.message.Message objects via mailsend

0.1.2 (released 2016-09-02)
---------------------------

- The mime structure of HTML emails is now compatible with Outlook 2011
- The SMTPUTF8 extension is requested when messages contain utf-8 addresses.
  (feature is available in Python 3.5 only)

0.1.1 (released 2015-12-21)
---------------------------

- Fixes for compatibility with envparse-0.2

0.1 (released 2015-12-19)
-------------------------

- Forked from https://github.com/rconradharris/tinysmtp
- Added configuration via URL (eg ``Connection('smtp://user@example.org')``)
- Various bug fixes
- Added ``rewrite_to`` argument to Mail class constructor method. This causes
  all messages to be rewritten to the given address(es), and is
  expected to be used for development/testing.
- Added ``bcc`` argument to Mail class constructor method. This causes
  all messages to be bcc'd to the given address(es).
- Added ``suppress_send`` argument to the Mail class constructor. This
  causes messages to not be sent (but may be still accessed via
  ``Mail.subscribe``)
