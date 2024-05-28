import json
from __init__ import app, db
from sqlalchemy.exc import IntegrityError

#This material was based on a template provided by our teacher.
class College(db.Model):
    __tablename__ = 'colleges'  # table name is plural, class name is singular
    
    
#NEW DATA COLUMNS - Tuition, student count, student-faculty ratio, safety score 

    # Define the Player schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=True, nullable=True)
    _link = db.Column(db.String(255), unique=False, nullable=True)
    _image = db.Column(db.String(255), unique=False, nullable=True)
    _tuition = db.Column(db.Integer, unique=False, nullable=True)
    _studentCount = db.Column(db.Integer, unique=False, nullable=True)
    _studentFaculty = db.Column(db.Integer, unique=False, nullable=True)
    _safetyscore = db.Column(db.Float, unique=False, nullable=True)
    _graduationrate = db.Column(db.Float, unique=False, nullable=True)

    def __init__(self, name, link, image, tuition, studentCount, studentFaculty, safetyScore, graduationrate):
        self._name = name    # variables with self prefix become part of the object, 
        self._link = link
        self._image = image
        self._tuition = tuition
        self._studentCount = studentCount
        self._studentFaculty = studentFaculty
        self._safetyscore = safetyScore
        self._graduationrate = graduationrate

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def link(self):
        return self._link
    
    @link.setter
    def link(self, link):
        self._link = link
        
    @property
    def image(self):
        return self._image
    
    @image.setter
    def image(self, image):
        self._image = image
    
    @property #tuition property
    def tuition(self): 
        return self._tuition
        
    @tuition.setter #tuition setter
    def tuition(self, tuition):
        self._tuition = tuition

    @property #studentCount property
    def studentCount(self): 
        return self._studentCount
        
    @studentCount.setter #studentCount setter
    def studentCount(self, studentCount):
        self._studentCount = studentCount
        
    @property #studentFaculty property
    def studentFaculty(self): 
        return self._studentFaculty
        
    @studentFaculty.setter #studentFaculty setter
    def studentFaculty(self, studentFaculty):
        self._studentFaculty = studentFaculty

    @property #score property
    def safetyScore(self): 
        return self._safetyscore
        
    @safetyScore.setter #score setter
    def safetyScore(self, safetyScore):
        self._safetyscore = safetyScore

    @property #graduation r8 property
    def graduationrate(self): 
        return self._graduationrate
        
    @safetyScore.setter #graduation r8 setter
    def graduationrate(self, graduationrate):
        self._graduationrate = graduationrate

    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a player object from Player(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "link": self.link,
            "image": self.image,
            "tuition": self.tuition,
            "studentCount": self.studentCount, 
            "studentFaculty": self.studentFaculty, 
            "safetyscore": self.safetyScore,
            "graduationrate": self.graduationrate
        }

    # CRUD update: updates name, uid, password, tokens
    # returns self
    def update(self, dictionary):
        """only updates values in dictionary with length"""
        for key in dictionary:
            if key == "name":
                self.name = dictionary[key]
            if key == "link":
                self.link = dictionary[key]
            if key == "image":
                self.image = dictionary[key]
            if key == "tuition":
                self.tuition = dictionary[key]
            if key == "studentCount":
                self.studentCount = dictionary[key]
            if key == "studentFaculty":
                self.studentFaculty = dictionary[key]
            if key == "safetyscore":
                self.safetyScore = dictionary[key]
            if key == "graduationrate":
                self.graduationrate = dictionary[key]
            
        db.session.commit()
        return self

    # return self
    def delete(self):
        colleges = self
        db.session.delete(self)
        db.session.commit()
        return colleges

"""Database Creation and Testing """
# Builds working data for testing
def initColleges():
    with app.app_context():
        db.create_all()
        c1 = College(name='Stanford University',link='https://admission.stanford.edu/apply/',image='https://identity.stanford.edu/wp-content/uploads/sites/3/2020/07/block-s-right.png', tuition=82162, studentCount=16914, studentFaculty=6, safetyScore=1.03, graduationrate=0.94)
        c2 = College(name='Harvard University',link='https://college.harvard.edu/admissions/apply',image='https://1000logos.net/wp-content/uploads/2017/02/Harvard-Logo.png', tuition=83538, studentCount=22947, studentFaculty=7, safetyScore=1.37, graduationrate=0.97)
        c3 = College(name='MIT',link='https://apply.mitadmissions.org/portal/apply',image='https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/MIT_logo.svg/2560px-MIT_logo.svg.png', tuition=79850, studentCount=11376, studentFaculty=3, safetyScore=0.92, graduationrate=0.95)
        c4 = College(name='Georgia Tech',link='https://admission.gatech.edu/apply/',image='https://brand.gatech.edu/sites/default/files/inline-images/GTVertical_RGB.png', tuition=28106, studentCount=45296, studentFaculty=22, safetyScore=1.65, graduationrate=0.9)
        c5 = College(name='Duke University',link='https://admissions.duke.edu/apply/',image='https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Duke_Blue_Devils_logo.svg/909px-Duke_Blue_Devils_logo.svg.png', tuition=62688, studentCount=18000, studentFaculty=6, safetyScore=1.28, graduationrate=0.95)
        c6 = College(name='Yale University',link='https://www.yale.edu/admissions',image='https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Yale_University_logo.svg/2560px-Yale_University_logo.svg.png', tuition=85120, studentCount=14776, studentFaculty=6, safetyScore=1.11, graduationrate=0.97)
        c7 = College(name='Princeton University',link='https://admission.princeton.edu/apply',image='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Princeton_seal.svg/1200px-Princeton_seal.svg.png', tuition=80415, studentCount=5590, studentFaculty=5, safetyScore=0.85, graduationrate=0.98)
        c8 = College(name='Columbia University',link='https://undergrad.admissions.columbia.edu/apply',image='https://admissions.ucr.edu/sites/default/files/styles/form_preview/public/2020-07/ucr-education-logo-columbia-university.png?itok=-0FD6Ma2', tuition=86097, studentCount=36650, studentFaculty=6, safetyScore=1.43, graduationrate=0.95)
        c9 = College(name='University of Chicago',link='https://collegeadmissions.uchicago.edu/apply',image='https://upload.wikimedia.org/wikipedia/commons/c/cd/University_of_Chicago_Coat_of_arms.png', tuition=86856, studentCount=14467, studentFaculty=5, safetyScore=1.57, graduationrate=0.95)
        c10 = College(name='UC Berkeley',link='https://admissions.berkeley.edu/apply-to-berkeley/',image='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Seal_of_University_of_California%2C_Berkeley.svg/1200px-Seal_of_University_of_California%2C_Berkeley.svg.png', tuition=43043, studentCount=45060, studentFaculty=19, safetyScore=1.34, graduationrate=0.93)
        c11 = College(name='UCLA',link='https://admission.ucla.edu/apply',image='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/UCLA_Bruins_primary_logo.svg/1200px-UCLA_Bruins_primary_logo.svg.png', tuition=36980, studentCount=65282, studentFaculty=19, safetyScore=1.16, graduationrate=0.92)
        c12 = College(name='Cornell University', link='https://admissions.cornell.edu/apply', image='https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Cornell_University_seal.svg/1200px-Cornell_University_seal.svg.png', tuition=80287, studentCount=23620, studentFaculty=9, safetyScore=1.5, graduationrate=0.93)
        c13 = College(name='University of Pennsylvania', link='https://admissions.upenn.edu/admissions-and-financial-aid', image='https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/UPenn_shield_with_banner.svg/1920px-UPenn_shield_with_banner.svg.png', tuition=85738, studentCount=22432, studentFaculty=6, safetyScore=1.2, graduationrate=0.95)
        c14 = College(name='California Institute of Technology (Caltech)', link='https://www.admissions.caltech.edu/apply', image='https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Seal_of_the_California_Institute_of_Technology.svg/1920px-Seal_of_the_California_Institute_of_Technology.svg.png', tuition=79947, studentCount=2240, studentFaculty=3, safetyScore=0.7, graduationrate=0.94)

        #Add new data to this line
        colleges = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14]
        """Builds sample user/note(s) data"""
        for college in colleges:
            try:
                '''add user to table'''
                object = college.create()
                print(f"Created new uid {object.id}")
            except:  # error raised if object nit created
                '''fails with bad or duplicate data'''
                print(f"Records exist uid {college.id}, or error.")