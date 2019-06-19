# edx-api-client
[![codecov.io](https://codecov.io/github/mitodl/edx-api-client/coverage.svg?branch=master)](https://codecov.io/github/mitodl/edx-api-client?branch=master)
Python interface for edX REST APIs

## Installation

To get the latest stable release from PyPi

```bash
pip install edx-api-client
```

To get the latest commit from GitHub

```bash
pip install -e git+git://github.com/mitodl/edx-api-client.git#egg=edx-api-client
```


## Tests

If you're going to run integration tests, you'll need to specify the
`ACCESS_TOKEN` environment variable to a valid access token.

You can create an access token (and the associated oauth app, and
grant) through the edX admin.

If you're going to run the integration tests against localhost, you'll
additionally need to turn off TLS validation with the environment
variable `OAUTHLIB_INSECURE_TRANSPORT=1`. This will skip the HTTPS
validation which is required by the OAuth spec.

Your edx demo course (course id `course-v1:edX+DemoX+Demo_Course`)
must be enabled for CCX.

The Course Enrollment integration tests have the following requirements:
- The `API_KEY` value must match the `settings.EDX_API_TOKEN` value in LMS
- The user assigned to that `ACCESS_TOKEN` must be an admin in the edX demo course.
  Adding a user as an admin can be done in Studio (url: `<studio_url>/course_team/course-v1:edX+DemoX+Demo_Course`

## Release Notes

See the RELEASE.rst file
