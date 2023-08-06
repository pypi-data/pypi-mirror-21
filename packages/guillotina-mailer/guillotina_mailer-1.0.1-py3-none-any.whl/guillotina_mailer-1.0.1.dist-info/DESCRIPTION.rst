.. contents::

guillotina_mailer
=================


Configuration
-------------

config.json can include mailer section::

    "applications": ["guillotina_mailer"],
    "mailer": {
      "default_sender": "foo@bar.com",
      "endpoints": {
        "default": {
          "type": "smtp",
          "host": "localhost",
          "port": 25
        }
      }
    }


Printing mailer
---------------

For development/debugging, you can use a console print mailer::

    "applications": ["guillotina_mailer"],
    "mailer": {
      "default_sender": "foo@bar.com",
      "endpoints": {
        "default": {
          "type": "smtp",
          "host": "localhost",
          "port": 25
        }
      },
      "utility": "guillotina_mailer.utility.PrintingMailerUtility"
    }


Sending mail
------------

POST http://localhost:8080/zodb/container/@mailer::

    {
      "sender": "foo@bar.com",
      "recipient": "john@doe.com",
      "subject": "Some subject",
      "text": "Hello"
    }


Permissions
-----------

`guillotina_mailer` defines a permission `mailer.SendMail` which, by default,
only the `guillotina.ContainerAdmin` role is assigned.


Using the mailer in code
------------------------

You can also directly use the mailer in your code::

    from guillotina.component import queryUtility
    from guillotina_mailer.interfaces import IMailer
    mailer = queryUtility(IMailer)
    await mailer.send(recipient='john@doe.com', subject='This is my subject', text='Body of email')

1.0.1 (2017-04-10)
------------------

- remove dependencies on repoze.sendmail and transaction
  [vangheem]

- Test mailer did not provide correct signature
  [vangheem]


1.0.0 (2017-04-04)
------------------

- Initial release moved from guillotina_mailer


