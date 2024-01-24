import base64
import io
from PIL import Image
import numpy as np
import cv2
import mediapipe as mp
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
app=Flask(__name__)
try:
    with open("D:\.project\still-gorge-08761\server.txt") as f:
        lines=f.read()
        app.config['SERVER_NAME'] = lines
except:
    app.config['SERVER_NAME'] = 'still-gorge-08761.herokuapp.com' 
CORS(app)





class Model():
    def __init__(self):
        self.mediapipePose=mp.solutions.pose
        self.mediapipeModel=self.mediapipePose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mediapipeDrawing  = mp.solutions.drawing_utils
        self.createModel()
        self.poses=['Akarna_Dhanurasana',
 'Bharadvaja_s_Twist_pose_or_Bharadvajasana_I_',
 'Boat_Pose_or_Paripurna_Navasana_',
 'Bound_Angle_Pose_or_Baddha_Konasana_',
 'Bow_Pose_or_Dhanurasana_',
 'Bridge_Pose_or_Setu_Bandha_Sarvangasana_',
 'Camel_Pose_or_Ustrasana_',
 'Cat_Cow_Pose_or_Marjaryasana_',
 'Chair_Pose_or_Utkatasana_',
 'Child_Pose_or_Balasana_',
 'Cobra_Pose_or_Bhujangasana_',
 'Cockerel_Pose',
 'Corpse_Pose_or_Savasana_',
 'Cow_Face_Pose_or_Gomukhasana_',
 'Crane__Crow__Pose_or_Bakasana_',
 'Dolphin_Plank_Pose_or_Makara_Adho_Mukha_Svanasana_',
 'Dolphin_Pose_or_Ardha_Pincha_Mayurasana_',
 'Downward-Facing_Dog_pose_or_Adho_Mukha_Svanasana_',
 'Eagle_Pose_or_Garudasana_',
 'Eight-Angle_Pose_or_Astavakrasana_',
 'Extended_Puppy_Pose_or_Uttana_Shishosana_',
 'Extended_Revolved_Side_Angle_Pose_or_Utthita_Parsvakonasana_',
 'Extended_Revolved_Triangle_Pose_or_Utthita_Trikonasana_',
 'Feathered_Peacock_Pose_or_Pincha_Mayurasana_',
 'Firefly_Pose_or_Tittibhasana_',
 'Fish_Pose_or_Matsyasana_',
 'Four-Limbed_Staff_Pose_or_Chaturanga_Dandasana_',
 'Frog_Pose_or_Bhekasana',
 'Garland_Pose_or_Malasana_',
 'Gate_Pose_or_Parighasana_',
 'Half_Lord_of_the_Fishes_Pose_or_Ardha_Matsyendrasana_',
 'Half_Moon_Pose_or_Ardha_Chandrasana_',
 'Handstand_pose_or_Adho_Mukha_Vrksasana_',
 'Happy_Baby_Pose_or_Ananda_Balasana_',
 'Head-to-Knee_Forward_Bend_pose_or_Janu_Sirsasana_',
 'Heron_Pose_or_Krounchasana_',
 'Intense_Side_Stretch_Pose_or_Parsvottanasana_',
 'Legs-Up-the-Wall_Pose_or_Viparita_Karani_',
 'Locust_Pose_or_Salabhasana_',
 'Lord_of_the_Dance_Pose_or_Natarajasana_',
 'Low_Lunge_pose_or_Anjaneyasana_',
 'Noose_Pose_or_Pasasana_',
 'Peacock_Pose_or_Mayurasana_',
 'Pigeon_Pose_or_Kapotasana_',
 'Plank_Pose_or_Kumbhakasana_',
 'Plow_Pose_or_Halasana_',
 'Pose_Dedicated_to_the_Sage_Koundinya_or_Eka_Pada_Koundinyanasana_I_and_II',
 'Rajakapotasana',
 'Reclining_Hand-to-Big-Toe_Pose_or_Supta_Padangusthasana_',
 'Revolved_Head-to-Knee_Pose_or_Parivrtta_Janu_Sirsasana_',
 'Scale_Pose_or_Tolasana_',
 'Scorpion_pose_or_vrischikasana',
 'Seated_Forward_Bend_pose_or_Paschimottanasana_',
 'Shoulder-Pressing_Pose_or_Bhujapidasana_',
 'Side-Reclining_Leg_Lift_pose_or_Anantasana_',
 'Side_Crane__Crow__Pose_or_Parsva_Bakasana_',
 'Side_Plank_Pose_or_Vasisthasana_',
 'Sitting_pose_1__normal_',
 'Split_pose',
 'Staff_Pose_or_Dandasana_',
 'Standing_Forward_Bend_pose_or_Uttanasana_',
 'Standing_Split_pose_or_Urdhva_Prasarita_Eka_Padasana_',
 'Standing_big_toe_hold_pose_or_Utthita_Padangusthasana',
 'Supported_Headstand_pose_or_Salamba_Sirsasana_',
 'Supported_Shoulderstand_pose_or_Salamba_Sarvangasana_',
 'Supta_Baddha_Konasana_',
 'Supta_Virasana_Vajrasana',
 'Tortoise_Pose',
 'Tree_Pose_or_Vrksasana_',
 'Upward_Bow__Wheel__Pose_or_Urdhva_Dhanurasana_',
 'Upward_Facing_Two-Foot_Staff_Pose_or_Dwi_Pada_Viparita_Dandasana_',
 'Upward_Plank_Pose_or_Purvottanasana_',
 'Virasana_or_Vajrasana',
 'Warrior_III_Pose_or_Virabhadrasana_III_',
 'Warrior_II_Pose_or_Virabhadrasana_II_',
 'Warrior_I_Pose_or_Virabhadrasana_I_',
 'Wide-Angle_Seated_Forward_Bend_pose_or_Upavistha_Konasana_',
 'Wide-Legged_Forward_Bend_pose_or_Prasarita_Padottanasana_',
 'Wild_Thing_pose_or_Camatkarasana_',
 'Wind_Relieving_pose_or_Pawanmuktasana',
 'Yogic_sleep_pose',
 'viparita_virabhadrasana_or_reverse_warrior_pose']
    def createModel(self):
        with open("static/model.tflite","rb") as file:
            fileContent = file.read()
        self.interpreter = tf.lite.Interpreter(model_content=fileContent)
        self.interpreter.allocate_tensors()
        self.inputIndex = self.interpreter.get_input_details()[0]["index"]
        self.outputIndex = self.interpreter.get_output_details()[0]["index"]
        print("Model created")
    def predict(self,poseToPredict,inputImage):
        if(not self.interpreter):
            self.createModel()
        try:
            inputImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2RGB)
            mediapipeResults = self.mediapipeModel.process(inputImage)
            landmarks = mediapipeResults.pose_landmarks.landmark
            self.mediapipeDrawing.draw_landmarks(inputImage, mediapipeResults.pose_landmarks, self.mediapipePose.POSE_CONNECTIONS,
                                self.mediapipeDrawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                self.mediapipeDrawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                 ) 
            inputArray=[]
            for landmark in landmarks:
                inputArray.append([landmark.x,landmark.y])
            inputArray=[inputArray]
            inputArray=np.array(inputArray,"float32")
            inputArray=inputArray.reshape(1,33,2,1)
            self.interpreter.set_tensor(self.inputIndex, inputArray)
            self.interpreter.invoke()
            predictedResult = self.interpreter.get_tensor(self.outputIndex)
            if(poseToPredict<0):
                poseToPredict = predictedResult[0].argmax()
            return self.poses[poseToPredict],predictedResult[0][poseToPredict],inputImage
        except Exception as e:
            print("in Predict method",e)
            return "none",0,False
    def close(self):
        del self.interpreter
        del self.inputIndex
        del self.outputIndex
        print("model closed")






cnnModel = Model()
def frame(predictedPose):
    global image
    predictedPose,poseAccuracy,image = cnnModel.predict(predictedPose,image)
    if isinstance(image,bool):
        if(image==False):
            return(jsonify({"error":"Error occured"}))
    pillowImage = Image.fromarray(image)
    buffer = io.BytesIO()
    pillowImage.save(buffer, format="PNG")
    newImageAsString = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()
    resposeOutput={"data":newImageAsString,"score":str(round(poseAccuracy*100,2)),"pose":predictedPose}
    return (jsonify(resposeOutput))
@app.route("/web",methods=["POST"])
def web():
    global image
    if(request.method == "POST"):
        requestData=request.json["data"]
        requestData=requestData.split(",")[1]
        imageData=base64.b64decode(requestData)
        imageBytes=Image.open(io.BytesIO(imageData))
        image=np.array(imageBytes)
        pose=request.json["pose"]
        return frame(int(pose))

if __name__=="__main__":
    app.run() 