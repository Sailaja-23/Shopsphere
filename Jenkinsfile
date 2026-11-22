pipeline {
    agent any

    environment {
        DATABASE_URL = 'sqlite://'
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
        IMAGE_NAME = 'shopsphere'
        IMAGE_TAG = '1.0'
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
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements-dev.txt
                '''
            }
        }

        stage('Run Tests and Coverage') {
            steps {
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

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Building ShopSphere Docker image"

                    docker build \
                      -t ${IMAGE_NAME}:${IMAGE_TAG} \
                      -t ${IMAGE_NAME}:build-${BUILD_NUMBER} .

                    docker images shopsphere
                '''
            }
        }
        stage('Deploy with Docker Compose') {
            steps {
                sh '''
                    echo "Deploying ShopSphere"
                    docker compose -p shopsphere up -d --no-build

                    echo "Checking container status"
                    docker compose -p shopsphere ps

                    echo "Waiting for API"
                    curl --fail --retry 10 --retry-delay 5 --retry-connrefused http://127.0.0.1:8000/docs

                    echo "ShopSphere deployment successful"
               '''
            }
        }
    }
      

    post {
        always {
            junit testResults: 'reports/junit.xml',
                  allowEmptyResults: true

            archiveArtifacts artifacts: 'reports/**',
                             allowEmptyArchive: true
        }

        success {
            echo 'ShopSphere CI and Docker image build completed!'
        }

        failure {
            echo 'Pipeline failed. Check the console output.'
        }
    }
}

