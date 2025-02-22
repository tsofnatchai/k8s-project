pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/avielb/rmqp-example.git'
            }
        }
        stage('Build Producer & Consumer') {
            steps {
                sh 'docker build -t producer:latest producer/'
                sh 'docker build -t consumer:latest consumer/'
            }
        }
        stage('Push to Docker Registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-credentials-id', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
                    sh 'docker tag producer:latest my-docker-repo/producer:latest'
                    sh 'docker tag consumer:latest my-docker-repo/consumer:latest'
                    sh 'docker push my-docker-repo/producer:latest'
                    sh 'docker push my-docker-repo/consumer:latest'
                }
            }
        }
    }
}
