from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Person, OfficeLocation, OrgGroup
import random


class Command(BaseCommand):
    args = '<number_of_users>'
    help = 'Creates random users for local testing'

    def handle(self, *args, **options):
        last_names = [
            'Sherman', 'Maddox', 'Montgomery', 'Small', 'Larsen', 'Marsh', 'Gardner', 'White', 'Gill', 'Pennington', 'Stein', 'Kirby', 'Jennings', 'French', 'Glass', 'Velasquez', 'Doyle', 'York', 'Fisher', 'Strong', 'Henson', 'Harmon', 'Higgins', 'James', 'Hancock', 'Drake', 'Eaton', 'Gordon', 'Harrington', 'Blevins', 'Avila', 'Solis', 'Richmond', 'Stark', 'Haynes', 'Durham', 'Montoya', 'Barrett', 'Chase', 'Mckay', 'Little', 'Perry', 'Howard', 'Caldwell', 'West', 'Fox', 'Long', 'Wright', 'Foster', 'Sloan', 'Frazier', 'Lowe', 'Cabrera', 'Barron', 'Ayala', 'Frank', 'Hammond', 'Orr', 'Holloway', 'King', 'Rush', 'Wiley', 'Neal', 'Davis', 'Fulton', 'Webb', 'Sanchez', 'Strickland', 'Clark', 'Middleton', 'Moody', 'Owens', 'Graham', 'Cotton', 'Shaffer', 'Hawkins',
            'Cooper', 'Justice', 'Clarke', 'Mcconnell', 'Mccarthy', 'Macdonald', 'Castillo', 'Gilbert', 'Horton', 'Finley', 'Beard', 'Sanders', 'Levy', 'Richard', 'Bowen', 'Grant', 'Wilkins', 'Ramsey', 'Lynch', 'Koch', 'Mercado', 'Roach', 'Bond', 'Lane', 'Tanner', 'Byers', 'Humphrey', 'Austin', 'Carney', 'Golden', 'Pope', 'Kramer', 'Ellison', 'Jefferson', 'Duffy', 'Gross', 'Mcmahon', 'Hudson', 'Mckee', 'Atkinson', 'Bush', 'Thompson', 'Faulkner', 'Christian', 'Ingram', 'Cannon', 'Gay', 'Nieves', 'Hodges', 'Langley', 'Watson', 'Woods', 'Gallagher', 'Delacruz', 'Stafford', 'Knight', 'Kerr', 'Chapman', 'Roman', 'Christensen', 'Robles', 'Mathews', 'Waller', 'Buckley', 'Myers', 'Powers', 'Lindsay', 'Gates', 'Miller', 'Johns', 'Morin', 'Fleming', 'Bishop', 'Clements']
        first_names = [
            'Sarah', 'Ian', 'Upton', 'Uriah', 'Hayden', 'Zia', 'Lila', 'Benjamin', 'Addison', 'Vivian', 'Kirby', 'Oscar', 'Demetrius', 'Hashim', 'Michelle', 'Odessa', 'Phillip', 'Michael', 'Dante', 'Omar', 'Dominic', 'Wing', 'Joshua', 'Charlotte', 'Thomas', 'Aquila', 'Rana', 'Jolene', 'Felix', 'Cailin', 'Tatiana', 'Oprah', 'Belle', 'Sydnee', 'Kuame', 'Fleur', 'Matthew', 'Sylvia', 'Mary', 'Deborah', 'Ross', 'Hyacinth', 'Jacqueline', 'Jessica', 'Callie', 'Ariana', 'Leo', 'Desiree', 'Lunea', 'Chava', 'Jorden', 'Rudyard', 'Cally', 'Knox', 'Arthur', 'Dana', 'Rebekah', 'Yen', 'Hadassah', 'Duncan', 'Ginger', 'Valentine', 'Ivana', 'Iona', 'Jemima', 'Dorothy', 'Joan', 'Timothy', 'Amity', 'Uriel', 'Skyler', 'Phelan', 'Alma', 'Hadley',
            'Quemby', 'Sonya', 'Axel', 'Slade', 'Riley', 'Rajah', 'Giselle', 'Selma', 'Nadine', 'Pascale', 'Carol', 'Steel', 'Lane', 'Emi', 'Trevor', 'Wyatt', 'Claire', 'Harlan', 'Liberty', 'Alexandra', 'Avram', 'Barbara', 'Rashad', 'Holmes', 'Kenneth', 'Preston', 'Patience', 'Adele', 'Alfonso', 'Harrison', 'Julian', 'Jena', 'Peter', 'Kessie', 'Katell', 'Denton', 'Piper', 'Jerry', 'Teegan', 'Chandler', 'Walter', 'Cheryl', 'Desirae', 'Tasha', 'Hunter', 'Logan', 'Tatyana', 'Gail', 'Galvin', 'Dara', 'Athena', 'Kay', 'Dustin', 'Faith', 'Mariam', 'Leroy', 'Edan', 'Alexis', 'Nissim', 'Octavia', 'Kareem', 'Heidi', 'Aspen', 'Gregory', 'Garrison', 'Jolie', 'Gloria', 'Alec', 'Asher', 'Julie', 'Ayanna', 'Gavin', 'Germane', 'Bertha', 'Quinn', 'Tarik']

        office_location = OfficeLocation.objects.get(pk='DC123')

        for x in xrange(int(args[0])):
            while True:
                first_name = first_names[int(random.random() *
                                             len(first_names))]
                last_name = last_names[int(random.random() * len(last_names))]
                username = last_name + first_name[0]
                email = username + '@exmaple.com'
                if not get_user_model().objects.filter(username=email).exists():
                    break

            user_attr = {
                'first_name': first_name,
                'last_name': last_name,
                'is_active': True,
                'is_superuser': False,
                'date_joined': '2012-03-01T16:03:14Z',
                'password': 'pbkdf2_sha256$10000$ggAKkiHobFL8$xQzwPeHNX1vWr9uNmZ/gKbd17uLGZVM8QNcgmaIEAUs=',
                'is_staff': True,
                'email': email,
                'username': email
            }

            userModel = get_user_model()
            user = userModel(**user_attr)
            user.save()

            person_attr = {
                'office_location': office_location,
                'allow_tagging': True,
                'photo_file': 'avatars/default.jpg',
                'stub': username.replace('.', ''),
                'office_phone': '5555555555',
                'user': user,
                'email_notifications': False,
                'org_group': OrgGroup.objects.order_by('?')[0]
            }

            person = Person(**person_attr)
            person.save()

        self.stdout.write(
            'Successfully created %d users and persons' % int(args[0]))
