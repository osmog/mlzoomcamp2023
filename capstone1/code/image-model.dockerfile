FROM tensorflow/serving:2.7.0

COPY tomato-model /models/tomato-model/1
ENV MODEL_NAME="tomato-model"