pipeline {
    agent any
    environment {
        KUBECONFIG = "C:\\Users\\TsofnatChai\\.kube\\config" // Update the correct kubeconfig path on Windows
        PRODUCER_IMAGE = 'tsofnatg/producer'
        CONSUMER_IMAGE = 'tsofnatg/consumer'
        REGISTRY_CREDENTIALS = 'docker-hub-credentials'
        HELM_RELEASE_NAME_PRODUCER = "release-producer"   // Unique release name for producer
        HELM_RELEASE_NAME_CONSUMER = "release-consumer"   // Unique release name for consumer
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
        stage('Configure Kubernetes Access') {
            steps {
                script {
                    bat "kubectl config view"  // Verify Kube config
                    bat "kubectl get nodes"    // Verify connection to cluster
                }
            }
        }
        stage('Clean Up ConfigMap') {
            steps {
                script {
                    // Delete the existing rabbitmq-config before deploying the consumer
                    bat "kubectl delete configmap rabbitmq-config --ignore-not-found"
                }
            }
        }
        stage('Clean Up Secret') {
            steps {
                script {
                    // Delete the existing rabbitmq-secret before deploying the consumer
                    bat "kubectl delete secret rabbitmq-secret --ignore-not-found"
                }
            }
        }
        stage('Uninstall Old Producer Release') {
            steps {
                script {
                    bat "helm uninstall release-producer --namespace default --ignore-not-found"
                }
            }
        }
        stage('Uninstall Old Consumer Release') {
            steps {
                script {
                    bat "helm uninstall release-consumer --namespace default --ignore-not-found"
                }
            }
        }
        stage('Deploy Producer Application') {
            steps {
                script {
                    bat "helm upgrade --install ${HELM_RELEASE_NAME_PRODUCER} ${HELM_CHART_PATH} --set image.repository=${PRODUCER_IMAGE} --set image.tag=latest --values ${HELM_CHART_PATH}/values.yaml"
                }
            }
        }
        stage('Deploy Consumer Application') {
            steps {
                script {
                    bat "helm upgrade --install ${HELM_RELEASE_NAME_CONSUMER} ${HELM_CHART_PATH} --set image.repository=${CONSUMER_IMAGE} --set image.tag=latest --values ${HELM_CHART_PATH}/values.yaml"
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
