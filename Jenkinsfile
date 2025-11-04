pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds' // ID delle credenziali in Jenkins
        DOCKERHUB_USERNAME = '<TUO_USERNAME_DOCKERHUB>' // sostituire con il tuo username
        IMAGE_NAME = "${DOCKERHUB_USERNAME}/flask-app-example"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set Image Tag') {
            steps {
                script {
                    if (env.GIT_TAG_NAME) {
                        // Se buildata da un tag git
                        env.IMAGE_TAG = env.GIT_TAG_NAME
                    } else if (env.BRANCH_NAME == 'master') {
                        env.IMAGE_TAG = 'latest'
                    } else if (env.BRANCH_NAME == 'develop') {
                        // usa i primi 7 caratteri dello SHA del commit
                        env.IMAGE_TAG = "develop-${env.GIT_COMMIT.take(7)}"
                    } else {
                        env.IMAGE_TAG = "${env.BRANCH_NAME}-${env.GIT_COMMIT.take(7)}"
                    }
                }
                echo "Docker image tag set to: ${env.IMAGE_TAG}"
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                        sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                        sh "docker logout"
                    }
                }
            }
        }
    }
}

