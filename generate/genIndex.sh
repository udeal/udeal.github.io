rm -rf body.html 
python3 genBody.py
cat head.html body.html tail.html > ../index.html

