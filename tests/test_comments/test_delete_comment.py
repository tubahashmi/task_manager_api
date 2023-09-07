import json


class TestCommentResource:
    def test_delete_comment_with_valid_data(self, app, db, comment_resource, task_exists_mock, comment_exists_mock):
        with app.test_request_context('/api/v1/tasks/123abc/comments/456def', method='DELETE'):

            response = comment_resource.delete(task_id='123abc', comment_id='456def')
            response_data = response[0]
            response_status = response[1]

            assert response_status.value == 200
            assert response_data['status'] == 'success'


    def test_delete_comment_with_invalid_task(self, app, db, comment_resource):
        with app.test_request_context('/api/v1/tasks/invalid_task_id/comments/456def', method='DELETE'):
            response = comment_resource.delete(task_id='invalid_task_id', comment_id='456def')

            response_data = response[0]
            response_status = response[1]

            assert response_status.value == 404
            assert response_data['status'] == 'failed'


    def test_delete_comment_with_invalid_comment(self, app, db, comment_resource):
        with app.test_request_context('/api/v1/tasks/123abc/comments/invalid_comment_id', method='DELETE'):
            response = comment_resource.delete(task_id='123abc', comment_id='invalid_comment_id')

            response_data = response[0]
            response_status = response[1]

            assert response_status.value == 404
            assert response_data['status'] == 'failed'