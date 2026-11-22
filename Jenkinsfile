
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
                echo 'Setting up Python environment'

                sh '''
                    python3 --version
                    python3 -m venv .venv
                    . .venv/bin/activate

                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running ShopSphere automated tests'

                sh '''
                    . .venv/bin/activate
                    pytest -v
                '''
            }
        }
    }

    post {
        success {
            echo 'ShopSphere CI Pipeline completed successfully!'
        }

        failure {
            echo 'ShopSphere CI Pipeline failed. Check the console output.'
        }
    }
}
