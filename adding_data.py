from app import db
from app.models import Temperatures, Humidities, Luminosities

data_1 = [20,21,22,23,24]
data_2 = [60,85,75,96,42]
data_3 = [50,87,96,45,85]


for i in range(5):
    temp = Temperatures(data=data_1[i])
    db.session.add(temp)


for i in range(5):
    hum = Humidities(data=data_2[i])
    db.session.add(hum)


for i in range(5):
    lum = Luminosities(data=data_3[i])
    db.session.add(lum)




db.session.commit()


