import unittest
import random

class SecurityAnalyst:

    def calculate_department_score(self, threat_scores, importance):
        if not threat_scores:
            return 0  # No users, no threat
        average_score = sum(threat_scores) / len(threat_scores)
        weighted_score = average_score * importance
        return weighted_score

    def calculate_company_score(self, departments):
        total_weighted_score = 0
        total_importance = 0
        for department in departments:
            score = self.calculate_department_score(department['threat_scores'], department['importance'])
            total_weighted_score += score
            total_importance += department['importance']
        
        return (total_weighted_score / total_importance) if total_importance > 0 else 0


class TestSecurityAnalyst(unittest.TestCase):

    def setUp(self):
        self.analyst = SecurityAnalyst()

    def generate_random_data(self, mean, variance, size, min_score=0, max_score=90):
        return [min(max(int(random.gauss(mean, variance)), min_score), max_score) for _ in range(size)]

    def test_department_score_calculation(self):
        # Test with known threat scores and importance tag
        threat_scores = [10, 20, 30]
        importance = 3
        expected_score = sum(threat_scores) / len(threat_scores) * importance
        self.assertEqual(self.analyst.calculate_department_score(threat_scores, importance), expected_score)

    def test_empty_department(self):
        # Test department with no users
        self.assertEqual(self.analyst.calculate_department_score([], 3), 0)

    def test_company_score_with_equal_importance(self):
        # All departments have equal importance and similar average threat scores
        departments = [
            {'threat_scores': [10, 20, 30], 'importance': 2},
            {'threat_scores': [15, 25, 35], 'importance': 2},
            {'threat_scores': [20, 30, 40], 'importance': 2}
        ]
        avg_score = sum([10, 20, 30, 15, 25, 35, 20, 30, 40]) / 9
        self.assertAlmostEqual(self.analyst.calculate_company_score(departments), avg_score, places=2)

    def test_company_score_with_high_importance_department(self):
        # One department has much higher importance, so its threat score should dominate
        departments = [
            {'threat_scores': [10, 20, 30], 'importance': 1},
            {'threat_scores': [80, 85, 90], 'importance': 5}
        ]
        high_importance_weighted = sum([80, 85, 90]) / 3 * 5
        low_importance_weighted = sum([10, 20, 30]) / 3 * 1
        total_importance = 1 + 5
        expected_score = (high_importance_weighted + low_importance_weighted) / total_importance
        self.assertAlmostEqual(self.analyst.calculate_company_score(departments), expected_score, places=2)

    def test_all_zero_threat_scores(self):
        # All users have zero threat scores
        departments = [
            {'threat_scores': [0, 0, 0], 'importance': 3},
            {'threat_scores': [0, 0, 0], 'importance': 2}
        ]
        self.assertEqual(self.analyst.calculate_company_score(departments), 0)

    def test_varying_department_sizes(self):
        # Departments with varying numbers of users and threat levels
        departments = [
            {'threat_scores': self.generate_random_data(10, 5, 10), 'importance': 2},
            {'threat_scores': self.generate_random_data(20, 10, 100), 'importance': 3},
            {'threat_scores': self.generate_random_data(30, 15, 200), 'importance': 4}
        ]
        # No expected score, just verify it calculates without error
        self.assertTrue(0 <= self.analyst.calculate_company_score(departments) <= 90)

    def test_outliers_in_department_scores(self):
        # One department has an extremely high average due to outliers
        departments = [
            {'threat_scores': [10, 20, 15], 'importance': 2},
            {'threat_scores': [90, 90, 90], 'importance': 1}  # Outlier-heavy department
        ]
        weighted_score1 = (10 + 20 + 15) / 3 * 2
        weighted_score2 = (90 + 90 + 90) / 3 * 1
        total_importance = 2 + 1
        expected_score = (weighted_score1 + weighted_score2) / total_importance
        self.assertAlmostEqual(self.analyst.calculate_company_score(departments), expected_score, places=2)

if __name__ == '__main__':
    unittest.main()
