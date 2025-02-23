pipeline {
    agent any
    environment {
        PRODUCER_IMAGE = 'tsofnatchai/producer'
        CONSUMER_IMAGE = 'tsofnatchai/consumer'
        REGISTRY_CREDENTIALS = 'docker-hub-credentials'
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/tsofnatchai/k8s-project.git'
            }
        }
        stage('Build Producer Image') {
            steps {
                script {
                    docker.build("${PRODUCER_IMAGE}:latest", "./producer")
                }
            }
        }
        stage('Build Consumer Image') {
            steps {
                script {
                    docker.build("${CONSUMER_IMAGE}:latest", "./consumer")
                }
            }
        }
        stage('Push Producer Image') {
            steps {
                script {
                    docker.withRegistry('', REGISTRY_CREDENTIALS) {
                        docker.image("${PRODUCER_IMAGE}:latest").push()
                    }
                }
            }
        }
        stage('Push Consumer Image') {
            steps {
                script {
                    docker.withRegistry('', REGISTRY_CREDENTIALS) {
                        docker.image("${CONSUMER_IMAGE}:latest").push()
                    }
                }
            }
        }
        stage('Clean Up Docker Images') {
            steps {
                bat 'docker image prune -f'  // Windows agent
                // sh 'docker image prune -f'  // Linux/Mac agent
            }
        }
    }
//     post {
//         cleanup {
//             // Remove unused Docker images to free up space
//             //sh 'docker image prune -f'
//             bat 'docker image prune -f'
//         }
//     }
}
