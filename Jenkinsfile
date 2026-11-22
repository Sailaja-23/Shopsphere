
pipeline {
    agent any

    environment {
        DATABASE_URL = 'sqlite://'
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out ShopSphere source code'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing application and testing dependencies'

                sh '''
                    python3 --version
                    python3 -m venv .venv
                    . .venv/bin/activate

                    python -m pip install --upgrade pip
                    pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Run Tests and Coverage') {
            steps {
                echo 'Running pytest and generating reports'

                sh '''
                    . .venv/bin/activate
                    mkdir -p reports

                    pytest -v \
                      --junitxml=reports/junit.xml \
                      --cov=app \
                      --cov-report=term-missing \
                      --cov-report=xml:reports/coverage.xml \
                      --cov-report=html:reports/htmlcov
                '''
            }
        }
    }

    post {
        always {
            echo 'Publishing test and coverage reports'

            junit testResults: 'reports/junit.xml',
                  allowEmptyResults: true

            archiveArtifacts artifacts: 'reports/**',
                             allowEmptyArchive: true
        }

        success {
            echo 'ShopSphere tests and coverage completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the test results and console output.'
        }
    }
}
