pipeline {
    agent any

    options {
    timestamps()
    timeout(time: 20, unit: 'MINUTES')
    disableConcurrentBuilds()
    }

    environment {
        DATABASE_URL = 'sqlite://'
        PIP_DISABLE_PIP_VERSION_CHECK = '1'
        IMAGE_NAME = 'shopsphere'
        IMAGE_TAG = '1.0'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
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

                    docker images ${IMAGE_NAME}
                '''
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                withCredentials([
                    file(
                        credentialsId: 'shopsphere-env',
                        variable: 'ENV_FILE'
                    )
                ]) {
                    sh '''
                        set +x
                        set -e

                        echo "Preparing secure environment file"

                        cp "$ENV_FILE" .env.docker
                        chmod 600 .env.docker

                        trap 'rm -f .env.docker' EXIT

                        echo "Validating Docker Compose configuration"

                        docker compose -p shopsphere config --quiet

                        echo "Deploying ShopSphere"

                        docker compose -p shopsphere up -d --no-build

                        echo "Checking deployment status"

                        docker compose -p shopsphere ps

                        echo "Waiting for API health"

                        attempt=1

                        while [ "$attempt" -le 30 ]; do
                            if curl -fsS http://127.0.0.1:8000/docs -o /dev/null; then
                               echo "ShopSphere API is responding successfully"
                               break
                            fi

                            echo "API not ready yet. Attempt $attempt/30"
                            attempt=$((attempt + 1))
                            sleep 5
                        done

                        if [ "$attempt" -gt 30 ]; then
                            echo "ShopSphere API failed to become ready"
                            docker compose -p shopsphere logs --tail=80 app
                            exit 1
                        fi

                        echo "ShopSphere deployment successful"
                    '''
                }
            }
        }
    }

    post {
        always {
            junit(
                testResults: 'reports/junit.xml',
                allowEmptyResults: true
            )

            archiveArtifacts(
                artifacts: 'reports/**',
                allowEmptyArchive: true
            )

            echo 'ShopSphere pipeline execution completed.'
        }

        success {
            echo 'ShopSphere CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'ShopSphere CI/CD pipeline failed.'

            sh '''
                echo "Collecting deployment diagnostics..."
                docker compose -p shopsphere ps || true
                docker compose -p shopsphere logs --tail=50 app || true
            '''
        }
    }
}
