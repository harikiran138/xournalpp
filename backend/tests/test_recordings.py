import unittest
import json
import sys
import os

# Add backend directory to path so we can import app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import Recording

class TestRecordingsAPI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_recording(self):
        payload = {
            "title": "Test Recording",
            "metadata": {"duration": 120}
        }
        response = self.client.post('/api/recordings/', 
                                  data=json.dumps(payload),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], "Test Recording")
        self.assertIn('id', data)

    def test_list_recordings(self):
        # Create a recording first
        self.client.post('/api/recordings/', 
                        data=json.dumps({"title": "Rec 1"}),
                        content_type='application/json')
        
        response = self.client.get('/api/recordings/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], "Rec 1")

    def test_update_recording(self):
        # Create
        create_resp = self.client.post('/api/recordings/', 
                                     data=json.dumps({"title": "Original"}),
                                     content_type='application/json')
        rec_id = json.loads(create_resp.data)['id']
        
        # Update
        response = self.client.patch(f'/api/recordings/{rec_id}',
                                   data=json.dumps({"title": "Updated"}),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], "Updated")

if __name__ == '__main__':
    unittest.main()
