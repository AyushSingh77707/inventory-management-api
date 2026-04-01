FROM python:3.11-slim        #i want python 3.11 ready made environment

WORKDIR /app                 #working folder set

COPY requirements.txt .      #requirement.txt container me copy kro

RUN pip install --no-cache-dir -r requirements.txt            #sare pips install kro container me

COPY . .          #mera pura project container me copy kro

EXPOSE 8000           #meri api 8000 port pe chalegi

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]    # container start hone pe ye commands chalegi