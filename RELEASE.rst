Release Notes
=============

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

