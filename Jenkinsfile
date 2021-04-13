pipeline {
  agent {
    docker { image 'jenkins/agent' }
  }
  stages {
    stage('everything') {
      steps {
        checkout scm
        dir("Docker") {
          docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
            def customImage = docker.build("pgb6/datascraper_test2")
            customImage.push()
          }
        }
      }
    }
  }
}
