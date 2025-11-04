pipeline {
    agent any

    environment {
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
                        env.IMAGE_TAG = env.GIT_TAG_NAME
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
                script {
                    docker.build("${DOCKERHUB_CREDENTIALS_USR}/flask-app-example:${env.IMAGE_TAG}").withRun { c ->
                        sh """
                        echo "${DOCKERHUB_CREDENTIALS_PSW}" | docker login -u "${DOCKERHUB_CREDENTIALS_USR}" --password-stdin
                        docker push ${DOCKERHUB_CREDENTIALS_USR}/flask-app-example:${env.IMAGE_TAG}
                        """
                    }
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

