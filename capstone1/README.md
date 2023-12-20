# Capstone1 project

# Tomato Leaf Disease Classification  

## Data
### Source: https://www.kaggle.com/datasets/ashishmotwani/tomato/data

Over 20k images of tomato leaves with 10 diseases and 1 healthy class. Images are collected from both lab scenes and in-the-wild scenes. 

Classes:
* Late_blight
* healthy
* Early_blight
* Septorialeafspot
* TomatoYellowLeafCurlVirus
* Bacterial_spot
* Target_Spot
* Tomatomosaicvirus
* Leaf_Mold
* Spidermites Two-spottedspider_mite
* Powdery Mildew

The goal is to develop a model that can predict tomato leaf disease and deploy it in a docker compose.

## Project folder structure

### capstone1
- code
  - Pipfile
  - Pipfile.lock
  - docker-compose.yaml
  - gateway.py
  - image-gateway.dockerfile
  - image-model.dockerfile
  - proto.py
  - test.py
  - tomato-model - **saved model**.
- model
    - data - **dataset**
      - big - **original dataset downloaded from kaggle**
      - small - **a smaller version of the original dataset**
  - Pipfile
  - Pipfile.lock
  - convertToSavedModel.ipynb - **converts .h5 to saved model**
  - createsmalldata.ipynb - **creates a smaller version of the original dataset**
  - notebook.ipynb - **EDA, find best model, save to .h5**
  - xception_v1_12_0.898.h5 - **the best model**
- README.md

**model** folder is used to train the model using small and big dataset, save the best model to .h5 file and convert it to the save model. 

**code** folder is used to create the model and the gateway services using docker-compose. The saved model created in the **model** folder is copied into this folder.

### Steps

The project was done in the following steps:  
Steps 1-7 were done in the **model** folder and in Kaggle notebook.  
Steps 8-10  were done in the **code** folder.  
This was done to have separate pipenv environments.

1. Download the dataset, unpack and copy **train** and **valid** folders to **.\model\data\big folder**.
2. Create a smaller version of the original dataset to play with the model. It was done in createsmalldata.ipynb.
3. In notebook.ipynb explore some metadata about the dataset, create different models based on the xception model, play with different metaparameters, like learning rate, inner dense layer sise, dropout size, epoch number.
4. Import the notebook into the Kaggle to benefits from GPU and train the final model using the original dataset with the thousands of images.
5. Save the best model to .h5 and download it to my computer.
6. Convert the .h5 model to the saved model using convertToSavedModel.ipynb notebook
7. Copy the saved model to the **code** folder.
8. Build docker images for the model and the gateway.
9. Start docker containers using docker-compose.
10. Test the service using **test.py**

### How to use saved model and create docker images

* Build model image
```bash
docker build -t tomato-model:xception-0898-001 \
  -f image-model.dockerfile .
```

* Build gateway image
```bash
docker build -t tomato-gateway:001 \
  -f image-gateway.dockerfile .
```

* Start docker-compose
```bash
docker-compose up -d
```

* Test the service
```bash
python test.py
```

* Stop docker-compose
```bash
docker-compose down
```

### Example

* Start docker-compose
```bash
(base) mogos@TOWER:~/projects/mlzoomcamp2023/capstone1/code$ docker-compose up -d
[+] Building 0.0s (0/0)   docker:default
[+] Running 2/2
 ✔ Container code-gateway-1       Started   0.0s 
 ✔ Container code-tomato-model-1  Started   0.0s 
```
* Test the service

To test the service I used an image of the tomate leaf with Leaf Mold disease
![Test image](https://vegcropshotline.org/wp-content/uploads/2018/08/3-CercosporaLeaf1.jpg)

It was taken from [here](https://vegcropshotline.org/article/tomato-leaf-mold-diseases/).

```bash
(base) mogos@TOWER:~/projects/mlzoomcamp2023/capstone1/code$ python test.py
{'Bacterial_spot': -1.736464262008667, 'Early_blight': -1.955533742904663, 'Late_blight': 5.443584442138672, 'Leaf_Mold': 9.409354209899902, 'Septoria_leaf_spot': -1.5283541679382324, 'Spider_mites Two-spotted_spider_mite': -9.764419555664062, 'Target_Spot': -11.01914119720459, 'Tomato_Yellow_Leaf_Curl_Virus': -5.174718856811523, 'Tomato_mosaic_virus': 1.2046741247177124, 'healthy': -11.281664848327637, 'powdery_mildew': -3.8318982124328613}
```

As you can see Leaf_Mold has the highest score: 'Leaf_Mold': 9.409354209899902

* Stop docker-compose
```bash
(base) mogos@TOWER:~/projects/mlzoomcamp2023/capstone1/code$ docker-compose down
[+] Running 3/3
 ✔ Container code-gateway-1       Removed    0.6s 
 ✔ Container code-tomato-model-1  Removed   10.4s 
 ✔ Network code_default           Removed    0.3s  
```