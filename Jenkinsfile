pipeline {
          agent {
              label 'BuildServer'
          }

          environment {
              // def img = ("${env.JOB_NAME}:${env.BUILD_ID}").toLowerCase()
              def registry = "gonesai4/llm_project1"
              def img = "${registry}" + ":${env.BUILD_ID}"
              def KEY = "${env.OPENAI_API_KEY}"
          }

          stages {
            stage('Checkout Code') {
                        steps {
                            echo 'Checkout Code'
                            //git 'https://github.com/gonesai4/llm_project1.git'
                            git branch: 'main', credentialsId: 'Git-credentials', url: 'https://github.com/gonesai4/llm_project1.git'
                            sh 'ls -l'
                        }
            }

            stage('Build Image') {
                        steps {
                            echo 'Build Docker Image using Docker file'
                            // docker build -t flaskapp:v1 .
                            script {
                              dockerImg = docker.build("${img}")
                            }
                        }
            }

            stage('Deploy Container') {
                    steps {
                        echo 'Deploy Container'
                        script {
                            sh returnStatus: true, script: 'docker stop $(docker ps -a | grep ${env.registry} | awk \'{print $1}\')'
                            cont = docker.image("${img}").run("-p 80:80 OPENAI_API_KEY='${KEY}'")
                            // sleep (100)
                        }
                    }
            }

            /*stage('Release') {
              steps {
                  echo 'Distribute Image to the Docker Hub'
                  script {
                      docker.withRegistry('https://registry.docker.com','docker_registry'){
                          dockerImg.push()
                          dockerImg.push('latest')
                      }
                  }
              }
            }*/
         }
}
