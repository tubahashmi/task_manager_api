import json


class TestCommentResource:

    def test_create_comment_with_valid_data(self, app, db, comment_resource, task_exists_mock):
        data = {'comment': 'This is a test comment.'}
        with app.test_request_context('/api/v1/tasks/1/comments', method='POST',
                                      data=json.dumps(data), content_type='application/json'):
            response = comment_resource.post(task_id=1)

        response_data = response[0]
        response_status = response[1]

        assert response_status.value == 201
        assert response_data['status'] == 'success'

    def test_create_comment_with_invalid_task(self, app, db, comment_resource):
        data = {'comment': 'This is a test comment.'}
        with app.test_request_context('/api/v1/tasks/invalid_task_id/comments', method='POST',
                                      data=json.dumps(data), content_type='application/json'):
            response = comment_resource.post(task_id='invalid_task_id')

        response_data = response[0]
        response_status = response[1]

        assert response_status.value == 404
        assert response_data['status'] == 'failed'

