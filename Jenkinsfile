pipeline {
    agent any

    environment {
        // Usa le credenziali DockerHub che hai aggiunto in Jenkins (ID = dockerhub-creds)
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
    }

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Set Image Tag') {
            steps {
                script {
                    if (env.GIT_TAG_NAME) {
                        env.IMAGE_TAG = "${env.GIT_TAG_NAME}"
                    } else if (env.BRANCH_NAME == 'main') {
                        env.IMAGE_TAG = 'latest'
                    } else if (env.BRANCH_NAME == 'develop') {
                        env.IMAGE_TAG = "develop-${env.GIT_COMMIT.substring(0,7)}"
                    } else {
                        env.IMAGE_TAG = "unknown-${env.GIT_COMMIT.substring(0,7)}"
                    }
                    echo "Docker image tag set to: ${env.IMAGE_TAG}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                    docker build -t ${DOCKERHUB_CREDENTIALS_USR}/flask-app-example:${IMAGE_TAG} .
                """
            }
        }

        stage('Push Docker Image') {
            steps {
                sh """
                    echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin
                    docker push ${DOCKERHUB_CREDENTIALS_USR}/flask-app-example:${IMAGE_TAG}
                """
            }
        }
    }

    post {
        success {
            echo "Docker image pushed successfully!"
        }
        failure {
            echo "Pipeline failed. Check the logs."
        }
    }
}

