"""
Comprehensive API Test Suite for MindCare Backend
Tests all endpoints: authentication, quizzes, videos, clinics, history
"""

import requests
import json
import uuid
from typing import Dict, Any
import time

BASE_URL = 'http://localhost:8000/api'

class APITester:
    """Test MindCare API endpoints"""
    
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_id = None
        self.test_results = []
    
    def log_result(self, test_name: str, passed: bool, details: str = ''):
        """Log test result"""
        self.test_results.append({
            'test': test_name,
            'passed': passed,
            'details': details
        })
        status = '✓ PASS' if passed else '✗ FAIL'
        print(f"{status}: {test_name} - {details}")
    
    def print_summary(self):
        """Print test summary"""
        passed = sum(1 for r in self.test_results if r['passed'])
        total = len(self.test_results)
        print(f"\n{'='*60}")
        print(f"Test Summary: {passed}/{total} passed")
        print(f"{'='*60}\n")
        
        failed_tests = [r for r in self.test_results if not r['passed']]
        if failed_tests:
            print("Failed Tests:")
            for test in failed_tests:
                print(f"  - {test['test']}: {test['details']}")
    
    # Authentication Tests
    
    def test_user_registration(self) -> bool:
        """Test user registration endpoint"""
        url = f"{BASE_URL}/users/auth/register/"
        
        user_data = {
            'username': f'testuser_{uuid.uuid4().hex[:8]}',
            'email': f'testuser_{uuid.uuid4().hex[:8]}@test.com',
            'password': 'TestPassword123!',
            'password2': 'TestPassword123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        try:
            response = self.session.post(url, json=user_data)
            
            if response.status_code == 201:
                data = response.json()
                self.token = data.get('token')
                self.user_id = data.get('user', {}).get('id')
                self.session.headers.update({'Authorization': f'Token {self.token}'})
                self.log_result('User Registration', True, f'Created user {user_data["email"]}')
                return True
            else:
                self.log_result('User Registration', False, f'Status {response.status_code}: {response.text}')
                return False
        except Exception as e:
            self.log_result('User Registration', False, str(e))
            return False
    
    def test_user_login(self, email: str, password: str) -> bool:
        """Test user login endpoint"""
        url = f"{BASE_URL}/users/auth/login/"
        
        login_data = {
            'email': email,
            'password': password
        }
        
        try:
            response = self.session.post(url, json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                self.session.headers.update({'Authorization': f'Token {self.token}'})
                self.log_result('User Login', True, f'Logged in {email}')
                return True
            else:
                self.log_result('User Login', False, f'Status {response.status_code}')
                return False
        except Exception as e:
            self.log_result('User Login', False, str(e))
            return False
    
    def test_get_profile(self) -> bool:
        """Test get user profile endpoint"""
        url = f"{BASE_URL}/users/auth/profile/"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                self.log_result('Get User Profile', True, 'Profile retrieved')
                return True
            else:
                self.log_result('Get User Profile', False, f'Status {response.status_code}')
                return False
        except Exception as e:
            self.log_result('Get User Profile', False, str(e))
            return False
    
    # Quiz Tests
    
    def test_list_quizzes(self) -> bool:
        """Test list quizzes endpoint"""
        url = f"{BASE_URL}/assessments/quizzes/"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                quiz_count = len(data) if isinstance(data, list) else data.get('count', 0)
                self.log_result('List Quizzes', True, f'Retrieved {quiz_count} quizzes')
                return True
            else:
                self.log_result('List Quizzes', False, f'Status {response.status_code}')
                return False
        except Exception as e:
            self.log_result('List Quizzes', False, str(e))
            return False
    
    def test_get_quiz_types(self) -> bool:
        """Test get quiz types endpoint"""
        url = f"{BASE_URL}/assessments/quizzes/types/"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                types = data.get('quiz_types', [])
                self.log_result('Get Quiz Types', True, f'Retrieved types: {types}')
                return True
            else:
                self.log_result('Get Quiz Types', False, f'Status {response.status_code}')
                return False
        except Exception as e:
            self.log_result('Get Quiz Types', False, str(e))
            return False
    
    def test_submit_quiz(self) -> bool:
        """Test submit quiz endpoint"""
        url = f"{BASE_URL}/assessments/quiz-results/submit/"
        
        # Create quiz response data (9 responses for PHQ-9)
        quiz_data = {
            'quiz_id': str(uuid.uuid4()),  # Using placeholder UUID
            'responses': [
                {'question_id': str(uuid.uuid4()), 'option_id': str(uuid.uuid4()), 'response_text': '1'} 
                for _ in range(9)
            ],
            'time_taken_seconds': 300,
            'device_type': 'WEB'
        }
        
        try:
            response = self.session.post(url, json=quiz_data)
            
            # Expect failure due to non-existent quiz, but endpoint should exist
            if response.status_code in [201, 400, 404]:
                self.log_result('Submit Quiz (Endpoint)', True, f'Endpoint exists (status {response.status_code})')
                return True
            else:
                self.log_result('Submit Quiz (Endpoint)', False, f'Unexpected status {response.status_code}')
                return False
        except Exception as e:
            self.log_result('Submit Quiz (Endpoint)', False, str(e))
            return False
    
    def test_get_quiz_results(self) -> bool:
        """Test get user's quiz results endpoint"""
        url = f"{BASE_URL}/assessments/quiz-results/my-results/"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                count = data.get('count', 0)
                self.log_result('Get Quiz Results', True, f'Retrieved {count} results')
                return True
            else:
                self.log_result('Get Quiz Results', False, f'Status {response.status_code}')
                return False
        except Exception as e:
            self.log_result('Get Quiz Results', False, str(e))
            return False
    
    # Video Tests
    
    def test_video_endpoints_exist(self) -> bool:
        """Test video upload endpoint exists"""
        url = f"{BASE_URL}/assessments/videos/upload/"
        
        try:
            # Just check if endpoint exists (POST without video will fail gracefully)
            response = self.session.post(url)
            
            if response.status_code in [400, 415, 201, 422]:  # Any response means endpoint exists
                self.log_result('Video Upload Endpoint', True, 'Endpoint exists')
                return True
            else:
                self.log_result('Video Upload Endpoint', False, f'Unexpected status {response.status_code}')
                return False
        except Exception as e:
            self.log_result('Video Upload Endpoint', False, str(e))
            return False
    
    def test_get_video_analyses(self) -> bool:
        """Test get user's video analyses endpoint"""
        url = f"{BASE_URL}/assessments/videos/my-analyses/"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                count = data.get('count', 0)
                self.log_result('Get Video Analyses', True, f'Retrieved {count} analyses')
                return True
            else:
                self.log_result('Get Video Analyses', False, f'Status {response.status_code}')
                return False
        except Exception as e:
            self.log_result('Get Video Analyses', False, str(e))
            return False
    
    # Health Profile Tests
    
    def test_get_health_profile(self) -> bool:
        """Test get health profile endpoint"""
        url = f"{BASE_URL}/users/health-profile/"
        
        try:
            response = self.session.get(url)
            
            if response.status_code in [200, 404]:  # OK or not found
                self.log_result('Get Health Profile', True, f'Status {response.status_code}')
                return True
            else:
                self.log_result('Get Health Profile', False, f'Status {response.status_code}')
                return False
        except Exception as e:
            self.log_result('Get Health Profile', False, str(e))
            return False
    
    # Journal Tests
    
    def test_get_journal_entries(self) -> bool:
        """Test get journal entries endpoint"""
        url = f"{BASE_URL}/users/journal/"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                count = data.get('count', 0)
                self.log_result('Get Journal Entries', True, f'Retrieved {count} entries')
                return True
            else:
                self.log_result('Get Journal Entries', False, f'Status {response.status_code}')
                return False
        except Exception as e:
            self.log_result('Get Journal Entries', False, str(e))
            return False
    
    # Assessment History Tests
    
    def test_get_assessment_history(self) -> bool:
        """Test get assessment history endpoint"""
        url = f"{BASE_URL}/assessments/history/my-history/"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                count = data.get('count', 0)
                self.log_result('Get Assessment History', True, f'Retrieved {count} records')
                return True
            else:
                self.log_result('Get Assessment History', False, f'Status {response.status_code}')
                return False
        except Exception as e:
            self.log_result('Get Assessment History', False, str(e))
            return False
    
    def test_get_assessment_summary(self) -> bool:
        """Test get assessment summary endpoint"""
        url = f"{BASE_URL}/assessments/history/summary/"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                total = data.get('total_assessments', 0)
                self.log_result('Get Assessment Summary', True, f'Total assessments: {total}')
                return True
            else:
                self.log_result('Get Assessment Summary', False, f'Status {response.status_code}')
                return False
        except Exception as e:
            self.log_result('Get Assessment Summary', False, str(e))
            return False
    
    # Clinic Tests
    
    def test_list_clinics(self) -> bool:
        """Test list clinics endpoint"""
        url = f"{BASE_URL}/clinics/clinics/"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                clinic_count = len(data) if isinstance(data, list) else 0
                self.log_result('List Clinics', True, f'Retrieved {clinic_count} clinics')
                return True
            else:
                self.log_result('List Clinics', False, f'Status {response.status_code}')
                return False
        except Exception as e:
            self.log_result('List Clinics', False, str(e))
            return False
    
    def test_get_clinic_cities(self) -> bool:
        """Test get clinic cities endpoint"""
        url = f"{BASE_URL}/clinics/clinics/cities/"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                cities = data.get('cities', [])
                self.log_result('Get Clinic Cities', True, f'Retrieved {len(cities)} cities')
                return True
            else:
                self.log_result('Get Clinic Cities', False, f'Status {response.status_code}')
                return False
        except Exception as e:
            self.log_result('Get Clinic Cities', False, str(e))
            return False
    
    def test_nearest_clinics(self) -> bool:
        """Test nearest clinics endpoint"""
        url = f"{BASE_URL}/clinics/recommendations/nearest/"
        
        params = {
            'latitude': 40.7128,
            'longitude': -74.0060,
            'radius': 50
        }
        
        try:
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                clinic_count = len(data) if isinstance(data, list) else 0
                self.log_result('Get Nearest Clinics', True, f'Retrieved {clinic_count} nearest clinics')
                return True
            else:
                self.log_result('Get Nearest Clinics', False, f'Status {response.status_code}')
                return False
        except Exception as e:
            self.log_result('Get Nearest Clinics', False, str(e))
            return False
    
    # Run All Tests
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("\n" + "="*60)
        print("MindCare API Test Suite")
        print("="*60 + "\n")
        
        # Authentication Tests
        print(">> Authentication Tests")
        self.test_user_registration()
        if self.token:  # Only proceed if registration successful
            self.test_get_profile()
        
        # Quiz Tests
        print("\n>> Quiz Tests")
        self.test_list_quizzes()
        self.test_get_quiz_types()
        self.test_submit_quiz()
        self.test_get_quiz_results()
        
        # Video Tests
        print("\n>> Video Tests")
        self.test_video_endpoints_exist()
        self.test_get_video_analyses()
        
        # Health & Journal Tests
        print("\n>> User Profile Tests")
        self.test_get_health_profile()
        self.test_get_journal_entries()
        
        # Assessment Tests
        print("\n>> Assessment History Tests")
        self.test_get_assessment_history()
        self.test_get_assessment_summary()
        
        # Clinic Tests
        print("\n>> Clinic Tests")
        self.test_list_clinics()
        self.test_get_clinic_cities()
        self.test_nearest_clinics()
        
        # Print summary
        self.print_summary()


if __name__ == '__main__':
    tester = APITester()
    tester.run_all_tests()
