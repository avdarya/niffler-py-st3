
FROM python:3.12-slim

WORKDIR /niffler_tests_python

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget curl gnupg2 ca-certificates apt-transport-https \
    fonts-liberation \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2 libpango-1.0-0 \
    libpangocairo-1.0-0 libgtk-3-0 libx11-xcb1 libx11-6 libxext6 libxi6 libxtst6 \
    libdrm2 libxshmfence1 libglib2.0-0 unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

#RUN apt-get update && \
#    apt-get install -y wget gnupg ca-certificates curl \
#    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 \
#    libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2 libpango-1.0-0 \
#    libpangocairo-1.0-0 libgtk-3-0 libx11-xcb1 && \
#    apt-get clean && rm -rf /var/lib/apt/lists/*

#RUN apt-get update && apt-get install -y postgresql-client  && apt-get clean

#COPY ./requirements.txt /code/requirements.txt
#RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# Install Poetry and configure it to install into the system site-packages
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false

COPY niffler_tests_python/pyproject.toml niffler_tests_python/poetry.lock* ./
RUN poetry install --no-interaction --no-ansi --with dev
# Ensure Playwright Python package & pytest plugin are installed
RUN pip install --no-cache-dir playwright pytest-playwright
## Install browser(s) & system dependencies for Playwright
RUN python -m playwright install --with-deps chromium firefox

COPY niffler_tests_python/ /niffler_tests_python/
ENV PYTHONPATH="/niffler_tests_python"

#COPY ./app /code/app
#
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

ENTRYPOINT ["poetry", "run", "pytest"]

#docker build -t qaguru/niffler-py-tests:0.1 -f ./niffler_tests_python/Dockerfile .
# docker run --rm --env-file docker.env --network niffler-py-st3-avdarya_niffler-network  qaguru/niffler-py-tests:0.1 -s -v tests