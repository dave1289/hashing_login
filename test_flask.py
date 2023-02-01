from unittest import TestCase

from app import app
from models import db, User, Tweet

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_hash_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class HashBashTestCase(TestCase):

    def setUp(self):

        Tweet.query.delete()

        test_tweet = Tweet(user_id="1", comment='test')
        db.session.add(test_tweet)
        db.session.commit()

        self.id = tweet.id
        self.pet_id = pet.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_home(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('HASHBASH', html)

    def test_show_bashes(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.pet_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('BASH IT', html)

    def test_add_pet(self):
        with app.test_client() as client:
            test_tweet = Tweet(user_id='1', comment='test')
            resp = client.post("/", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test", html)