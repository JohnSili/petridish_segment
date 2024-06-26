# petridish_segment
Project where we use Yolov5 for segmentation batteries on petri dish.  \
\
git clone https://github.com/JohnSili/petridish_segment.git \
cd petridish_segment \
git clone https://github.com/ultralytics/yolov5 \
cd yolov5 \
pip install Flask \
pip install -r requirements.txt \
cd .. \
\
for local test activate enviroment in your IDE\
python app.py #for local test \
\
for server test:\
source env/bin/activate \
flask --app app run --host=0.0.0.0 #for server\
