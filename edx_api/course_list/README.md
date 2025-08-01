# Course List API

The Course List API provides efficient retrieval of multiple courses with support for filtering and pagination.

## Usage

```python
from edx_api.client import EdxApi

client = EdxApi(credentials={'access_token': <token>}, base_url=<LMS_BASE_URL>)

# Get all courses
for course in client.course_list.get_courses():

# Filter by organization
for course in client.course_list.get_courses(org='MIT'):

# Get specific courses
course_keys = ['course-v1:edX+DemoX+Demo_Course', 'course-v1:MITx+6.00.1x+3T2015']
for course in client.course_list.get_courses(course_keys=course_keys):
```

## Rate Limiting

The edX API implements server-side rate limiting. The Course List client uses conservative defaults:
- **Page size**: Fixed at 100 courses per page
- **Batch size**: Fixed at 100 course keys per batch
- **Automatic pagination**: Handles multiple pages automatically

## API Reference

### `get_courses()`

Retrieves course information from the edX Course List API with support for filtering, batching, and pagination.

**Parameters:**
- `course_keys` (list, optional): List of course keys to retrieve.
- `org` (str, optional): Filter by organization code (e.g., "MIT").
- `search_term` (str, optional): Search term to filter courses.
- `username` (str, optional): The username whose visible courses to return.
- `active_only` (bool, optional): Only return non-ended courses.
- `**kwargs`: Additional query parameters

**Returns:**
- Generator yielding CourseDetail objects for each course
