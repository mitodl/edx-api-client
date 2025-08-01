Release Notes
=============

Version 1.12.0
--------------

- feat: add basic course list API functionality (#119)
- chore(deps): pin actions/cache action to 5a3ec84 (#109)
- chore(deps): update dependency ubuntu to v24 (#116)
- chore(deps): update codecov/codecov-action action to v5 (#117)

Version 1.11.0 (Released May 27, 2025)
--------------

- feat: Add course runs API management (#121)
- chore(deps): update actions/checkout action to v4 (#111)
- chore(deps): update actions/setup-python action to v5 (#112)
- chore(deps): update dependency python to 3.13 (#118)
- ci: update ubuntu runner and cache action (#120)

Version 1.10.0 (Released August 19, 2024)
--------------

- feat: validate user registration api (#106)
- chore: bump python to 3.9 (#107)
- Add renovate.json

Version 1.9.0 (Released May 22, 2024)
-------------

- refactor: remove X-EdX-Api-Key usage (#104)

Version 1.8.0 (Released August 16, 2023)
-------------

- feat: add bulk retirement api (#100)
- Delete PR Template

Version 1.7.0 (Released March 14, 2023)
-------------

- feat: add certificate_available_date in course detail (#98)

Version 1.6.0 (Released December 15, 2022)
-------------

- added support for force enrollment on openedx (#96)

Version 1.5.0 (Released October 21, 2022)
-------------

- feat: add course pacing property (#93)

Version 1.4.1 (Released October 07, 2022)
-------------

- parentheses

Version 1.4.0 (Released October 07, 2022)
-------------

- Fix test?
- Update comment
- Fix and return array of CourseMode objects

Version 1.3.0 (Released September 09, 2022)
-------------

- format
- Try test
- Update cost test
- Fix test
- Update
- Fix test
- format
- cleanup
- fix 2
- Fix test
- Working hold

Version 1.2.0 (Released April 14, 2022)
-------------

- feat: add Verified mode enrollment creation (#85)

Version 1.1.0 (Released January 05, 2022)
-------------

- add api client for edx change email settings

Version 1.0.1 (Released August 25, 2021)
-------------

- Remove the check for username to match the grade username (#81)

Version 1.0.0 (Released June 09, 2021)
-------------

- Update dependencies, support only newer python

Version 0.12.0 (Released February 23, 2021)
--------------

- removing mixer package (#76)

Version 0.11.0 (Released December 17, 2020)
--------------

- Replace Travis with Github actions (#73)

Version 0.10.0 (Released December 03, 2020)
--------------

- Added API to update user name and removed pep8

Version 0.9.0 (Released December 19, 2019)
-------------

- Update CourseDetails client to pass username

Version 0.8.0 (Released August 30, 2019)
-------------

- Added unenrollment functionality

Version 0.7.1 (Released June 19, 2019)
-------------

- Allow for setting api_key to the edX API key

Version 0.7.0 (Released May 22, 2019)
-------------

- Allow to specify enrollment mode when creating enrollment for student
- Add functionality to query grades by course_id.
- Implement interface to call enrollments list from edx-platform. The new `edx_api.enrollments.CourseEnrollments.get_enrollments` method will return all the enrollments for one or multiple course_ids.

Version 0.6.1 (Released November 05, 2018)
-------------

- loosen requirements (#48)

Version 0.6.0 (Released October 29, 2018)
-------------

- Update grades API to v1 (#45)
- Update six version to latest (#46)

Version 0.5.0 (Released May 09, 2018)
-------------

- Added timeout in edx requests (#40)

Version 0.4.0 (Released June 02, 2017)
-------------

- Specify pylint version
- Lint
- Fix test
- Added user_info client
- Fix lint
- Lint
- Fix code coverage
- Updated client with edX newly added attributes in certificates api (#31)

Version 0.3.0 (Released September 22, 2016)
-------------

- Added capability to create enrollment in a course
- Added Current Grade REST API support

Version 0.2.1 (Released June 24, 2016)
-------------

- Removed pdbpp to not break compatibility with python 3.4
- Changed certificates function to raise HTTPError
- Upgraded some requirements
- Changed docstring to conform to return type

Version 0.2.0 (Released April 26, 2016)
-------------

- Added certificates client
- Added additional helpers for enrollments
- Added another helper method for enrollments

