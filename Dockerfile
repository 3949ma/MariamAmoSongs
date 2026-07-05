FROM kivy/buildozer:latest

WORKDIR /home/user/app

COPY . /home/user/app

RUN pip install --upgrade pip
RUN pip install buildozer==1.6.0 Cython==0.29.37

CMD ["buildozer", "-v", "android", "debug"]
