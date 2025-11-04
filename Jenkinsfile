pipeline {
    agent any

    environment {
        IMAGE_TAG = ''
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

        stage('Build and Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', 
                                                  usernameVariable: 'DOCKER_USER', 
                                                  passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin
                        docker build -t \$DOCKER_USER/flask-app-example:\$IMAGE_TAG .
                        docker push \$DOCKER_USER/flask-app-example:\$IMAGE_TAG
                    """
                }
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

