node {
    checkout scm
    dir("Docker")){
    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {

        def customImage = docker.build("pgb6/datascraper_test")
        customImage.push()
    }
  }
  
}
