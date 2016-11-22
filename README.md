# Gender-Age Analytics server

based on:

1. Caffe Docker forked from christopher5106/last_caffe_with_stn
2. http://www.openu.ac.il/home/hassner/projects/cnn_agegender/

manual build & run foreground
-----------------------------
1. sudo docker build -t gender docker/standalone/cpu
2. sudo docker run -p 5000:5000 -v /tmp:/opt/tmp -i -t gender

1. # put a.jpg in /tmp and then
2. curl "http://localhost:5000/analyze/a.jpg"


