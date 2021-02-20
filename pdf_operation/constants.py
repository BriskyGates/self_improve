import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(PROJECT_DIR, 'tests')
CASES_DIR = os.path.join(PROJECT_DIR, 'cases')
CASES_TRUE_DIR = os.path.join(CASES_DIR, 'true_case')
CASES_FALSE_DIR = os.path.join(CASES_DIR, 'false_case')
SEARCH_WORD = ['DRAFT', 'PROFORMA', 'PREADVICE']

if __name__ == '__main__':
    print(PROJECT_DIR)