FROM amazonlinux AS libra-reminder-base

ENV DEBIAN_FRONTEND=noninteractive
RUN /usr/bin/yum update -y
RUN /usr/bin/yum upgrade -y
RUN /usr/bin/yum install -y python3.7
RUN /usr/bin/yum install -y python3-pip
RUN /usr/bin/yum install -y zip
RUN mkdir /root/libra_reminder





FROM libra-reminder-base AS libra-reminder
WORKDIR /root/libra_reminder
ADD requirements.txt /root/libra_reminder/requirements.txt
RUN STATIC_DEPS=true cat requirements.txt | STATIC_DEPS=true xargs /usr/bin/pip3 install -t /root/libra_reminder
ADD libra_reminder.py /root/libra_reminder/libra_reminder.py
ADD libra_scraper.py /root/libra_reminder/libra_scraper.py
ADD slack_notifier.py /root/libra_reminder/slack_notifier.py
RUN zip -r --quiet /root/libra_reminder/lambda-scraper ./*
CMD /bin/cp /root/libra_reminder/lambda-scraper.zip /tmp
