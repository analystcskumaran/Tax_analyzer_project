pipeline {
    agent any  // Runs on any available Jenkins agent
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/yourusername/tax-analyzer-project.git'  // Replace with your repo URL
            }
        }
        stage('Setup Environment') {
            steps {
                sh 'python3 -m venv venv'
                sh 'source venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'source venv/bin/activate && pytest --junitxml=results.xml'  // Runs tests and generates JUnit report
            }
            post {
                always {
                    junit 'results.xml'  // Publishes test results in Jenkins UI
                }
            }
        }
    }
    post {
        success {
            echo 'Tests passed! Ready for deployment.'
        }
        failure {
            echo 'Tests failed. Check logs.'
        }
    }
}