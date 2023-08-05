CHANGE LOG
==========

1.3.0
-----
- Added yourwords wagtailadmin for CentralCMS

1.2.2
-----
- Add yourwords permission to groups

1.2.1
-----
- Updated YourWords markup to

1.2.0
-----
- Add YourWords to sections

1.1.4
-----
- Server srcset image thumbnail

1.1.3
-----
- Home page thumbnail and main page images

NOTE: Templates updates

1.1.2
-----
- Return None if there is no competition

1.1.1
-----
- BEM templates methodology

1.1.0
-----
- Add support for hiding untranslated content

1.0.2
-----
- Removed `http://testserver` from test URLs

1.0.1
-----

- Restructured your words competition to introduce index page

NOTE: This release is not compatible with molo versions less than 3.0

1.0.0
-----

- Added multi-language support

Backwards incompatible changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- deprecated use of ``LanguagePage``: your words competition is now direct child of ``Main`` (use ``SiteLanguage`` for multilanguage support)
- deprecated use of ``competition.thank_you_page``: use the template tag ``{% load_thank_you_page_for_competition competition as thank_you_pages %}``

NOTE: This release is not compatible with molo versions less than 3.0

0.0.2
-----
- update django admin
- add convert to article functionality

0.0.1
-----
- initial release
