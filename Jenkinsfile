pipeline {
  agent any

  stages {
    stage('Compile') {
      steps {
        sh '''
          chmod +x gradlew
          ./gradlew compileJava
        '''
      }
    }

    stage('Unit test') {
      steps {
        sh '''
          chmod +x gradlew
          ./gradlew test
        '''
      }
    }

    stage('Code coverage') {
      steps {
        sh '''
          chmod +x gradlew
          ./gradlew jacocoTestReport
        '''

        publishHTML(target: [
          reportDir: 'build/reports/jacoco/test/html',
          reportFiles: 'index.html',
          reportName: 'JaCoCo Report'
        ])

        sh '''
          chmod +x gradlew
          ./gradlew jacocoTestCoverageVerification
        '''
      }
    }
  }

  post {
    success {
      setGitHubPullRequestStatus context: 'jenkins/ci', state: 'SUCCESS'
    }
    failure {
      setGitHubPullRequestStatus context: 'jenkins/ci', state: 'FAILURE'
    }
    unstable {
      setGitHubPullRequestStatus context: 'jenkins/ci', state: 'ERROR'
    }
    aborted {
      setGitHubPullRequestStatus context: 'jenkins/ci', state: 'ERROR'
    }
  }
}