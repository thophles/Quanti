from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('', validators=[InputRequired()], render_kw={"placeholder": "e-mail"})
    password = PasswordField('', validators=[InputRequired()], render_kw={"placeholder": "password"})
    remember_me = BooleanField('Remember Me')
class RegistrationForm(FlaskForm):
    name = StringField('', validators=[InputRequired()], render_kw={"placeholder": "Name"})
    email = StringField('', validators=[InputRequired()], render_kw={"placeholder": "e-mail"})
    password = PasswordField('', validators=[InputRequired()], render_kw={"placeholder": "password"})
    departmentOne = SelectField(
            '',
            choices = [('Choose a Department', 'Choose a Department'), ('Academic Spine', 'Academic Spine'), ('AIADO', 'AIADO'),
            ('Arts Administration', 'Arts Administration'), ('Art Education', 'Art Education'), ('Art History, Theory, Criticism', 'Art History, Theory, Criticism'),
            ('Art & Technology', 'Art & Technology'), ('Art Therapy', 'Art Therapy'), ('Ceramics', 'Ceramics'), ('Contemporary Practices', 'Contemporary Practices'),
            ('Fashion Design', 'Fashion Design'), ('Fiber and Material Studies', 'Fiber and Material Studies'), ('Film, Video, New Media, and Animation', 'Film, Video, New Media, and Animation'), ('Historic Preservation', 'Historic Preservation'),
            ('Low Residency', 'Low Residency'), ('Liberal Arts', 'Liberal Arts'), ('New Arts Journalism', 'New Arts Journalism'), ('Painting and Drawing', 'Painting and Drawing'),
            ('Performance', 'Performance'), ('Photography', 'Photography'), ('Printmedia', 'Printmedia'), ('Sculpture', 'Sculpture'),
            ('Sound', 'Sound'), ('Visual Critique Studies', 'Visual Critique Studies'),
            ('Visual Communication Design', 'Visual Communication Design'), ('Writing', 'Writing')],
            validators = [InputRequired()])
    departmentTwo = SelectField(
            '',
            choices = [('Choose a Department', 'Choose a Department'), ('Academic Spine', 'Academic Spine'), ('AIADO', 'AIADO'),
            ('Arts Administration', 'Arts Administration'), ('Art Education', 'Art Education'), ('Art History, Theory, Criticism', 'Art History, Theory, Criticism'),
            ('Art & Technology', 'Art & Technology'), ('Art Therapy', 'Art Therapy'), ('Ceramics', 'Ceramics'), ('Contemporary Practices', 'Contemporary Practices'),
            ('Fashion Design', 'Fashion Design'), ('Fiber and Material Studies', 'Fiber and Material Studies'), ('Film, Video, New Media, and Animation', 'Film, Video, New Media, and Animation'), ('Historic Preservation', 'Historic Preservation'),
            ('Low Residency', 'Low Residency'), ('Liberal Arts', 'Liberal Arts'), ('New Arts Journalism', 'New Arts Journalism'), ('Painting and Drawing', 'Painting and Drawing'),
            ('Performance', 'Performance'), ('Photography', 'Photography'), ('Printmedia', 'Printmedia'), ('Sculpture', 'Sculpture'),
            ('Sound', 'Sound'), ('Visual Critique Studies', 'Visual Critique Studies'),
            ('Visual Communication Design', 'Visual Communication Design'), ('Writing', 'Writing')])
    Grade = SelectField('', choices=[(1, 'Freshman'),
    (2, 'Sophomore'), (3, 'Junior'),
    (4, 'Senior'), (5, 'First-Year Grad'),
    (6, 'Second-Year Grad')],
    coerce=int,
    validators = [InputRequired()])
