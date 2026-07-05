FROM kivy/buildozer:latest

WORKDIR /home/user/app

COPY . /home/user/app

RUN pip install --upgrade pip
RUN pip install buildozer==1.6.0 Cython==0.29.37

ENV BUILDOZER_WARN_ON_ROOT=0

ENTRYPOINT ["sh","-c","yes | buildozer -v android debug"]
