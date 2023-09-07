
class TestCommentResource:

    def test_get_comments_for_task(self, app, db, comment_resource, task_exists_mock, task_comments_mock):
        with app.test_request_context('/api/v1/tasks/1/comments', method='GET'):
            response = comment_resource.get(task_id=1)

            response_data = response[0]
            response_status = response[1]

            assert response_status.value == 200
            assert response_data['status'] == 'success'

    def test_get_comments_for_invalid_task(self, app, db, comment_resource):
        with app.test_request_context('/api/v1/tasks/invalid_task_id/comments', method='GET'):
            response = comment_resource.get(task_id='invalid_task_id')
            response_status = response[1]

            assert response_status.value == 404

