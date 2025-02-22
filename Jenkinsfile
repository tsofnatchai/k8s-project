pipeline {
    agent any

    environment {
        REGISTRY = 'tsofnatg'
        IMAGE_PRODUCER = 'producer'
        IMAGE_CONSUMER = 'consumer'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/avielb/rmqp-example.git', branch: 'main'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    sh "docker build -t ${REGISTRY}/${IMAGE_PRODUCER}:latest -f producer/Dockerfile ."
                    sh "docker build -t ${REGISTRY}/${IMAGE_CONSUMER}:latest -f consumer/Dockerfile ."
                }
            }
        }

        stage('Login to Docker Registry') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'docker-hub-credentials', variable: 'DOCKER_PASS')]) {
                        sh "echo $DOCKER_PASS | docker login -u ${REGISTRY} --password-stdin"
                    }
                }
            }
        }

        stage('Push Images to Registry') {
            steps {
                script {
                    sh "docker push ${REGISTRY}/${IMAGE_PRODUCER}:latest"
                    sh "docker push ${REGISTRY}/${IMAGE_CONSUMER}:latest"
                }
            }
        }
    }
}
