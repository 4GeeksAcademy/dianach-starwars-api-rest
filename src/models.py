from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Planets(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(80), unique=False, nullable=False)
    gravity = db.Column(db.String(80), unique=False, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)
    rotation_period = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f"Planeta {self.planet_name}"
    
    def serialize(self):
        return{
            "planet_name" : self.planet_name,
            "id" : self.id,
            "gravity" : self.gravity,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,

        }
    
class Starships(db.Model):
    __tablename__ = "starships"
    id = db.Column(db.Integer, primary_key=True)
    starship_name = db.Column(db.String(30), unique=False, nullable=False) 
    model = db.Column(db.String(30), unique=False, nullable=False)
    starship_class = db.Column(db.String(30), unique=False, nullable=False)
    length = db.Column(db.String(30), unique=False, nullable=False)
    crew = db.Column(db.String(30), unique=False, nullable=False)

    def __repr__(self):
        return f"Nave {self.starship_name}"

    def serialize(self):
        return{
            "starship_name" : self.starship_name,
            "id" : self.id,
            "model" : self.model,
            "starship_class": self.starship_class,
            "length": self.length,
            "crew": self.crew,
     }   

class Characters(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(20), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    hair_color = db.Column(db.String(20), nullable=False)
    skin_color = db.Column(db.String(20), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"), nullable=True)
    planet = db.relationship(Planets)
    starship_id = db.Column(db.Integer, db.ForeignKey("starships.id"), nullable=True)
    starship = db.relationship(Starships)
    favorites = db.relationship("Favorites", back_populates="character")

    def __repr__(self):
        return f"{self.character_name}"
    
    def serialize(self):
        return {
            "character_name": self.character_name,
            "id": self.id,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color,
            "hair_color": self.hair_color,
            "planet": self.planet.serialize() if self.planet else None,
            "starship": self.starship.serialize() if self.starship else None,
        }

class Favorites(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(30), unique=True, nullable=False) 
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    starship_id = db.Column(db.Integer, db.ForeignKey('starships.id'), nullable=True)

    character = db.relationship("Characters")
    planet = db.relationship("Planets")
    starship = db.relationship("Starships")

    def __repr__(self):
        return f"{self.list_name}"

    def serialize(self):
        return {
            "list_name": self.list_name,
            "character": self.character.serialize() if self.character else None,
            "planet": self.planet.serialize() if self.planet else None,
            "starship": self.starship.serialize() if self.starship else None,
            "id": self.id
        }

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(80), unique=False, nullable=True)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True)
    favorites_id = db.Column(db.Integer, db.ForeignKey("favorites.id"))
    favorites = db.relationship(Favorites)
    
    def __repr__(self):
        return '<User %r>' % self.username
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username" : self.username,
            # do not serialize the password, its a security breach
        }