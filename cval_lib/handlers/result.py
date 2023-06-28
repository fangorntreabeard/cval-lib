"""
Introducing CVAL Rest API, a powerful tool for AI developers in the computer vision field.
Our service combines the concepts of human-in-the-loop and active learning to improve the quality of
your models and minimize annotation costs for classification, detection, and segmentation cases.

With CVAL, you can iteratively improve your models by following our active learning loop.
First, manually or semi-automatically annotate a random set of images.
Next, train your model and use uncertainty and diversity methods to score the remaining images for annotation.
Then, manually or semi-automatically annotate the images marked as more confident to increase the accuracy of the model.
Repeat this process until you achieve an acceptable quality of the model.

Our service makes it easy to implement this workflow and improve your models quickly and efficiently.
Try our demo notebook to see how CVAL can revolutionize your computer vision projects.

To obtain a client_api_key, please send a request to k.suhorukov@digital-quarters.com
"""

from requests import Session

from cval_lib.handlers._abstract_handler import AbstractHandler
from cval_lib.models.result import ResultResponse


class Result(AbstractHandler):
    """
    The result is the entity in which the processing data is stored
    """
    def __init__(
            self,
            session: Session,
    ):
        self.route = f'http://127.0.0.1:9940/api/result'
        self.result_id = None
        super().__init__(session)

    def _set_result_id(self, result_id: str = None):
        if result_id is None:
            result_id = self.result_id
        if result_id is None:
            raise ValueError('result_id cannot be None')
        self.result_id = result_id

    def get_result(self, result_id: str = None) -> ResultResponse:
        """
        :param result_id: id of result
        :return: ResultResponse
        """
        self._set_result_id(result_id)
        self._get(self.route + f'/{self.result_id}')
        return ResultResponse.parse_obj(self.send().json())

    def get_results(self, dataset_id: str = None, limit=100, ):
        """
        :param dataset_id: id of dataset
        :param limit: limit of returned objects
        :return:
        """
        self._get(self.route + 's', params={'limit': limit, 'dataset_id': dataset_id if dataset_id else 'null'})
        return [ResultResponse.parse_obj(i) for i in self.send().json()]
