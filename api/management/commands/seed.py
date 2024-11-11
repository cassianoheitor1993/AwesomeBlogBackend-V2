from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from api.models import Category, Article, Comment, Image
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.core.files.base import ContentFile
import random
from api.models import Category
import requests

class Command(BaseCommand):
    help = 'Seeds the database'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # erase tables
        Comment.objects.all().delete()
        Image.objects.all().delete()
        Article.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()

        # Seed Categories
        categories = []
        for category in ['Technology', 'Business', 'Science', 'Health', 'Lifestyle']:
            categories.append(Category.objects.create(name=category))

        # Seed Users
        users = []
        for _ in range(5):
            user = User.objects.create_user(username=fake.unique.user_name(), password='password')
            users.append(user)

        # Create Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='cassianomedeiros',
                email='cassiano.medeiros.93@gmail.com',
                password='admin'
            )
    

        # Seed Articles
        articles_data = [
            (1, "High himself major own guess.", "Anyone audience seven cultural instead program professional. Federal east than art large necessary.", timezone.now(), timezone.now(), 4, 1),
            (2, "Meet such national source trade blood.", "System expert gun because factor science. Boy reduce phone lead yard teach. These most cold suggest rest. Themselves success ready. Risk animal product interest long read.", timezone.now(), timezone.now(), 2, 1),
            (3, "Year again development wrong world.", "War significant yet senior common. Respond nor begin few. Since others drop improve range. Establish late station cold force power.", timezone.now(), timezone.now(), 1, 1),
            (4, "Education economy theory above leave late effort central.", "Father large decade various red billion someone. Building less make movement. Air sort increase wrong different table nothing everybody. Clearly lot later land pretty American.", timezone.now(), timezone.now(), 2, 1),
            (5, "Small head cultural admit charge car note Democrat.", "Fall old whether heart. Them product candidate trial sport go number. Majority improve the safe check. Just early cell professor.", timezone.now(), timezone.now(), 1, 1),
            (6, "Exploring the Power of Technology", "An in-depth look at how technology shapes modern life.", timezone.now(), timezone.now(), 1, 1),
            (7, "The Future of Data Science", "Data science is changing how businesses make decisions.", timezone.now(), timezone.now(), 2, 2),
            (8, "Top Trends in Software Development", "What to expect in the next wave of software development.", timezone.now(), timezone.now(), 3, 3),
            (9, "The Rise of AI", "Artificial Intelligence continues to evolve rapidly.", timezone.now(), timezone.now(), 4, 4),
            (10, "Creating a Better Future with Renewable Energy", "Renewable energy is paving the way for sustainable solutions.", timezone.now(), timezone.now(), 5, 5),
            (11, "Understanding Machine Learning", "An introduction to the basics of machine learning and its applications.", timezone.now(), timezone.now(), 1, 1),
            (12, "Digital Marketing in the Modern World", "How digital marketing is reshaping business strategies.", timezone.now(), timezone.now(), 2, 2),
            (13, "Cybersecurity Basics", "Steps to protect your information in an online world.", timezone.now(), timezone.now(), 3, 3),
            (14, "Building Resilient Infrastructure", "How to build systems that can withstand challenges.", timezone.now(), timezone.now(), 4, 4),
            (15, "The Importance of Clean Code", "Clean code practices for efficient software development.", timezone.now(), timezone.now(), 5, 5),
            (16, "Remote Work and Productivity", "Exploring productivity strategies for remote teams.", timezone.now(), timezone.now(), 1, 1),
            (17, "Introduction to Cloud Computing", "The basics of cloud computing and how it benefits businesses.", timezone.now(), timezone.now(), 2, 2),
            (18, "Mastering the Art of Networking", "Effective strategies for building a professional network.", timezone.now(), timezone.now(), 3, 3),
            (19, "Ethical Implications of AI", "Considering the ethical aspects of Artificial Intelligence.", timezone.now(), timezone.now(), 4, 4),
            (20, "Data Privacy and You", "An overview of data privacy and how to protect personal data.", timezone.now(), timezone.now(), 5, 5),
            (21, "The Evolution of Web Development", "A look at how web development has changed over the years and what the future holds.", timezone.now(), timezone.now(), 1, 1),
            (22, "The Impact of Blockchain Technology", "Understanding how blockchain is transforming industries beyond cryptocurrency.", timezone.now(), timezone.now(), 2, 1),
            (23, "Navigating the Gig Economy", "Strategies for success in an increasingly freelance-oriented job market.", timezone.now(), timezone.now(), 3, 2),
            (24, "Trends in Mobile App Development", "Exploring the latest trends and technologies in mobile app development.", timezone.now(), timezone.now(), 4, 2),
            (25, "The Role of Big Data in Business", "How big data analytics is driving business decisions.", timezone.now(), timezone.now(), 1, 3),
            (26, "Advancements in Robotics", "A closer look at the innovations in robotics and their implications.", timezone.now(), timezone.now(), 2, 3),
            (27, "Sustainable Business Practices", "How businesses can implement sustainable practices for better impact.", timezone.now(), timezone.now(), 3, 4),
            (28, "The Future of E-commerce", "Exploring trends and technologies shaping the e-commerce landscape.", timezone.now(), timezone.now(), 4, 4),
            (29, "Artificial Intelligence in Healthcare", "The potential of AI to transform healthcare delivery and outcomes.", timezone.now(), timezone.now(), 1, 5),
            (30, "Introduction to Agile Methodologies", "Understanding the principles of Agile and its benefits for project management.", timezone.now(), timezone.now(), 2, 5),
            (31, "Virtual Reality in Education", "How VR is changing the way we learn and teach.", timezone.now(), timezone.now(), 3, 1),
            (32, "Navigating the Cybersecurity Landscape", "Understanding the current challenges and solutions in cybersecurity.", timezone.now(), timezone.now(), 4, 2),
            (33, "The Importance of User Experience Design", "Why UX design is critical for successful digital products.", timezone.now(), timezone.now(), 1, 3),
            (34, "Smart Cities: The Future of Urban Living", "Exploring how technology is reshaping urban environments.", timezone.now(), timezone.now(), 2, 4),
            (35, "Understanding Natural Language Processing", "An introduction to NLP and its applications in various industries.", timezone.now(), timezone.now(), 3, 5),
        ]

        for _, title, body, _, _, category_index, author in articles_data:
            Article.objects.create(
                title=title,
                body=body,
                created_at=timezone.now(),
                updated_at=timezone.now(),
                category=categories[category_index-1],
                author=users[author-1]
            )

        
        # Seed Images
        # List of image paths
        image_paths = [
            'images/andrew-neel-rndjGfyInvs-unsplash.jpg',
            'images/andrew-neel-st-_pIZEvKM-unsplash.jpg',
            'images/arisa-chattasa-EHD-ODi1TjM-unsplash.jpg',
            'images/chu-gummies-oVEf8q8t_To-unsplash.jpg',
            'images/devin-justesen-49YPssjmBMM-unsplash.jpg',
            'images/hansjorg-rath-2i5d6UcJE3s-unsplash.jpg',
            'images/hansjorg-rath-ZkLHSmh_828-unsplash.jpg',
            'images/jess-bailey-iMjLgjFms7E-unsplash.jpg',
            'images/pau-casals-9ZrZU-GrIiw-unsplash.jpg',
            'images/s-b-vonlanthen-D75_5tWZDQ4-unsplash.jpg',
            'images/anete-lusina-GOZxrAlNIt4-unsplash.jpg',
        ]

        # assign images to articles
        for article in Article.objects.all():
            num_images = random.randint(1, 5)
            selected_images = random.sample(image_paths, num_images)
            for image_path in selected_images:
                Image.objects.create(
                    article=article,
                    image=image_path
                )

        # Seed Comments
        for article in Article.objects.all():
            for _ in range(3):
                Comment.objects.create(
                    article=article,
                    author=User.objects.order_by('?').first(),
                    body=fake.paragraph(),
                    created_at=timezone.now()
                )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully'))