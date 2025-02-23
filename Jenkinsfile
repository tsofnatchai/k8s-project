pipeline {
    agent any
    environment {
        PRODUCER_IMAGE = 'tsofnatg/producer'
        CONSUMER_IMAGE = 'tsofnatg/consumer'
        REGISTRY_CREDENTIALS = 'docker-hub-credentials'
        HELM_RELEASE_NAME = "release"
        HELM_CHART_PATH = "./helm/my-app-chart"  // Adjusted path to the Helm chart
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
        stage('Deploy Producer Application') {
            steps {
                script {
                    bat "helm upgrade --install ${HELM_RELEASE_NAME}-producer ${HELM_CHART_PATH} --set image.repository=${PRODUCER_IMAGE} --values ${HELM_CHART_PATH}/values.yaml"
                }
            }
        }
        stage('Deploy Consumer Application') {
            steps {
                script {
                    bat "helm upgrade --install ${HELM_RELEASE_NAME}-consumer ${HELM_CHART_PATH} --set image.repository=${CONSUMER_IMAGE} --values ${HELM_CHART_PATH}/values.yaml"
                }
            }
        }
        stage('Clean Up Docker Images') {
            steps {
                bat 'docker image prune -f'  // Windows agent
            }
        }
    }
}
