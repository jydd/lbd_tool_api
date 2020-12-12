FROM python:3.6.9
COPY ./ /app
WORKDIR /app
EXPOSE 5000
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ pipenv && pipenv install \
    && wget https://npm.taobao.org/mirrors/node/v14.15.1/node-v14.15.1-linux-x64.tar.xz -O ~/node.tar.xz \
    && tar xvJf ~/node.tar.xz -C ~/ && ln -s ~/node-v14.15.1-linux-x64/bin/* /usr/local/bin/ \
    && npm --registry https://registry.npm.taobao.org install
ENV TZ Asia/Shanghai
ENTRYPOINT ["/app/run.sh"]
