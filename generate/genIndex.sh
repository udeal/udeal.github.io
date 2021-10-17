rm -rf body2.html 
python3 genBody.py
cat body1.html body2.html body3.html > ../index.html

