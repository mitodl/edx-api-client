Release Notes
=============

Version 0.7.0
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

